from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from movies.forms import CommentForm, PartialMovieForm, PartialCommentForm
from django.db.models import Count
import requests

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer, TopMoviesSerializer

class MovieList(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_movie_form = PartialMovieForm(request.data, instance=Movie())
        if new_movie_form.is_valid():
            if new_movie_form.instance.download_omdb_data() == 200:
                new_movie = new_movie_form.save()
                return Response(MovieSerializer(new_movie).data)
            else:
                return Response('Could not connect to omdb')
        else:
            return Response('Could not save the movie', status=status.HTTP_400_BAD_REQUEST)

class CommentList(APIView):

    def get(self, request, format=None):
        movie_id = request.GET.get('movie')
        if movie_id:
            form = PartialCommentForm({'movie': movie_id}, instance=Comment())
            if form.is_valid():
                print(request.GET.get('movie'))
                comments = Comment.objects.filter(movie_id=movie_id)
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)
            else:
                return Response(form.errors)
        else:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)


    def post(self, request):
        new_comment_form = CommentForm(request.data, instance=Comment())
        if new_comment_form.is_valid():
            new_comment = new_comment_form.save()
            return Response(CommentSerializer(new_comment).data)
        else:
            return Response(new_comment_form.errors)

class TopMoviesList(APIView):

    def get(self, request):
        top_movies = Movie.objects.annotate(count=Count('comment')).order_by('-count')
        serializer = TopMoviesSerializer(top_movies, many=True)
        return Response(serializer.data)
