from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns
from user.models import Profile 
from django.utils import timezone, dateformat
from django.core.validators import MinLengthValidator
import math

# Create your models here.
class Question(models.Model):
    """Model representing a question."""
    sent_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    sent_to = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, related_name = "answer")
    body = models.TextField(max_length=1024, help_text="Ask me anything", validators=[
            MinLengthValidator(4, 'Question must contain at least 4 characters!')
            ])
    created_at = models.DateTimeField(auto_now_add=True)
    is_anon = models.BooleanField(default = True)
    is_answered = models.BooleanField(default = False)
	
    def __str__(self):
        """String for representing the Model object."""
        return self.body


class Answer(models.Model):
    """Model representing an answer."""
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    body = models.TextField(max_length=3072)
	
    def __str__(self):
        """String for representing the Model object."""
        return self.body

    def answer_author(self):
        """String for representing the Model object."""
        return self.question.sent_to

    def question_author(self):
        """String for representing the Model object."""
        return self.question.sent_by

    
class Post(models.Model):
    """Model representing a post."""
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    liked = models.ManyToManyField(User, default=None, blank = True, related_name="post_likes")
    shared = models.ManyToManyField(User, default=None, blank = True, related_name="post_shares")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.pk)
    
    def get_created_at(self):
        """String for representing the Model object."""
        created_date = self.created_at.strftime("%d/%m/%Y %H:%M:%S")

        return created_date

    def get_whenpublished(self):
        now = timezone.now()
        
        diff= now - self.created_at
        
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


    def get_question_author(self):
        return self.answer.question_author().user


    def get_like(self):
	    return self.liked.all()
	
    @property
    def like_count(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        """Returns the url to access a particular profile."""
        return reverse('post-detail', args=[str(self.id)])
