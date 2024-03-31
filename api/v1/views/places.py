#!/usr/bin/python3
"""Place REST api blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    '''Route for retrieveing all places in a city'''
    places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places), 200


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    '''route for getting a place object by ID'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    '''route to delete a place by id'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    '''route for creating a new place'''
    if not storage.get(City, city_id):
        abort(404)
    if not request.is_json:
        abort(400, 'Missing name')

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if not storage.get(User, data.get('user_id')):
        abort(404)
    if 'name' not in data:
        return jsonify('Missing name'), 400

    place = Place(**data, city_id=city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    '''route for updating a place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id',
                     'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return (jsonify(place.to_dict()), 200)
