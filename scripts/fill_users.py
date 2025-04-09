import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_web.settings')
django.setup()

from app.models import Profile
from django.contrib.auth.models import User

AVATAR_PATH = 'static/img/avatars/avatar1.jpg'
users = []

# for i in range(10):
#     username = f'user{i}'
#     email = f'user{i}@example.com'
#     password = 'testpassword'
#
#     user = User.objects.create_user(username=username, email=email, password=password)
#
#     users.append(Profile(avatar=AVATAR_PATH, user=user))
#
# Profile.objects.bulk_create(users)

print(Profile.objects.all())
