from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.SimpleRouter()
router.register(r'^movies', views.MovieList)
router.register(r'^comments', views.CommentList)
router.register(r'^top', views.TopMoviesList)
app_name = 'movies'

urlpatterns = [
    # path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>', views.MovieDetailView.as_view()),
    # path('comments/', views.CommentList.as_view()),
    # path('top/', views.TopMoviesList.as_view()),
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
