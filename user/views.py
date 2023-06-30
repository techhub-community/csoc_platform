import re
import threading
from typing import Any, Dict
from loguru import logger

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django import http
from django.http import JsonResponse
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

from .forms import CustomUserCreationForm, LoginForm, CreateTeamForm, ResetPasswordForm, ForgotPasswordForm
from .models import Member, User, Program, Team, Invite, Inquiry
from csoc_backend.views import AllowTeamCreationMixin
from .signals import send_forgot_password_mail


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
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            status = User.objects.filter(email=email)
            if user is not None:
                login(request, user)
                context = self.get_context_data(**kwargs)
                context['title']='Login Successful'
                context['success_message'] = 'Logged in successfully.'
                context['alert_type'] = 'success'
                return render(request,'landing/index.html',context)
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
        if form.is_valid():
            form.save()
            context = self.get_context_data(**kwargs)
            context['title']='Sign Up Successful'
            context['success_message'] = 'An Verification Mail sent to your Email ID. It might take 2-3 hours to reach you.'
            context['alert_type'] = 'success'
            return render(request,'landing/index.html',context)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    login_url = 'user:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        member = Member.objects.filter(user=user, acceptance_status=True).distinct()
        try:
            team = member.first().team if member.first() else None
            context['team'] = team
            member_count = Member.objects.filter(team=team, acceptance_status=True).distinct().count()
            context['team_members'] = Member.objects.filter(team=team, acceptance_status=True) if team else []
            team_list = Member.objects.filter(user=user, acceptance_status=False).values_list('team', 'pk')
            context['pending_requests'] = { Team.objects.get(pk=team[0]): {"members": Member.objects.filter(team_id=team, acceptance_status=True), "pk": team[1]} for team in team_list}
            context['domain']= settings.DOMAIN
        except:
            member_count = 0
        context['allow_team_creation'] = member_count < 3
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
                if member.user.id != current_user.id:
                    context[f'member{index}'] = member
                    index+=1
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request=request)
        context = self.get_context_data(**kwargs)
        user = request.user
        if form.is_valid():
            created_flag = False
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
                created_flag = True
                member2 = User.objects.get(id=member2)
                member2 = Member.objects.create(user=member2, team=team)
                invite = Invite.objects.create(sender=member1, receiver=member2, team=team)
                invite.save()
            
            if member3 and not Member.objects.filter(user=member3, acceptance_status=True):
                created_flag = True
                member3 = User.objects.get(id=member3)
                member3 = Member.objects.create(user=member3, team=team)
                invite = Invite.objects.create(sender=member1, receiver=member3, team=team)
                invite.save()

            if created_flag:
                request.session['title'] = 'Invite Successful'
                request.session['success_message'] = 'A Verification Mail sent to their Email ID. Team will be updated after their response.'
                request.session['alert_type'] = 'success'
            return redirect('user:create_team')
        else:
            context['title'] = 'Invite request failed'
            context['error_message'] = ' '.join(form.non_field_errors())
            context['alert_type'] = 'error'
        return self.render_to_response(context)

 
class AcceptInviteView(LoginRequiredMixin, AllowTeamCreationMixin, View):
    def get(self, request, **kwargs):
        try:
            member = Member.objects.get(id=self.kwargs.get('pk'))
            if request.user == member.user:
                member.acceptance_status = True
                member.save()
            else:
                logger.info("request user does not match member user, its not there account")
        except:
            logger.info(f"Member does not exit {pk}") 
        return redirect('user:profile')
    

class RejectInviteView(LoginRequiredMixin, AllowTeamCreationMixin, View):
    def get(self, request, **kwargs):
        try:
            member = Member.objects.get(id=self.kwargs.get('pk'))
            if request.user == member.user:
                member.delete()
            else:
                logger.info("request user does not match member user, its not there account")
        except:
            logger.info(f"Member does not exit {pk}")
        return redirect('user:profile')
    

class EmailVerificationView(View):
    def get(self, request, token):
        user = self.get_user(token)
        if user is not None:
            user.is_active = True
            logger.info(f"{user} is now verified")
            user.save()
            # You can add additional logic here, such as redirecting to a success page
            # {% url 'user:login' %}
            return render(request,'email_verify.html',{'page': reverse_lazy("user:login")})
        else:
            logger.info(f"{user} is cannot be verified, maybe already verified")
            # Handle invalid token, redirect to an error page or show an error message
            return render(request,'email_verify_fail.html',{'page': reverse_lazy("user:login")})
    
    def get_user(self, token):
        User = get_user_model()
        try:
            uidb64, token = token.split(':')
            user = User.objects.get(pk=uidb64)
            if default_token_generator.check_token(user, token):
                return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logger.info(f"{e} for token {token}")
        return None


class ClearSessionDataView(View):
    def delete(self, request, *args, **kwargs):
        try:
            del request.session['title']
            del request.session['success_message']
            del request.session['alert_type']
        except Exception as e:
            logger.info(f"Expection while deleting session data: {e}")
            return JsonResponse({'message':e})
        return JsonResponse({'message': 'Session data cleared successfully'})


def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        inquiry=Inquiry.objects.create(name=name,email=email,subject=subject,message=message)
        inquiry.save()
        # Redirect to a success page or do any other necessary handling
        # Assuming you have a 'success' named URL pattern    

    # Render the form template if not a POST request or form submission fails
    return HttpResponse('OK',status=200)


class CustomPasswordChangeView(TemplateView):
    template_name = "account/change_password.html"
    success_url = reverse_lazy("user:login")
    form_class = ResetPasswordForm

    def dispatch(self, request, *args, **kwargs):
        self.reset_user = self.get_user()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = self.reset_user
        if user is not None:
            print(self.form_class())
            return render(request, self.template_name, {'form': self.form_class()})
        return render(request, template_name="account/login.html")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = self.reset_user
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form, validlink=False))

    def get_user(self):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        try:
            uid = uidb64
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return None

    def form_valid(self, form):
        user = self.reset_user
        if user is not None:
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form, validlink=False))


class ForgotPasswordView(FormView):
    template_name = "account/forgot_password.html"
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("user:login")

    def dispatch(self, request, *args, **kwargs):
        self.email_success = False
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = User.objects.filter(email=email)
        user = users.first()

        if user:
            token = default_token_generator.make_token(user)
            reset_url = self.request.build_absolute_uri(
                reverse_lazy("user:password_reset_confirm", kwargs={"uidb64": user.pk, "token": token})
            )
            pattern = r"http://django"
            replacement_protocol = "https://"
            replacement_domain = "csoc.codeshack.codes"
            reset_url = re.sub(pattern, replacement_protocol + replacement_domain, url)
            email_thread = threading.Thread(
                target=send_forgot_password_mail,
                kwargs=({'reset_url': reset_url, 'user': user})
            )
            email_thread.start()
            self.email_success = True
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        if self.email_success:
            context['title'] = 'Password Recovery Success'
            context['success_message'] = 'Password recovery email has been sent on your email'
            context['alert_type'] = 'success'
            return render(request, 'account/login.html', context)
        context['title'] = 'Password Recovery Failed'
        context['success_message'] = 'There was some issue please try again'
        context['alert_type'] = 'error'
        return render(request, 'account/login.html', context)
