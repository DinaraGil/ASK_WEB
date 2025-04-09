
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

from app.models import Question, Profile, Tag, UserRating, AnswerLike, Answer

users = list(Profile.objects.all())
answers = list(Answer.objects.all())
answerlikes = []

for i in range(10):
    answer= random.choice(answers)
    user = random.choice(users)

    if not AnswerLike.objects.filter(user_id=user, answer_id=answer).exists():
        answerlikes.append(AnswerLike(user_id=user, answer_id=answer, vote=True))

AnswerLike.objects.bulk_create(answerlikes)

print(AnswerLike.objects.all())