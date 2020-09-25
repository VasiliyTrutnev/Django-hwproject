from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Categories, Ads
from django.db.models import Count
from django.template import loader

def index(request):
    ad_queryset = Ads.objects.annotate(favorite_nums=Count('favorites')).order_by('-favorite_nums')[:3]
    template = loader.get_template('bullboard/index.html')
    context = {
        'ads': ad_queryset,
        'descr': 'Bullboard - это сайт частных объявлений нового поколения!',
    }
    return HttpResponse(template.render(context))

def allads(request):
    allads_queryset = Ads.objects.all()
    template = loader.get_template('bullboard/allads.html')
    context = {
        'ad_feed': allads_queryset,
    }
    return HttpResponse(template.render(context))

def ad_detail(request, ad_id):
    ad = Ads.objects.get(id=ad_id)
    response = "id:{}|description:{}|author:{}".format(ad.id, ad.description, ad.author)
    return HttpResponse(response)

def ad_by_category(request):
    ad_by_category_queryset = Ads.objects.all()
    return HttpResponse(ad_by_category_queryset)
