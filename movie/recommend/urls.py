from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('health', views.health, name='health'),
    path('', views.home, name='home'),
    path('recform', views.recform, name='recform')
]