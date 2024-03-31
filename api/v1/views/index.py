#!/usr/bin/python3
"""Index entry for the blueprint.
The module has 2 endpoints handler one for the /status
and the other /stats for counting all the instances as json
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    '''Status route.

    Returns:
        json of status ok
    '''
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats')
def stats():
    '''Route to retrieves the number of each objects by type.

    Returns:
        json of all instances count'''
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.amenity import Amenity
    from models.review import Review
    from models.user import User

    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
        })
