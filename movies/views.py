from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        if len(request.data.get('title', '')) < 1:
            return Response(
                'title needs to be filled in',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            new_movie = Movie(title=request.data.get('title'))
            omdb_request = new_movie.download_omdb_data()
            if omdb_request == 200:
                new_movie.save()
                return Response(MovieSerializer(new_movie).data)
            else:
                return Response(omdb_request, status=status.HTTP_404_NOT_FOUND)

class CommentList(APIView):

    def get(self, request, format=None):
        if request.data.get('movie_id'):
            try:
                movie_id = int(request.data.get('movie_id'))
            except ValueError:
                return Response(
                    'Invalid id provided',
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                comments = Comment.objects.filter(movie_id=movie_id)
                if len(comments):
                    serializer = CommentSerializer(comments, many=True)
                    return Response(serializer.data)
                else:
                    return Response(
                        "No comments for this movie",
                        status=status.HTTP_404_NOT_FOUND
                    )
        else:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    def post(self, request):
        comment_body = request.data.get('comment_body')
        movie_id_str = request.data.get('movie_id')
        if not movie_id_str:
            return Response(
                'movie_id must be provided',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            movie_id = int(movie_id_str)
        except ValueError:
            return Response(
                'Invalid id provided',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            movie = Movie.objects.get(id=movie_id)
        except ValueError:
            return Response(
                'Movie with this ID was not found',
                status=status.HTTP_400_BAD_REQUEST
            )
        if not comment_body:
            return Response(
                'comment body can\'t be blank',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            new_comment = Comment(body=comment_body, movie=movie)
            new_comment.save()
            return Response(CommentSerializer(new_comment).data)

class TopMoviesList(APIView):

    def get(self, request):
        top_movies = Movie.objects.annotate(count=Count('comment')).order_by('-count')
        serializer = TopMoviesSerializer(top_movies, many=True)
        return Response(serializer.data)
