from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from django.db.models import Count
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer, TopMoviesSerializer
from movies.api.filters import MovieFilter, CommentFilter

class MovieList(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter,)
    filterset_class = MovieFilter
    queryset = Movie.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        omdb_response = serializer.download_omdb_data()
        if omdb_response.status_code == 200:
            if omdb_response.json().get('Response') == 'True':
                serializer.save()
                _response = {
                    'Movie': serializer.data,
                    'omdb_response': omdb_response.json()
                }
                _status = status.HTTP_200_OK
            else:
                _response = omdb_response.json()
                _status = status.HTTP_404_NOT_FOUND
        else:
            _response = omdb_response.json()
            _status = omdb_response.status_code
        return Response(_response, status=_status)

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

class CommentList(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

# class CommentList(APIView):

#     def get(self, request, format=None):
#         movie_id = request.GET.get('movie')
#         if movie_id:
#             form = PartialCommentForm({'movie': movie_id}, instance=Comment())
#             if form.is_valid():
#                 comments = Comment.objects.filter(movie_id=movie_id)
#                 serializer = CommentSerializer(comments, many=True)
#                 return Response(serializer.data)
#             else:
#                 return Response(form.errors)
#         else:
#             comments = Comment.objects.all()
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data)


#     def post(self, request):
#         new_comment_form = CommentForm(request.data, instance=Comment())
#         if new_comment_form.is_valid():
#             new_comment = new_comment_form.save()
#             return Response(CommentSerializer(new_comment).data)
#         else:
#             return Response(new_comment_form.errors)

class TopMoviesList(ListModelMixin, GenericViewSet):
    serializer_class = TopMoviesSerializer
    queryset = Movie.objects.annotate(count=Count('comment')).order_by('-count')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
