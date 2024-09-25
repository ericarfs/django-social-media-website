from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_email
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators = [validate_email])

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'icon',
            'question_helper',
            'allow_anonymous_questions',
        ]