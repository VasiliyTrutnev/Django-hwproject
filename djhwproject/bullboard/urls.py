from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('allads/', views.allads, name='allads'),
    path('allads/create', views.ad_create, name='ad_create'),
    path('allads/<int:ad_id>/edit', views.ad_edit, name='ad_edit'),
    path('allads/<int:ad_id>/delete', views.ad_delete, name='ad_delete'),
    path('allads/<int:ad_id>/favor', views.favor_ad, name='favor_ad'),
    path('ad_detail/<int:ad_id>', views.ad_detail, name='ad_detail'),
    path('ad_by_category/', views.ad_by_category, name='ad_by_category'),
    path('category_detail/<int:category_id>', views.category_detail, name='category_detail'),

]