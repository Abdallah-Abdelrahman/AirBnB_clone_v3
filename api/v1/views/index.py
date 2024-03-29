#!/usr/bin/python3
'''Index entry '''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    '''Status route'''
    return jsonify({'status': 'OK'})
