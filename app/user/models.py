from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse 
from itertools import chain
from .managers import ProfileManager
from pages.notifications import notifications_count

# Create your models here.

class Profile(models.Model):
    """Model representing an user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "")
    date_of_birth = models.DateField(null=True, blank=True)
    following = models.ManyToManyField(User, related_name='following', blank = True)
    blocked = models.ManyToManyField(User, related_name='blocked_users', blank = True)
    silenced = models.ManyToManyField(User, related_name='silenced_users', blank = True)
    question_helper = models.TextField(max_length=200, default = "Ask me anything !", null=True, blank=True)
    allow_anonymous_questions = models.BooleanField(default = True)

    objects = models.Manager()
    profiles = ProfileManager()

    def get_absolute_url(self):
        """Returns the url to access a particular profile."""
        return reverse('profile-detail', args=[self.user.username])

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)

    def get_user(self):
        """String for representing the Model object."""
        return str(self.user.username)

    @property
    def notif_count(self):
        return notifications_count(self.user)

    """FOLLOWING METHODS"""
    def get_following(self):
        """Returns the users the account is following."""
        return self.following.all()

    def get_following_users(self):
        """Returns a list of users the account is following."""
        following_list = [user for user in self.get_following()]
        return following_list

    @property
    def following_count(self):
        """Returns the number of users the account is following."""
        return self.get_following().count()


    """FOLLOWERS METHODS"""    
    def get_followers(self):
        query_set = Profile.objects.all()
        followers_list = []
        for profile in query_set:
            if self.user in profile.get_following():
                followers_list.append(profile.user)

        return followers_list

    @property
    def followers_count(self):
        """Returns the number of users the account is following."""
        return len(self.get_followers())


    """SILENCED METHODS"""
    def get_silenced(self):
        """Returns the users the account blocked."""
        return self.silenced.all()

    def get_silenced_users(self):
        """Returns a list of users the account blocked."""
        silenced_list = [user for user in self.get_silenced()]
        return silenced_list

    @property
    def silenced_count(self):
        """Returns the number of users the account blocked."""
        return self.get_silenced().count()

    
    """SILENCED BY METHODS"""
    def get_silenced_by_users(self):
        """Returns a list of users that blocked the account."""
        query_set = Profile.objects.all()
        silenced_by_list = []
        for profile in query_set:
            if self.user in profile.get_silenced_users():
                silenced_by_list.append(profile.user)

        return silenced_by_list

    @property
    def silenced_by_count(self):
        """Returns the number of users the account blocked."""
        return len(self.get_silenced_by_users())


    """BLOCKED METHODS"""
    def get_blocked(self):
        """Returns the users the account blocked."""
        return self.blocked.all()

    def get_blocked_users(self):
        """Returns a list of users the account blocked."""
        blocked_list = [user for user in self.get_blocked()]
        return blocked_list

    @property
    def block_count(self):
        """Returns the number of users the account blocked."""
        return self.get_blocked().count()

    
    """BLOCKED BY METHODS"""
    def get_blocked_by_users(self):
        """Returns a list of users that blocked the account."""
        query_set = Profile.objects.all()
        blocked_by_list = []
        for profile in query_set:
            if self.user in profile.get_blocked_users():
                blocked_by_list.append(profile.user)

        return blocked_by_list

    @property
    def block_by_count(self):
        """Returns the number of users the account blocked."""
        return len(self.get_blocked_by_users())

    
    """POSTS METHODS"""  
    def get_my_posts(self):
        posts = [self.post_set.all()]
        query_set = None

        if len(posts) > 0:
            query_set = sorted(chain(*posts), reverse = True, key=lambda obj: obj.created_at)
        return query_set

    @property
    def posts_count(self):
        return self.post_set.all().count()

    def get_my_and_following_posts(self):
        users = [user for user in self.get_following()]
        posts = []
        query_set = None
        for u in users:
            profile = Profile.objects.get(user = u)
            profile_posts = profile.post_set.all()
            posts.append(profile_posts)

        my_posts = self.post_set.all()
        posts.append(my_posts)

        if len(posts) > 0:
            query_set = sorted(chain(*posts), reverse = True, key=lambda obj: obj.created_at)
        
        return query_set
    

    




