from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core import serializers
from django import forms
from .service.recommend_service import get_popular_movies_mock
from .service.recommend_service import get_all_movies

# Create your views here.

#### Controllers
def health(request):
    return HttpResponse("Application news portal Started", content_type="text/plain")


def home(request):
  popular_movies = get_popular_movies_mock()
  context = {
    "popular_movies":popular_movies
    }
  return render(request, 'index.html', context)

def recform(request):
  movie_list = get_all_movies()
  context = {
    "movie_list":movie_list
    }
  return render(request, 'recform.html', context)