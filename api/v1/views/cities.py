#!/usr/bin/python3
'''Handels City RESTFul API actions'''
from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', strict_slashes=False)
def get_citites(state_id):
    '''gets all cities in a state'''

    cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        for city in state.cities:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    '''get's a city using it's id '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    '''delets an existing city '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    '''a post request to create a new city'''
    if not storage.get(State, state_id):
        abort(404)

    try:
        city_data = request.get_json(force=True)
        if 'name' not in city_data:
            return jsonify('Missing name'), 400
        city = City(**city_data, state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201

    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    '''a put request to update a city object'''
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        new_data = request.get_json(force=True)
        for k, v in new_data.items():
            if k not in ['id', 'state_id', 'created_at',
                         'updated_at']:
                setattr(city, k, v)

            city.save()
        return (jsonify(city.to_dict()), 200)

    except Exception:
        return jsonify('Not a JSON'), 400
