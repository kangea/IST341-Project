# IST341-Project

## Overview
The goal of this project is to build a movie recommendation engine using the MovieLens dataset from the GroupLens Research Group and create a web application that contains a form that takes 5 favorite movies along with ratings, which will be used to recommend ten additional movies to the users. 

## Required softwares 
Python 3.6

Pip pip 19.1

pipenv 2018.11.26

# Run the application
pipenv install

pipenv run python ./movie/manage.py runserver

# Notes 
Application is stated in port 8000 py default

### Application modeling logics is in 

/movie/recommend/service/recommend_service.py

### Application endpoint routes is in 

/movie/recommend/urls.py

### Application controller is in 

/movie/recommend/views.py

### Application UI is in

/movie/recommend/templates/
