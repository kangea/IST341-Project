from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core import serializers
from django import forms
from .service.recommend_service import get_popular_movies_mock
from .service.recommend_service import get_all_movies
from .service.recommend_service import get_personalized_recomm 
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
      watchedMovies.append(getMovieidAndRating(form, "movie1","Movie1Rating"))
      watchedMovies.append(getMovieidAndRating(form, "movie2","Movie2Rating"))
      watchedMovies.append(getMovieidAndRating(form, "movie3","Movie3Rating"))
      watchedMovies.append(getMovieidAndRating(form, "movie4","Movie4Rating"))
      watchedMovies.append(getMovieidAndRating(form, "movie5","Movie5Rating"))

      print("WM",watchedMovies)
      recommended_movies = get_personalized_recomm(watchedMovies)
      print(recommended_movies)
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
  Movie1Rating = forms.IntegerField(widget=forms.RadioSelect())
  Movie2Rating = forms.IntegerField(widget=forms.RadioSelect())
  Movie3Rating = forms.IntegerField(widget=forms.RadioSelect())
  Movie4Rating = forms.IntegerField(widget=forms.RadioSelect())
  Movie5Rating = forms.IntegerField(widget=forms.RadioSelect())

def getMovieidAndRating(form, id_att, rating_att):
  id = form.cleaned_data[id_att].split(":")[0]
  rating = form.cleaned_data[rating_att]
  obj = {"movieId": id, "rating":rating}

  return obj
