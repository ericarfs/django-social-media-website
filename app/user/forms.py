from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_email

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