from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'movies'

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>', views.MovieDetailView.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('top/', views.TopMoviesList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
