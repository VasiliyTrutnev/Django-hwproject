from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Profile, Categories, Ads
from django.db.models import Count
from django.template import loader
from .forms import AdForm

def index(request):
    """
    Вьюха главной страницы, показывает наиболее популярные объявления
    """
    ad_queryset = Ads.objects.annotate(favorite_nums=Count('favorites')).order_by('-favorite_nums')[:3]
    template = loader.get_template('bullboard/index.html')
    context = {
        'ads': ad_queryset,
        'descr': 'Bullboard - это сайт частных объявлений нового поколения!',
    }
    return HttpResponse(template.render(context))

def ad_create(request):
    """
    Вьюха для создания объявления
    """
    form = AdForm()
    context = {'form': form}
    template_name = 'bullboard/ad_create.html'

    if request.method == 'GET':
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = AdForm(request.POST, request.FILES)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            context['ad_was_created'] = True
            return render(request, template_name, context)
        else:
            context['ad_was_created'] = False
            context['form'] = form
            return render(request, template_name, context)


def ad_edit(request, ad_id):
    """
    Вьюха для редактирования публикации
    """
    ad = Ads.objects.get(id=ad_id)
    response = "Редактирование объявления Author:{}| description:{}".format(
        ad.author, ad.description)
    return HttpResponse(response)

def ad_delete(response, ad_id):
    """
    Вьюха для удаления объявления
    """
    ad = Ads.objects.get(id=ad_id)
    response = "Удаление объявления Author:{}| description:{}".format(
        ad.author, ad.description)
    return HttpResponse(response)

def favor_ad(request, ad_id):
    """
    Вьюха для добавления в избранное
    """
    print(request.POST)
    ad = Ads.objects.get(id=ad_id)
    if request.user in ad.favorites.all():
        favor = ad.favorites.get(pk=request.user.id)
        ad.favorites.remove(favor)
    else:
        ad.favorites.add(request.user)
        ad.save()
    return redirect(request.META.get('HTTP_REFERER'), request)

def allads(request):
    """
    Вьюха, отображающая все объявления
    """
    allads_queryset = Ads.objects.all()
    context = {
        'ad_feed': allads_queryset,
    }
    return render(request, 'bullboard/allads.html', context)

def ad_detail(request, ad_id):
    """
    Вьюха для детального просмотра объявления

    """
    try:
        ad = Ads.objects.get(id=ad_id)
    except Ads.DoesNotExist:
        raise Http404
    context = {
        'ad': ad
    }
    return render(request, 'bullboard/ad_detail.html', context)

def ad_by_category(request):
    """
    Вьюха для отображения всех категорий объявлений

    """
    categ = Categories.objects.all()
    context = {
        'categ': categ
    }
    return render(request, 'bullboard/categories.html', context)

def category_detail(request, category_id):
    """
    Вьюха для фильтра объявлений по категоиям

    """
    cat = Ads.objects.filter(id=category_id)
    context = {
        'cat': cat
    }
    return render(request, 'bullboard/category_detail.html', context)