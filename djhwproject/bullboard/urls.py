from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('allads/', views.AlladsView.as_view(), name='allads'),
    path('allads/create', views.AdCreateView.as_view(), name='ad_create'),
    path('allads/<int:ad_id>/edit', views.AdEditView.as_view(), name='ad_edit'),
    path('allads/<int:ad_id>/delete', views.AdDeleteView.as_view(), name='ad_delete'),
    path('allads/<int:ad_id>/delete_success', TemplateView.as_view(
        template_name='bullboard/delete_success.html'), name='delete-ad-success'),
    path('allads/<int:ad_id>/favor', views.AdFavorView.as_view(), name='favor_ad'),
    path('ad_detail/<int:ad_id>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad_by_category/', views.AdByCategoryView.as_view(), name='ad_by_category'),
    path('category_detail/<int:category_id>', views.CategoryDetailView.as_view(), name='category_detail'),

]