#!/usr/bin/python3
'''Review REST api blueprint'''
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    '''Route for retrieveing all reviews of a place'''
    reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews), 200


@app_views.route('/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    '''route for getting a place object by ID'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''route to delete a review by id'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<string:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''route for creating a new review'''
    if not storage.get(Place, place_id):
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
    if 'text' not in data:
        return jsonify('Missing text'), 400

    review = Place(**data, place_id=place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    '''route for updating a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return (jsonify(review.to_dict()), 200)
