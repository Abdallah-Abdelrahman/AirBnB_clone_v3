#!/usr/bin/python3
'''States REST api blueprint'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    '''Route to retreive all states'''
    resp = [s.to_dict() for s in storage.all(State).values()]
    return jsonify(resp), 200


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    '''Route to retreive state by id'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_state_by_id(state_id):
    '''Route to delete state by id'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    '''Route to add new state'''
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state_by_id(state_id):
    '''Route to udpate state based on id'''
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
