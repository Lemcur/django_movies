from django.test import TestCase
import datetime
# from rest_framework.test import RequestsClient
from movies.models import Movie, Comment
from rest_framework.test import APIRequestFactory
from movies.views import MovieList
from unittest.mock import MagicMock
from movies.forms import CommentForm

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
        response = self.client.get('/comments/')
        expected_response = [{
            'body': 'asd',
            'movie': 'Glass',
        }]
        self.assertEqual(response.json(), expected_response)

    def test_get_with_movie_id_returns_only_specific_comments(self):
        movie_1 = Movie(title='Glass', released=datetime.date(2000, 1, 1), genre="Drama")
        movie_2 = Movie(title='it', released=datetime.date(2000, 1, 1), genre="Drama")
        movie_1.save()
        movie_2.save()
        Comment(body='specific comment', movie=movie_1).save()
        Comment(body='invisible', movie=movie_2).save()

        response = self.client.get(f'/comments/?movie={movie_1.pk}')
        expected_response = [{
            'body': 'specific comment',
            'movie': 'Glass',
        }]

        self.assertEqual(response.json(), expected_response)

    def test_get_with_invalid_movie_id_returns_error(self):
        response = self.client.get('/comments/?movie=123qwe')
        expected_response = {
            "movie": [
                "Select a valid choice. That choice is not one of the available choices."
            ]
        }
        self.assertEqual(response.json(), expected_response)

    def test_post_with_valid_data_creates_a_comment(self):
        movie = Movie(title='Glass', released=datetime.date(2000, 1, 1), genre="Drama")
        movie.save()
        old_comments_count = Comment.objects.all().count()
        self.client.post('/comments/', {'body': 'commented', 'movie': movie.pk})
        new_comments_count = Comment.objects.all().count()
        self.assertEqual(old_comments_count + 1, new_comments_count)

    def test_post_with_invalid_data_returns_errors(self):
        response = self.client.post('/comments/', {})
        expected_response = {
            "body": [
                "This field is required."
            ],
            "movie": [
                "This field is required."
            ]
        }
        self.assertEqual(response.json(), expected_response)

class TopMoviesListTest(TestCase):
    def test_get_top_movies_returns_movies_and_their_ranks(self):
        movie_1 = Movie(title='Glass')
        movie_2 = Movie(title='Forrest Gump')
        movie_3 = Movie(title='it')

        movie_1.save()
        movie_2.save()
        movie_3.save()

        Comment(body='first movie', movie=movie_1).save()
        Comment(body='first movie again', movie=movie_1).save()
        Comment(body='second movie', movie=movie_2).save()
        Comment(body='yet another second movie', movie=movie_2).save()\

        expected_response = [{
            'title': 'Glass',
            'total_comments': 2,
            'rank': 1,
        },
        {
            'title': 'Forrest Gump',
            'total_comments': 2,
            'rank': 1,
        },
        {
            'title': 'it',
            'total_comments': 0,
            'rank': 2,
        }]
        response = self.client.get('/top/')
        self.assertEqual(response.json(), expected_response)
