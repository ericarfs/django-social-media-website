from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from user import views

app_name = 'user'

urlpatterns = [
    path('account/signup', SignUpView, name='signup'),
    path('account/login', LoginView, name='login'),
    path('account/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('home', views.homeView, name='home'),
    path('<str:user>/', views.profileDetailView, name='profile-detail'),
]