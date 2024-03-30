#!/usr/bin/python3
'''Handels amenity RESTFul API actions'''
from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('amenities', strict_slashes=False)
def get_amenities():
    '''gets all amenities'''

    amenities = storage.all(Amenity)
    resp = [a.to_dict() for a in amenities.values()]
    return (jsonify(resp), 200)


@app_views.route('amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    '''get a amenity by id '''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return (jsonify(amenity.to_dict()), 200)


@app_views.route('amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    '''delets an existing amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity_id:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('amenities',
                 strict_slashes=False, methods=['POST'])
def create_amenity():
    '''a post request to create a new amenity'''
    try:
        data = request.get_json(force=True)
        if 'name' not in data:
            return jsonify('Missing name'), 400
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    '''a put request to update a amenity object'''
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    try:
        data = request.get_json(force=True)
        for k, v in data.items():
            if k not in ('id', 'created_at', 'updated_at'):
                setattr(amenity, k, v)

            amenity.save()
        return (jsonify(amenity.to_dict()), 200)

    except Exception:
        return jsonify('Not a JSON'), 400
