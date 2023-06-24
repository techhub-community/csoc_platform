import threading
from typing import Any, Dict

from django import http
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.views.generic import FormView

from .forms import CustomUserCreationForm, LoginForm, CreateTeamForm
from .models import Member, User, Program, Team, Invite, Inquiry
from csoc_backend.views import AllowTeamCreationMixin
from django.conf import settings
from django.core.mail import send_mail

def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        inquiry=Inquiry.create(name=name,email=email,subject=subject,message=message)
        inquiry.save()
        # Redirect to a success page or do any other necessary handling
          # Assuming you have a 'success' named URL pattern

    # Render the form template if not a POST request or form submission fails
    return redirect('index')


class IsUserAuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(IsUserAuthenticatedMixin, TemplateView):
    form_class = LoginForm
    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            status = User.objects.filter(email=email)
            if user is not None:
                login(request, user)
                return redirect("index")
            elif status.values() and not status.values()[0]["is_active"]:
                form.add_error(None, "Your account is not been verified")
            else:
                form.add_error(None, "Invalid login credentials")
        return render(request, self.template_name, {"form": form})


class UserRegisterView(IsUserAuthenticatedMixin, TemplateView):
    template_name = "account/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("user:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.all()
        context['programs'] = programs
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('index')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    login_url = 'user:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        member = Member.objects.filter(user=user, acceptance_status=True).distinct()
        try:
            team = member.first().team
            context['team'] = team
            member_count = Member.objects.filter(team=team, acceptance_status=True).distinct().count()
            context['team_members'] = Member.objects.filter(team=team, acceptance_status=True) if team else []
        except:
            member_count = 0
        context['allow_team_creation'] = member_count < 3
        return context

class UserRequestView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    login_url = 'user:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        member = Member.objects.filter(user=user, acceptance_status=False).distinct()
        context['member'] = member
        return context
    
    
class UserLogoutView(LogoutView):
    next_page = "index"


class UserCreateTeamView(LoginRequiredMixin, AllowTeamCreationMixin, TemplateView):
    template_name = "account/create_team.html"
    form_class = CreateTeamForm
    login_url = 'user:login'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        
        users = User.objects.filter(is_active=True, is_superuser=False, program_selected=current_user.program_selected).exclude(id=current_user.id).distinct()
        
        unavailable_users = Member.objects.filter(acceptance_status=True).distinct().values_list('user_id', flat=True)
        available_users = users.exclude(id__in=unavailable_users)
        
        context['available_users'] = available_users
        
        context['member2'] = None
        context['member3'] = None 
        if Member.objects.filter(user=current_user, acceptance_status=True):
            team = Member.objects.filter(user=current_user, acceptance_status=True).first().team
            members = Member.objects.filter(team=team)
            index = 2
            for member in members:
                print(f'{index} {member.user}')
                if member.user.id != current_user.id:
                    context[f'member{index}'] = member
                    index+=1
        print(context)
        return context
    # email generation, UI update when showing 
    # waiting -> yellow, accpeted -> green, rejected -> dropbox
    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request=request)
        user = request.user
        print(form.errors)
        if form.is_valid():
            member2 = form.cleaned_data.get('member2')
            member3 = form.cleaned_data.get('member3')
            try:
                member1 = Member.objects.get(user=user, acceptance_status=True)
                team = member1.team
            except:
                team_count = Team.objects.all().count()
                team = Team.objects.create(name = f'Team{team_count+1}')
                member1 = Member.objects.create(user=user, team=team, acceptance_status=True)

            if member2 and not Member.objects.filter(user=member2, acceptance_status=True):
                member2 = User.objects.get(id=member2)
                member2 = Member.objects.create(user=member2, team=team)
                invite = Invite.objects.create(sender=member1, receiver=member2, Team=team)
                invite.save()
            
            if member3 and not Member.objects.filter(user=member3, acceptance_status=True):
                member3 = User.objects.get(id=member3)
                member3 = Member.objects.create(user=member3, team=team)
                invite = Invite.objects.create(sender=member1, receiver=member3, Team=team)
                invite.save()

            return redirect('index')            
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
class AcceptInviteView(LoginRequiredMixin, AllowTeamCreationMixin, View):
    def post(self, request, **kwargs):
        member = Member.objects.get(id=self.kwargs.get('pk'))
        member.acceptance_status = True
        member.save()
        return redirect('index')
    
class RejectInviteView(LoginRequiredMixin, AllowTeamCreationMixin, View):
    def post(self, request, **kwargs):
        member = Member.objects.get(id=self.kwargs.get('pk'))
        member.delete()
        return redirect('index')
    
class EmailVerificationView(View):
    def get(self, request, token):
        user = self.get_user(token)
        if user is not None:
            user.is_active = True
            user.save()
            # You can add additional logic here, such as redirecting to a success page
            return render(request,'email_verify.html',{'page':f"http://{settings.DOMAIN}/user/login/"})
        else:
            # Handle invalid token, redirect to an error page or show an error message
            return render(request,'email_verify_fail.html',{'page':f"http://{settings.DOMAIN}/user/login/"})
    
    def get_user(self, token):
        User = get_user_model()
        try:
            uidb64, token = token.split(':')
            user = User.objects.get(pk=uidb64)
            if default_token_generator.check_token(user, token):
                return user
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return None