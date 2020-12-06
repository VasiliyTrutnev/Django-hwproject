from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Profile, Categories, Ads, Feedback
from django.db.models import Count
from django.template import loader
from .forms import AdForm, FeedbackForm, LoginForm, SignupForm, UpdateProfileForm
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .exceptions import PermissionDenied
from django.utils import timezone


class IndexView(ListView):
    """Вьюха для главной страницы с наиболее популярными объявлениями"""
    model = Ads
    template_name = 'bullboard/index.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ads.objects.annotate(favorite_nums=Count('favorites')).order_by('-favorite_nums')[:3]


class AdCreateView(CreateView):
    """Вьюха для создания объявления"""
    form_class = AdForm
    template_name = 'bullboard/ad_create.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            context['ad_was_created'] = True
            context['form'] = self.form_class
            return render(request, self.template_name, context)
        else:
            context['ad_was_created'] = False
            context['form'] = form
            return render(request, self.template_name, context)


class AdEditView(UpdateView):
    """
    Вьюха для редактирования публикации
    """
    model = Ads
    pk_url_kwarg = 'ad_id'
    template_name = 'bullboard/ad_edit.html'
    form_class = AdForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("Вы должны быть автором объявления!")
        return super(AdEditView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        ad_id = self.kwargs['ad_id']
        return reverse('ad_edit', args=(ad_id,))


class AdDeleteView(DeleteView):
    """
        Вьюха для удаления объявления
        """
    model = Ads
    pk_url_kwarg = 'ad_id'
    template_name = 'bullboard/ad_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("Вы должны быть автором объявления!")
        return super(AdDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        ad_id = self.kwargs['ad_id']
        return reverse('delete-ad-success', args=(ad_id,))


class AdFavorView(View):
    """Вьюха для добавления объявления в избранное"""
    def get(self, request, ad_id, *args, **kwargs):
        return redirect(reverse('ad', args=(ad_id,)))

    def post(self, request, ad_id, *args, **kwargs):
        ad = get_object_or_404(Ads, id=ad_id)
        if ad.favorites.filter(id=request.user.id).exists():
            favor = ad.favorites.get(pk=request.user.id)
            ad.favorites.remove(favor)
        else:
            ad.favorites.add(request.user)
            ad.save()
        return redirect(request.META.get('HTTP_REFERER'), request)


class AlladsView(ListView):
    """Вьюха для просмотра всех объявлений"""
    template_name = 'bullboard/allads.html'
    model = Ads
    context_object_name = 'ad_feed'

    def get_queryset(self):
        return Ads.objects.all()


class AdDetailView(DetailView):
    """Вьюха для детального просмотра объявления"""
    model = Ads
    feedback_form = FeedbackForm
    pk_url_kwarg = 'ad_id'
    template_name = 'bullboard/ad_detail.html'

    def get(self, request, ad_id, *args, **kwargs):
        ad = Ads.objects.get(id=ad_id)
        context = {'ad': ad}
        return render(request,self.template_name, context)


    @method_decorator(login_required)
    def post(self, request, ad_id, *args, **kwargs):
        """
        Добавление отзыва
        """
        ad = get_object_or_404(Ads, pk=ad_id)
        form = self.feedback_form(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.date_publish = timezone.now()
            feedback.author = request.user
            feedback.in_ad = ad
            feedback.save()
            return render(request=request, template_name=self.template_name, context={'feedback_form': self.feedback_form,
                                                                                      'ad': ad,
                                                                                      'feedbacks': ad.feedback_set.order_by(
                                                                                          '-date_publish')})
        else:
            return render(request=request, template_name=self.template_name, context={'feedback_form': form,
                                                                                      'ad': ad,
                                                                                      'feedbacks': ad.feedback_set.order_by(
                                                                                          '-date_publish')})


class AdByCategoryView(ListView):
    """Вьюха для просмотра категорий объявлений"""
    model = Categories
    template_name = 'bullboard/categories.html'
    context_object_name = 'categ'

    def get_queryset(self):
        return Categories.objects.all()


class CategoryDetailView(View):
    """Вьюха для фильтра объявлений по категории"""
    template_name = 'bullboard/category_detail.html'

    def get(self, request, category_id, *args, **kwargs):
        cat = Ads.objects.filter(id=category_id)
        context = {'cat': cat}
        return render(request,self.template_name, context)


class LoginView(LoginView):
    template_name = 'my_auth/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('bullboard:index'), request)
            else:
                context = {}
                context['form'] = form
                return render(request=request, template_name=self.template_name, context=context)
        else:
            context = {'form': form}
            return render(request=request, template_name=self.template_name, context=context)


class ProfileView(DetailView):
    model = Profile
    template_name = 'bullboard/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__id=self.kwargs['user_id'])


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("bullboard:index"))


class SignupView(View):
    template_name = 'my_auth/signup.html'
    registration_form = SignupForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.registration_form}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(data=request.POST)
        registered = False
        if user_form.is_valid():
            user = user_form.save(commit=True)
            user.email = user_form.cleaned_data['email']
            user.save()
            registered = True
            return render(request, 'my_auth/signup.html',
                          {'registered': registered})
        else:
            return render(request, 'my_auth/signup.html',
                          {'form': user_form,
                           'registered': registered})


class EditProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'bullboard/edit_profile.html'
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("It is not your profile!")
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse('bullboard:profile', args=(user_id,))