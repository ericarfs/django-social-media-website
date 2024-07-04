from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns
from user.models import Profile 


# Create your models here.
class Question(models.Model):
    """Model representing a question."""
    sent_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    sent_to = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, related_name = "answer")
    body = models.TextField(help_text="Ask me anything")
    created_at = models.DateTimeField(auto_now_add=True)
    is_anon = models.BooleanField(default = True)
    is_answered = models.BooleanField(default = False)
	
    def __str__(self):
        """String for representing the Model object."""
        return self.body


class Answer(models.Model):
    """Model representing an question."""
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    body = models.TextField()
	
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
    """Model representing an answer."""
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
        return str(self.created_at)

    def get_like(self):
	    return self.liked.all()
	
    @property
    def like_count(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        """Returns the url to access a particular profile."""
        return reverse('post-detail', args=[str(self.id)])
