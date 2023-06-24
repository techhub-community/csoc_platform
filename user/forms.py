from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
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


class CreateTeamForm(forms.Form):
    member2 = forms.CharField(required=False)
    member3 = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        member2 = cleaned_data.get('member2')
        member3 = cleaned_data.get('member3')

        if member2 == member3:
            raise ValidationError("Member 2 and Member 3 cannot be the same.")


        return cleaned_data