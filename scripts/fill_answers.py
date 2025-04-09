
import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

questions = []
from faker import Faker
from app.models import Question, Profile, Answer

fake = Faker()

# Выбрать случайного пользователя как автора
users = list(Profile.objects.all())
questions = list(Question.objects.all())
answers=[]

for i in range(10):
    answer_text = fake.paragraph(nb_sentences=3)
    print("Текст вопроса:", answer_text)
    author = random.choice(users)

    answer = Answer(
        question=random.choice(questions),
        text=answer_text,
        author_id=author,
        created_at=timezone.now(),
        is_correct=random.choice(['True', 'False'])
    )
    answers.append(answer)

Answer.objects.bulk_create(answers)

print(Answer.objects.all())

