from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'pages'

urlpatterns = [
    path('', IndexView, name='index'),
    path('about', AboutView.as_view(), name='about'),
]
