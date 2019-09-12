#!/usr/bin/python3
""" Cities objects """

from models import storage
from models.city import City
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_city(state_id):
    """Returns all Cities on State"""
    li_st = []
    if not storage.get("State", state_id):
        abort(404)
    for cty in storage.all("City").values():
        if cty.to_dict()["state_id"] == state_id:
            li_st.append(cty.to_dict())
    return jsonify(li_st)

@app_views.route("/cities/<city_id>", methods=["GET"])
def gt_state_id(city_id):
    """Returns a City object"""
    ci = storage.get("City", city_id)
    if ci:
        return jsonify(ci.to_dict()), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes City object"""
    ci = storage.get("City", city_id)
    if ci:
        ci.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def creat_city(state_id):
    """Creates a City object"""
    n_dic = request.get_json()
    if not storage.get("State", state_id):
        abort(404)
    if not n_dic:
        abort(400, {"Not a JSON"})
    if 'name' not in n_dic:
        abort(400, {"Missing name"})
    n_ci = City(**n_dic)
    storage.save()
    return jsonify(n_ci.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def up_city(city_id):
    """Updates City"""
    n_dic = request.get_json()
    cit = storage.get("City", city_id)
    if not cit:
        abort(404)
    if not n_dic:
        abort(400, {"Not a JSON"})
    if "name" in n_dic:
        for key, val in n_dic.items():
            setattr(cit, key, val)
        state.save()
    return jsonify(state.to_dict()), 200
