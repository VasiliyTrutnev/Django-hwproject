from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.greeting, name='greetings'),
    path('welcome/', views.welcome, name='welcomes')
]