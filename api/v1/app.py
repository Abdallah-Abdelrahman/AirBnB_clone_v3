#!/usr/bin/python3
'''Flask api

Attrs:
    app: application that run flask wsgi
'''
from os import getenv, environ
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''handles 404 errors'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
