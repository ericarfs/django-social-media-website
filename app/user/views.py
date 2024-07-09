from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserRegistrationForm
from .models import Profile, User

# Create your views here.

def redirectPNF(request, exception): return redirect('home')

@user_passes_test(lambda user: not user.username, login_url='/home', redirect_field_name=None)
def SignUpView(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('/home')
    else:
        user_form = UserRegistrationForm()
        
    
    return render(request, 'user/signup.html', {'user_form': user_form})

#if user is already logged in, redirect to 'home' page.
@user_passes_test(lambda user: not user.username, login_url='/home', redirect_field_name=None)
def LoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'user/login.html', {'form_login': form_login})

def LogoutView(request):
    logout(request)
    return redirect('/')
