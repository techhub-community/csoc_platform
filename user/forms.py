from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Program, Member


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user
        member2 = cleaned_data.get('member2')
        member3 = cleaned_data.get('member3')

        if Member.objects.filter(user=user, acceptance_status=True):
            team = Member.objects.filter(user=user, acceptance_status=True).first().team
            if member2:
                member2_check = Member.objects.filter(user__id=member2, team=team)
                member2 = None if member2_check else member2
                cleaned_data['member2'] = member2
            if member3:
                member3_check = Member.objects.filter(user__id=member3, team=team)
                member3 = None if member3_check else member3
                cleaned_data['member3'] = member3

        if member2 == member3:
            raise ValidationError("Member 2 and Member 3 cannot be the same.")

        return cleaned_data