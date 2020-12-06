from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import LoginView, SignupView, ProfileView, EditProfileView, logout_view



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

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:user_id>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:user_id>/profile/edit', login_required(EditProfileView.as_view()), name='edit-profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(template_name='my_auth/password_reset.html'),
         name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(template_name='my_auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/<str:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete')]
