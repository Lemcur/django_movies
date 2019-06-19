from django.forms import ModelForm
from movies.models import Movie, Comment

class PartialMovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'movie']

class PartialCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['movie']
