from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from pages import views, htmx_views

app_name = 'pages'

handler404 = 'pages.views.redirectPNF' # Added this line in URLconf instead of settings.py

urlpatterns = [
    path('', IndexView, name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('home', views.homeView, name='home'),
    path('inbox/', views.inboxView, name='profile-inbox'),
    path('notifications/', views.notificationsView, name='notifications'),
    path('save_question',htmx_views.save_question, name = "save-question"),
    path('get_questions_by_user',htmx_views.get_questions_by_user, name = "get-questions-by-user"),
    path('<str:user>/', views.profileDetailView, name='profile-detail'),
    path('<str:user>/edit', views.editProfileView, name='profile-edit'),
    path('block_user_inbox/<str:user>',htmx_views.block_user_inbox, name = "block-user-inbox"),
    path('block_user_post/<str:user>',htmx_views.block_user_post, name = "block-user-post"),
    path('delete_question/<int:id>',htmx_views.delete_question, name = "delete-question"),
    path('get_question_by_id/<int:id>',htmx_views.get_question_by_id, name = "get-question-by-id"),
    path('save_answer/<int:id>',htmx_views.save_answer, name = "save-answer"),
    path('get_posts/<str:user>',htmx_views.get_posts, name = "get-posts"),

    path('<str:user>/post/<int:id>',views.postDetailView, name = "post-detail"),
    path('<str:user>/post/<int:id>/edit',htmx_views.edit_post, name = "edit-post"),

    path('get_post/<int:id>',htmx_views.get_post, name = "get-post"),
    path('like_post/<int:id>',htmx_views.like_post, name = "like-post"),
    path('share_post/<int:id>',htmx_views.share_post, name = "share-post"),
    path('save_post/<int:id>',htmx_views.save_post, name = "save-post"),
    path('delete_post/<int:id>',htmx_views.delete_post, name = "delete-post"),

    path('follow_unfollow_user/<str:user>',htmx_views.follow_unfollow_user, name = "follow-unfollow-user"),
    path('mute_unmute_user/<str:user>',htmx_views.mute_unmute_user, name = "mute-unmute-user"),
    path('block_unblock_profile/<str:user>',htmx_views.block_unblock_profile, name = "block-unblock-profile"),
    
    path('save_profile',htmx_views.save_profile_changes, name = "save-profile"),
]
