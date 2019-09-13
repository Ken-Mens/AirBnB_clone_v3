#!/usr/bin/python3
"""Amenities view objects"""

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/amenities", methods=["GET"])
def n_amenities():
    """Serialize object into JSON string"""
    li_st = []
    for idx in storage.all('Amenity').values():
        ok = idx.to_dict()
        li_st.append(ok)
    return jsonify(li_st)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_id(amenity_id):
    """Returns a Amenity object"""
    if storage.get("Amenity", amenity_id):
        return jsonify(d.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity_id(amenity_id):
    """Deletes an Amenity object"""
    x = storage.get("Amenity", amenity_id)
    if x:
        storage.delete(x)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def create_amenities():
    """Creates a Amenity"""
    n_dic = request.get_json()
    if not n_dic:
        abort(400, {"Not a JSON"})
    if 'name' not in n_dic:
        abort(400, {"Missing name"})
    new_amen = Amenity(**dic_t)
    storage.new(new_amen)
    storage.save()
    return jsonify(new_amen.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenities(amenity_id):
    """Updates an Amenity """
    dic_t = request.get_json()
    x = storage.get("Amenity", amenity_id)
    if x is None:
        abort(404)
    if not request.json:
        abort(400, {"Not a JSON"})
    if 'name' in dic_t:
        for k, v in dic_t.items():
            setattr(d, k, v)
        storage.save()
    return jsonify(x.to_dict()), 200
