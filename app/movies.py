#!/usr/bin/python
import json

from ast import literal_eval

from bottle import (
    delete,
    error,
    get,
    post,
    put,
    request,
    response,
    run
)
from pymongo.errors import WriteError

from connection import (
    db
)

''' For simplicity we are just using pymongo, however, if we wanted an ORM
system we would use something like MongoEngine, Ming, MongoAlchemy, etc...'''
movies = db.movies
# List of items that should be added as a MongoDB document.
valid_columns = ['title', 'release_date', 'production_company']


def validate_payload(payload):
    """ Method that validates incoming fields for database insertion
        Params:
            payload: dict
        Return:
            validated_item: dict
    """

    validated_item = {}
    if payload:
        # Only validate if key is inside list of valid columns
        validated_item = \
            {key: value for (key, value) in payload.items()
                if key in valid_columns}

    return validated_item


@get('/v1/movies/list')
def movie_list():
    """ Method that returns a list of all movies
        Params:
            void
        Return:
            json response
    """

    data = None
    movie_list = [movie for movie in movies.find({}, {'_id': False})]
    if movie_list:
        """ This is only required if you wish to deal with JSON
            data, and not having to parse the json response in the frontend."""
        data = literal_eval(str(movie_list))

    return {'status': 200, 'data': data}


@post('/v1/movies')
def movie_add():
    """ Method that adds a new movie into the movies collection.
        Params:
            void
        Return:
            json response
    """
    last_inserted = 0
    response = {'status': 400, 'data': [], 'message': 'Bad request'}
    json_data = validate_payload(request.json)

    if json_data:
        last_inserted = movies.insert_one(json_data).inserted_id

    if last_inserted:
        return {
            'status': 201,
            'data': str(last_inserted),
            'message': 'Movie entry has been created'}

    return response


@put('/v1/movies/<title>')
def movie_update(title):
    """ Method that updates an existing movie entry
        Params:
            title: str
        Return:
            json response
    """

    response = {'status': 400, 'data': [], 'message': 'Bad request'}
    json_data = validate_payload(request.json)

    if title:
        try:
            result = movies.update({'title': title}, {'$set': json_data})
        except WriteError:
            response['status'] = 500
            response['message'] = 'Internal server error'
            result = []

    if result and result['updatedExisting']:
        response['message'] = 'Entry has been successfully updated'
        response['status'] = 200

    return response


@delete('/v1/movies/<title>')
def movie_delete(title):
    """ Method that deletes one movie entry given a title.
        Params:
            title: str
        Return:
            json response
    """

    response = {'status': 412, 'data': [], 'message': 'Precondition failed'}
    result = movies.delete_many({'title': title})

    if result.deleted_count:
        response['message'] = 'Item has been successfully removed'
        response['status'] = 204

    return response


@error(400)
def error400(error):
    response.status = 400
    response.content_type = 'application/json'
    return json.dumps({'status': 400, 'data': [], 'message': 'Bad request'})


@error(404)
def error404(error):
    response.status = 404
    response.content_type = 'application/json'
    return json.dumps({'status': 404, 'data': [], 'message': 'Page not found'})


@error(405)
def error405(error):
    response.status = 405
    response.content_type = 'application/json'
    return json.dumps(
        {'status': 405, 'data': [], 'message': 'Method not allowed'})


@error(500)
def error500(error):
    response.status = 500
    response.content_type = 'application/json'
    return json.dumps(
        {'status': 500, 'data': [], 'message': 'Internal server error'})


if __name__ == '__main__':
    run(server='paste', host="localhost", port=8000)
