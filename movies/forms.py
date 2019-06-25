from django.forms import ModelForm, ValidationError, Field, CharField
from movies.models import Movie, Comment
import datetime


class DateFromStringField(Field):
    def to_python(self, value):
        try:
            date = datetime.datetime.strptime(value, '%d %b %Y').date()
        except Exception:
            raise ValidationError("Wrong format, accepted format is 01 Jan 2000")
        return date

class PartialMovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title']

class MovieForm(ModelForm):
    released = DateFromStringField()
    title = CharField(required=False)

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'released']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'movie']

class PartialCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['movie']
