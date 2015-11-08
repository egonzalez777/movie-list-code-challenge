import datetime
import json
import requests
import unittest

from mock import (
    patch
)

import movies


class TestMoviesRestAPI(unittest.TestCase):

    @patch('requests.get')
    def test_movie_list_success(self, movie_list):

        movie_list.return_value = \
            json.loads('{"status": 200, "data": [{"release_date":\
                "2014-08-23 10:18:32.926", "production_company": \
                "Rigo Biz", "title": "Some Title 22"}, {"release_date":\
                 "2014-08-23 10:18:32.926", "production_company": \
                 "Rigo Biz LTD", "title": "Some Title 50"}, {"release_date": \
                 "2014-08-23 10:18:32.926", "production_company": \
                 "Sony Bliz", "title": "Updated Title some 100"}, \
                 {"release_date": "2015-08-23 10:18:32.926", \
                 "production_company": "BCBG", "title": "Avengers"}]}')

        result = requests.get('http://localhost:8000/v1/movies/list')

        self.assertTrue(result.get('status'), 200)
        self.assertTrue(len(result.get('data')), 4)

    @patch('requests.post')
    def test_movie_add_success(self, movie_add):
        movie_add.return_value = \
            json.loads('{"status": 201, "message": \
                "Movie entry has been created", \
                "data": "563e51be17dd97f58f118e13"}')

        result = requests.post('http://localhost:8000/v1/movies', data={
            "title": "Test 1",
            "release_date": datetime.datetime.utcnow(),
            "production_company": "Rackspace"})

        self.assertEqual(result.get('status'), 201)
        self.assertEqual(result.get('message'), 'Movie entry has been created')

    @patch('requests.put')
    def test_movie_update_success(self, movie_update):
        movie_update.return_value = json.loads('{"status": 200, "message": \
            "Entry has been successfully updated", "data": []}')

        result = requests.put('http://localhost:8000/v1/movies/Avengers')

        self.assertEqual(result.get('status'), 200)
        self.assertEqual(
            result.get('message'), "Entry has been successfully updated")

    @patch('requests.delete')
    def test_movie_delete_success(self, movie_delete):
        movie_delete.return_value =\
            json.loads('{"status": 204, \
                "message": "Item has been successfully removed",\
                       "data": []}')

        result = requests.delete('http://localhost:8000/v1/movies/Testing')

        self.assertEqual(result.get('status'), 204)
        self.assertEqual(
            result.get('message'), "Item has been successfully removed")

    @patch('requests.get')
    def test_movie_list_404(self, movie_list):
        movie_list.return_value = json.loads(
            '{"status": 404, "data": [], "message": "Page not found"}')

        result = requests.get('http://localhost:8000/v1/movies/list/itemized')

        self.assertEqual(result.get('status'), 404)

    @patch('requests.delete')
    def test_movie_list_405_delete(self, movie_list):
        movie_list.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.delete(
            'http://localhost:8000/v1/movies/list', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.put')
    def test_movie_list_405_put(self, movie_list):
        movie_list.return_value = json.loads(
            '{"status": 500, "data": [], "message": "Internal server error"}')

        result = requests.put('http://localhost:8000/v1/movies/list')

        self.assertEqual(result.get('status'), 500)
        self.assertEqual(result.get('message'), "Internal server error")

    @patch('requests.post')
    def test_movie_list_405_post(self, movie_list):
        movie_list.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.post('http://localhost:8000/v1/movies/list', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.post')
    def test_movie_add_400(self, movie_add):
        movie_add.return_value = json.loads(
            '{"status": 400, "data": [], "message": "Bad request"}')

        result = requests.post('http://localhost:8000/v1/movies', data={})

        self.assertEqual(result.get('status'), 400)
        self.assertEqual(result.get('message'), 'Bad request')

    @patch('requests.put')
    def test_movie_add_405(self, movie_add):
        movie_add.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.put('http://localhost:8000/v1/movies', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.get')
    def test_movie_add_405_get(self, movie_add):
        movie_add.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.get('http://localhost:8000/v1/movies')

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.delete')
    def test_movie_add_405_delete(self, movie_add):

        movie_add.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.delete('http://localhost:8000/v1/movie', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.put')
    def test_movie_update_500(self, movie_update):

        movie_update.return_value = json.loads(
            '{"status": 500, "data": [], "message": "Internal server error"}')

        result = requests.put('http://localhost:8000/v1/movies/Avengers')

        self.assertEqual(result.get('status'), 500)
        self.assertEqual(result.get('message'), "Internal server error")

    @patch('requests.post')
    def test_movie_update_405_post(self, movie_update):

        movie_update.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.post(
            'http://localhost:8000/movies/Avengers', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.put')
    def test_movie_update_405_put(self, movie_update):
        movie_update.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.put('http://localhost:8000/v1/movies/Avengers')

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.delete')
    def test_movie_delete_400(self, movie_delete):
        movie_delete.return_value = json.loads(
            '{"status": 400, "data": [], "message": "Bad request"}')

    @patch('requests.delete')
    def test_movie_delete_404(self, movie_delete):
        movie_delete.return_value = json.loads(
            '{"status": 404, "data": [], "message": "Page not found"}')

    @patch('requests.get')
    def test_movie_delete_405_get(self, movie_delete):

        movie_delete.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.get(
            'http://localhost:8000/v1/movies/Avengers', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.post')
    def test_movie_delete_405_post(self, movie_delete):

        movie_delete.return_value = json.loads(
            '{"status": 405, "data": [], "message": "Method not allowed"}')

        result = requests.post(
            'http://localhost:8000/v1/movies/Avengers', data={})

        self.assertEqual(result.get('status'), 405)
        self.assertEqual(result.get('message'), 'Method not allowed')

    @patch('requests.delete')
    def test_movie_delete_405_delete_non_existing_record(self, movie_delete):

        movie_delete.return_value = json.loads(
            '{"status": 412, "data": [], "message": "Precondition failed"}')

        # Movie that does not exist in our db
        result = requests.delete('http://localhost:8000/v1/movies/Avengers')

        self.assertEqual(result.get('status'), 412)
        self.assertEqual(result.get('message'), "Precondition failed")

    def test_validate_payload(self):

        payload = {
            'title': 'Test title',
            'random_index': 'value',
            'release_date': '1/1/2015', 'production_company': 'Sony'}

        valid_payload = {
            'release_date': '1/1/2015',
            'production_company': 'Sony', 'title': 'Test title'}

        validated_payload = movies.validate_payload(payload)

        self.assertEqual(validated_payload, valid_payload)
