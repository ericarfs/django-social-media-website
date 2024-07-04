from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
############
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from .models import Question, Answer

# Create your views here.
@user_passes_test(lambda user: not user.username, login_url='/home', redirect_field_name=None)
def IndexView(request):
    return render(request, 'pages/index.html')

class AboutView(TemplateView):
    template_name=('pages/about.html') 
