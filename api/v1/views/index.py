#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

@app_views.route('/status', methods=["GET"])
def stat():
    """ return json stat: OK """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def class_count():
    """Retrieves the number of each object by type"""
    dic_t = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }
    return dic_t
