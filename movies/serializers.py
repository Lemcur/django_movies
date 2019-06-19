from .models import Movie, Comment
from rest_framework import serializers

class MovieSerializer(serializers.HyperlinkedModelSerializer):
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
