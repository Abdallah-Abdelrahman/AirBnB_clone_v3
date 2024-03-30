#!/usr/bin/python3
'''User REST api actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    '''Retrive a list of all Users'''
    resp = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(resp), 200


@app_views.route('users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    '''Retreves a user object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('users/<user_id>',
                 methods=['DELETE'])
def delete_user(user_id):
    '''deletes a user object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def add_user():
    '''creates a new user object'''
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates a User object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ('id', 'email', 'created_at',
                     'updated_at'):
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
