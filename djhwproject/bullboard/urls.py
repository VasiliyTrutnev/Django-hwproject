from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('allads/', views.allads, name='allads'),
    path('ad_detail/<int:ad_id>', views.ad_detail, name='ad_detail'),
    path('ad_by_category/', views.ad_by_category, name='ad_by_category'),
    path('category_detail/<int:category_id>', views.category_detail, name='category_detail'),

]