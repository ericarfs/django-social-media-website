from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns
from user.models import Profile 
from django.utils import timezone, dateformat
from django.core.validators import MinLengthValidator


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
