from movies.models import Movie, Comment
import django_filters

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Movie
        fields = ['title', 'released', 'genre']

class CommentFilter(django_filters.FilterSet):

    class Meta:
        model = Comment
        fields = ['body', 'movie']
