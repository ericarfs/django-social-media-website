from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from pages import views, htmx_views

app_name = 'pages'

urlpatterns = [
    path('', IndexView, name='index'),
    path('about', AboutView.as_view(), name='about'),
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
    path('get_posts',htmx_views.get_posts, name = "get-posts"),
    path('<str:user>/post/<int:id>/edit',htmx_views.edit_post, name = "edit-post"),
    path('save_post/<int:id>',htmx_views.save_post, name = "save-post"),
    path('delete_post/<int:id>',htmx_views.delete_post, name = "delete-post"),
]
