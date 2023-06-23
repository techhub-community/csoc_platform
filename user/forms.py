from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Program


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'usn', 
            'program_selected', 
            'techstack', 
            'proficiency', 
            'password1', 
            'password2'
            )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
