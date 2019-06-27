from .models import Movie, Comment
from rest_framework import serializers
from django.forms import Field, CharField, ValidationError, DateField
import requests
import datetime
from .api.fields import DateFromStringField
from django_movies.settings import ENV
from .api.mixins import DateParsable

APIKEY = ENV('OMDB_API_KEY')

class MovieSerializer(DateParsable, serializers.HyperlinkedModelSerializer):
    released = DateField(input_formats=['%d %b %Y', '%Y %M %D'])
    title = CharField(required=False)

    def download_omdb_data(self):
        omdb_response = requests.get(f'http://www.omdbapi.com/?apikey={APIKEY}&t={self.validated_data.get("title")}')
        omdb_json = omdb_response.json()
        if omdb_json.get('Response') == 'True':
            self.validated_data['genre'] = omdb_json.get('Genre')
            if omdb_json.get('Released') != 'N/A':
                self.validated_data['released'] = self.date_from_string(omdb_json.get('Released'))
        return omdb_response

    class Meta:
        model = Movie
        fields = ('title', 'released', 'genre')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('body', 'movie')

class TopMoviesSerializer(serializers.HyperlinkedModelSerializer):
    total_comments = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    def get_rank(self, obj):
        rank_set = set([])
        for movie in Movie.objects.all():
            rank_set.add(movie.comment_set.count())
        rank_list = list(rank_set)
        rank_list.reverse()
        return rank_list.index(obj.comment_set.count()) + 1

    def get_total_comments(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Movie
        fields = ('title', 'total_comments', 'rank')
