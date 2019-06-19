from django.test import TestCase
import datetime
# from rest_framework.test import RequestsClient
from movies.models import Movie, Comment
from rest_framework.test import APIRequestFactory
from movies.views import MovieList
from unittest.mock import MagicMock

class MovieListTest(TestCase):
    def test_get_returns_movie_list(self):
        Movie(title='Glass', released=datetime.date(2000, 1, 1), genre="Drama").save()
        response = self.client.get('/movies/')
        expected_response = [{
            "title": "Glass",
            "released": '2000-01-01',
            "genre": "Drama"
        }]
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 200)

    def test_post_with_no_title_returns_bad_request(self):
        response = self.client.post('/movies/', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Could not save the movie')

    def test_post_with_title_creates_new_movie(self):
        Movie.download_omdb_data = MagicMock(return_value=200)

        old_movie_count = Movie.objects.all().count()
        self.client.post('/movies/', {'title': 'Glass'})
        new_movie_count = Movie.objects.all().count()
        self.assertEqual(old_movie_count + 1, new_movie_count)

    def test_post_with_wrong_title_does_not_create_movie(self):
        Movie.download_omdb_data = MagicMock(return_value=404)

        old_movie_count = Movie.objects.all().count()
        self.client.post('/movies/', {'title': 'asdasdasdadsadadssadasda'})
        new_movie_count = Movie.objects.all().count()
        self.assertEqual(old_movie_count, new_movie_count)

class CommentListTest(TestCase):
    def test_get_returns_all_comments(self):
        movie = Movie(title='Glass', released=datetime.date(2000, 1, 1), genre="Drama")
        movie.save()
        Comment(body='asd', movie=movie).save()
        response = self.client.get('/movies/comments/')
        expected_response = [{
            'body': 'asd',
            'movie': 'Glass',
        }]
        self.assertEqual(response.json(), expected_response)
