import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

from app.models import Tag
Tag.objects.all().delete()

tags = []
tags_names = ['Python', 'Django', 'JavaScript', 'React', 'PostgreSQL', 'API', 'Docker', 'HTML', 'CSS', 'Git']

for i in range(10):
    tags.append(Tag(name=tags_names[i]))

Tag.objects.bulk_create(tags)

print(Tag.objects.all())
