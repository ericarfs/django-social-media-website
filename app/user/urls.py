from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from user import views

app_name = 'user'

urlpatterns = [
    path('signup', SignUpView, name='signup'),
    path('login', LoginView, name='login'),
    path('logout', LogoutView, name='logout'),

]
