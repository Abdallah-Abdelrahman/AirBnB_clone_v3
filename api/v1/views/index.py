#!/usr/bin/python3
'''Index entry '''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    '''Status route'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    '''Route to retrieves the number of each objects by type'''
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
