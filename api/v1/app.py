#!/usr/bin/python3
"""Create a new Flask app.

Attrs:
    app: flask application
"""
from os import getenv

from flask import Flask, jsonify, make_response
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
# CORS instance allowing all origins
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config['JSON_SORT_KEYS'] = True
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """Teardown appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
