#!/usr/bin/python3
'''app view blueprint

Attrs:
    app_views: instance of `Blueprint`
'''
from flask import Blueprint

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
