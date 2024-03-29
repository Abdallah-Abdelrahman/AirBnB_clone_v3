#!/usr/bin/python3
'''Flask api

Attrs:
    app: application that run flask wsgi
'''
from flask import Flask
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


if __name__ == '__main__':
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(port), threaded=True)
