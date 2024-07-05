from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from user import views, htmx_views

app_name = 'user'

urlpatterns = [
    path('account/signup', SignUpView, name='signup'),
    path('account/login', LoginView, name='login'),
    path('account/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('home', views.homeView, name='home'),
    path('inbox/', views.profileInboxView, name='profile-inbox'),
    path('check_question',htmx_views.check_question, name = "check-question"),
    path('save_question',htmx_views.save_question, name = "save-question"),
    path('get_questions_by_user',htmx_views.get_questions_by_user, name = "get-questions-by-user"),
    path('<str:user>/', views.profileDetailView, name='profile-detail'),
    path('block_user/<str:user>',htmx_views.block_user, name = "block-user"),
    path('delete_question/<int:id>',htmx_views.delete_question, name = "delete-question"),
    path('get_question_by_id/<int:id>',htmx_views.get_question_by_id, name = "get-question-by-id"),
    path('save_answer/<int:id>',htmx_views.save_answer, name = "save-answer"),

]
