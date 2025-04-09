from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


# Create your models here.
class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.annotate(like_count=Count('userrating')).order_by('-like_count')

    # def with_tag(self, tag_name):
    #     return self.filter(tags__name=tag_name).order_by('-created_at', '-id')

class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    author_id = models.ForeignKey('Profile', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField()

    def count_likes(self):
        return UserRating.objects.filter(question_id=self, vote=True).count()

# class QusetionInstance(models.Model):
#     STATUS_CHOICES = [('t', 'Taken'), ('a', 'Available')]
#
#     question = models.ForeignKey('Question', on_delete=models.PROTECT)
#     status = models.CharField(choices=STATUS_CHOICES)

# class TagManager(models.Manager):
#     def get_popular(self, count=10):
#         return (self.annotate(questions_count=models.Count('questions'))
#                    .order_by('-questions_count')[:count])

# class ProfileManager(models.Manager):
#     def get_best(self, count=5):
#         return (self.annotate(activity=models.Count('questions') + models.Count('answers'))
#                    .order_by('-activity')[:count])

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Profile(models.Model):
    avatar = models.ImageField(upload_to='static/img/avatars', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

#QuestionLike
class UserRating(models.Model):
    vote = models.BooleanField()
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'question_id')
