#!/usr/bin/python3
'''Flask api

Attrs:
    app: application that run flask wsgi
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(port), threaded=True)
