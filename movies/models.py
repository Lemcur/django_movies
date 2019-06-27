from django.db import models
from django.core.validators import MinLengthValidator

import requests, datetime

class Movie(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    released = models.DateField('Year', blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
