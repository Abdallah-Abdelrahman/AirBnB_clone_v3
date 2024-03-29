#!/usr/bin/python3
'''app view blueprint

Attrs:
    app_views: instance of `Blueprint`
'''

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *  # noqa: E402
import api.v1.views.states  # noqa: E402
from api.v1.views.cities import *
