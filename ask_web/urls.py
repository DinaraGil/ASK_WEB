from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('base', views.base, name='base'),
    path('ask', views.ask, name='ask'),
]
