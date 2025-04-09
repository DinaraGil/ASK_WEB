from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuestionManager(models.Manager):
    # def get_alive(self):
    #     return self.filter(dead_at__is_null = True)
    pass

class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    author_id = models.ForeignKey('Profile', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag')

# class QusetionInstance(models.Model):
#     STATUS_CHOICES = [('t', 'Taken'), ('a', 'Available')]
#
#     question = models.ForeignKey('Question', on_delete=models.PROTECT)
#     status = models.CharField(choices=STATUS_CHOICES)

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Profile(models.Model):
    avatar = models.ImageField(upload_to='static/img/avatars', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserRating(models.Model):
    vote = models.BooleanField()
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)