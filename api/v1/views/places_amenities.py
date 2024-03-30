#!/usr/bin/python3
'''Review REST api the Associative table places_amenities'''
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('places/<place_id>/amenities', strict_slashes=False)
def get_place_aminties(place_id):
    '''Route for retrieveing all amenities for a place'''
    amnts = []
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    for amnt in place.amenities:
        amnts.append(amnt.to_dict())
    return jsonify(amnts), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amentiy_plac(place_id, amenity_id):
    '''route to delete amentiy of a place'''
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity not in place.amenities:
        return abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_amenity_place(place_id, amenity_id):
    '''route for creating a new amenity of place'''
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    if amenity in place.amenities:
        return jsonify(amenity), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity), 201
