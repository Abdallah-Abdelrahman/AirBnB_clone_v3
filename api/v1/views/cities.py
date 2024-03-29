#!/usr/bin/python3
'''Handels City RESTFul API actions'''
from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities')
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


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    '''get's a city using it's id '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''delets an existing city '''

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    '''a post request to create a new city'''

    city_data = request.get_json()
    if not storage.get(State, state_id):
        abort(404)
    if not city_data:
        abort(400, discription='Not a JSON')

    if 'name' not in city_data:
        abort(400, discription='Missing name')

    new_city = City(**city_data)
    new_city.state_id = state_id
    new_city.save()
    return (jsonify(new_city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    '''a put request to update a city object'''

    city = storage.get(City, city_id)
    new_data = request.get_json()
    if not city:
        abort(404)
    if not new_data:
        abort(400, discription='Not a JSON')

    for k, v in new_data.items():
        if k not in ['id', 'state_id', 'created_at',
                     'updated_at']:
            setattr(city, k, v)

    storage.save()
    return (jsonify(city.to_dict()), 200)
