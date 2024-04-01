#!/usr/bin/python3
"""Index entry for the blueprint.
The module has 2 endpoints handler one for the /status
and the other /stats for counting all the instances as json

Attrs:
    STATS: mapping for each instance count
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


STATS = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User,
        }


@app_views.route('/status', methods=['GET'])
def status():
    '''Status route.

    Returns:
        json of status ok
    '''
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats', methods=['GET'])
def stats():
    '''Route to retrieves the number of each objects by type.

    Returns:
        json of all instances count
    '''
    instances_stats = {k: storage.count(v) for k, v in STATS.items()}

    return jsonify(instances_stats)
