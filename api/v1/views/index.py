#!/usr/bin/python3
"""index file to run the flask app"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """Status route"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def get_storage_stats():
    """Returns the count of all instances of each class in storage."""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    stats = {
            "users": storage.count(User),
            "amenities": storage.count(Amenity),
            "reviews": storage.count(Review),
            "places": storage.count(Place),
            "states": storage.count(State),
            "cities": storage.count(City),
            }

    return jsonify(stats), 200
