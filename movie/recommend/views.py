from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core import serializers
from django import forms

# Create your views here.

#### Controllers
def health(request):
    return HttpResponse("Application news portal Started", content_type="text/plain")


def home(request):
  context = {}
  #return render(request, 'home.html', context)
  return HttpResponse("Application home page", content_type="text/plain")