from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'movies'

# router = routers.DefaultRouter()

# router.register('', views.MovieList)
# # router.register('comments/', views.CommentList)

urlpatterns = [
    path('', views.MovieList.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('top/', views.TopMoviesList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
