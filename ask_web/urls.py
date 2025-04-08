from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('base', views.base, name='base'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('settings', views.settings, name='settings'),
]
