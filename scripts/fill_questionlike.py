
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

from app.models import Question, Profile, Tag, UserRating

users = list(Profile.objects.all())
questions = list(Question.objects.all())
userratings = []

for i in range(10):
    question= random.choice(questions)
    user = random.choice(users)

    userratings.append(UserRating(vote=True, user_id=user, question_id=question))

UserRating.objects.bulk_create(userratings)

print(UserRating.objects.all())