from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from movies.forms import MovieForm, CommentForm, PartialMovieForm, PartialCommentForm
from django.db.models import Count
from django.shortcuts import get_object_or_404
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
            omdb_response = new_movie_form.instance.download_omdb_data()
            if omdb_response.status_code == 200:
                if omdb_response.json().get('Response') == 'True':
                    new_movie = new_movie_form.save()
                    return Response(MovieSerializer(new_movie).data)
                else:
                    return Response(omdb_response.json(), status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(omdb_response.json(), status=omdb_response.status_code)
        else:
            return Response(new_movie_form.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        return Response(MovieSerializer(movie).data)

    def patch(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie_form = MovieSerializer(movie, data=request.data)
        if movie_form.is_valid():
            movie_form.save()
            return Response(MovieSerializer(movie).data)
        else:
            return Response(movie_form.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):

    def get(self, request, format=None):
        movie_id = request.GET.get('movie')
        if movie_id:
            form = PartialCommentForm({'movie': movie_id}, instance=Comment())
            if form.is_valid():
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
