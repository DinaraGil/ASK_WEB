
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

questions = []
from faker import Faker
from app.models import Question, Profile, Tag

fake = Faker()

Question.objects.all().delete()

# Выбрать случайного пользователя как автора
users = list(Profile.objects.all())
tags = list(Tag.objects.all())

for i in range(10):
    title = fake.sentence(nb_words=6)
    print("Заголовок:", title)
    question_text = fake.paragraph(nb_sentences=3)
    print("Текст вопроса:", question_text)
    author = random.choice(users)
    tags_to_insert = random.sample(tags, k=random.randint(1, 3))

    question = Question(
        title=title,
        text=question_text,
        author_id=author
    )
    question.save()
    question.tags.set(tags_to_insert)
    questions.append(question)

    # title = models.CharField(max_length=255)
    # text = models.CharField(max_length=1000)
    # author_id = models.ForeignKey('Profile', on_delete=models.PROTECT)
    # tags = models.ManyToManyField('Tag')


#Question.objects.bulk_create(questions)
#
print(Question.objects.all())