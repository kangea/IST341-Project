from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core import serializers
from django import forms
from .service.recommend_service import get_popular_movies_mock
from .service.recommend_service import get_all_movies
import json

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
    "movie_list":movie_list,
    "recommended_movies":get_popular_movies_mock()
    }

  if request.method == "POST":
    form = RecommendForm(request.POST) #if no files
    watchedMovies = []
    if form.is_valid():
      #do something if form is valid
      watchedMovies.append(form.cleaned_data['movie1'])
      watchedMovies.append(form.cleaned_data['movie2'])
      watchedMovies.append(form.cleaned_data['movie3'])
      watchedMovies.append(form.cleaned_data['movie4'])
      watchedMovies.append(form.cleaned_data['movie5'])
      print("WM",watchedMovies)
      return render(request, 'results.html', context)  

  return render(request, 'recform.html', context)

def getAllMovies(request):
  movie_list = get_all_movies()
  new_list = []
  length = len(movie_list)
  for x in range(length):
    obj = {
      "id": movie_list[x]["movieId"],
      "text": str(movie_list[x]["movieId"]) + ": "+ movie_list[x]["title"]
    }
    new_list.append(obj)
  res = {
    "results":new_list
  }
  #print(type(movie))
  return JsonResponse(res, safe=False)

class RecommendForm(forms.Form):
  movie1 = forms.CharField(label='Movie 1', max_length=100)
  movie2 = forms.CharField(label='Movie 2', max_length=100)
  movie3 = forms.CharField(label='Movie 3', max_length=100)
  movie4 = forms.CharField(label='Movie 4', max_length=100)
  movie5 = forms.CharField(label='Movie 5', max_length=100)
