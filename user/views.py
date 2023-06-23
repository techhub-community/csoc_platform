from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


# Create your views here.
def register(request):
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # name=form.cleaned_data.get('name')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm() 
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    pass


class RegisterView(TemplateView):
    template_name=""
    form_class = UserRegisterForm

