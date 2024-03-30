#!/usr/bin/python3
'''User REST api blueprint'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    '''Retrive a list of all Users'''
    return jsonify([u.to_dict() for u in storage.all(User).values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    '''Retreves a user object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    '''deletes a user object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    '''creates a new user object'''
    if not request.is_json:
        return jsonify('Not a JSON'), 400
    try:
        data = request.get_json(force=True)
        if 'email' not in data:
            return jsonify('Missing email'), 400
        if 'password' not in data:
            return jsonify('Missing password'), 400
        new_user = User(**data)
        new_user.save()

        return jsonify(new_user.to_dict()), 201
    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    '''Updates a User object'''
    if not request.is_json:
        return jsonify('Not a JSON'), 400
    try:
        data = request.get_json(force=True)
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        for k, v in data.items():
            if k not in ('id', 'email', 'created_at',
                         'updated_at'):
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    except Exception:
        return jsonify('Not a JSON'), 400
