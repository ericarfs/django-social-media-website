from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from user import views

app_name = 'user'

handler404 = 'user.views.redirectPNF' # Added this line in URLconf instead of settings.py


urlpatterns = [
    path('signup', SignUpView, name='signup'),
    path('login', LoginView, name='login'),
    path('logout', LogoutView, name='logout'),

]
