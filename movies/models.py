from django.db import models
from django.core.validators import MinLengthValidator

import requests, datetime

class Movie(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    released = models.DateField('Year', blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def download_omdb_data(self):
        omdb_response = requests.get(f'http://www.omdbapi.com/?apikey=41c8fb8c&t={self.title}')
        omdb_json = omdb_response.json()
        if omdb_json['Response'] == 'True':
            self.genre = omdb_json['Genre']
            self.released = datetime.datetime.strptime(omdb_json['Released'], '%d %b %Y').date()
            return 200
        else:
            return omdb_json


class Comment(models.Model):
    body = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
