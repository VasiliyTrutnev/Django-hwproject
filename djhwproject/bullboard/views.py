from django.shortcuts import render
from django.http import HttpResponse

def greeting(request):
    return HttpResponse('Hello, Guest!')

def welcome(request):
    return HttpResponse('Welcome to BullBoard!')
