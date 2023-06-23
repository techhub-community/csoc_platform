import threading

from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.views.generic import FormView

from .forms import CustomUserCreationForm, LoginForm
from .models import User, Program


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
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.all()
        context['programs'] = programs
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, self.template_name, self.get_context_data())


class UserLogoutView(LogoutView):
    next_page = "index"
