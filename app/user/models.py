from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse 
from itertools import chain

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

    def get_absolute_url(self):
        """Returns the url to access a particular profile."""
        return reverse('profile-detail', args=[self.user.username])

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)

    def get_user(self):
        """String for representing the Model object."""
        return str(self.user.username)

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
                followers_list.append(profile)

        return followers_list

    @property
    def followers_count(self):
        """Returns the number of users the account is following."""
        return len(self.get_followers())

    
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
    
    def add_new_following(self, user):
        self.following.add(user)
    
    def add_new_silenced(self, user):
        self.silenced.add(user)
    
    def add_new_blocked(self, user):
        self.blocked.add(user)
    

    




