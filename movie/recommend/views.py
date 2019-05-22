from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core import serializers
from django import forms
from .service.recommend_service import get_popular_movies
from .service.recommend_service import get_all_movies
from .service.recommend_service import get_cosine_recomm 
from .service.recommend_service import get_pearson_recomm 
from .service.recommend_service import get_recomm 
from .service.recommend_service import train_model_general
from .service.recommend_service import train_model_cosine
import json

# Create your views here.

#### Controllers
def health(request):
  """
  Endpoint that is used to start the training the models
  The endpoint is called right after deploying the app to train the model
  and make the model available globally for accessing it in multi user sessions
  This gives flexibility of not having to train the model on every user form submission
  """
  train_model_general()
  train_model_cosine()
  return HttpResponse("Application recommendation Started", content_type="text/plain")


def home(request):
  """
  Endpoint for home page.
  returns "index.html" with popular movies
  """
  popular_movies = get_popular_movies()
  context = {
    "popular_movies":popular_movies
    }
  
  return render(request, 'index.html', context)

def recform(request):
  """
  Endpoint for user movies form submission.
  returns "results.html" with recommended movies if form validation is success
  else return the form page "recform.html" itself
  """ 
  movie_list = get_all_movies()
  context = {
    "movie_list":movie_list,
    "recommended_movies":[]
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
      ## include 5 movie as training is slow
      #watchedMovies.append(getMovieidAndRating(form, "movie6","Movie6Rating"))
      #watchedMovies.append(getMovieidAndRating(form, "movie7","Movie7Rating"))
      #watchedMovies.append(getMovieidAndRating(form, "movie8","Movie8Rating"))
      #watchedMovies.append(getMovieidAndRating(form, "movie9","Movie9Rating"))
      #watchedMovies.append(getMovieidAndRating(form, "movie10","Movie10Rating"))      

      print("WM",watchedMovies)
      recommended_movies1 = get_cosine_recomm(watchedMovies)
      #removed pearson as its slow and poor result
      #recommended_movies2 = get_pearson_recomm(watchedMovies)
      recommended_movies3 = get_recomm(watchedMovies)
      print(recommended_movies1)
      context["recommended_movies1"] = recommended_movies1
      #context["recommended_movies2"] = recommended_movies2
      context["recommended_movies3"] = recommended_movies3
      return render(request, 'results.html', context)  

  return render(request, 'recform.html', context)

def getAllMovies(request):
  """
  format the movies data in such way that,
  auto-fill library typeahead.js expects to use it
  """
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
  """
  used django from model to generate form object,
  has helper methods for form validation.
  """
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
  #movie6 = forms.CharField(label='Movie 6', max_length=100)
  #movie7 = forms.CharField(label='Movie 7', max_length=100)
  #movie8 = forms.CharField(label='Movie 8', max_length=100)
  #movie9 = forms.CharField(label='Movie 9', max_length=100)
  #movie10 = forms.CharField(label='Movie 10', max_length=100)
  #Movie6Rating = forms.IntegerField(widget=forms.RadioSelect())
  #Movie7Rating = forms.IntegerField(widget=forms.RadioSelect())
  #Movie8Rating = forms.IntegerField(widget=forms.RadioSelect())
  #Movie9Rating = forms.IntegerField(widget=forms.RadioSelect())
  #Movie10Rating = forms.IntegerField(widget=forms.RadioSelect())  

def getMovieidAndRating(form, id_att, rating_att):
  """
  helper function to format the form inputs into,
  object of movieId and rating
  """
  id = form.cleaned_data[id_att].split(":")[0]
  rating = form.cleaned_data[rating_att]
  obj = {"movieId": id, "rating":rating}

  return obj
