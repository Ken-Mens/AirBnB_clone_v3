#!/usr/bin/python3
""" State objects """

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def gt_states():
    """Returns JSON string"""
    li_st = []
    for x in storage.all("State").values():
        li_st.append(x.to_dict())
    return jsonify(li_st), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def gt_state_id(state_id):
    """Returns a State object"""
    stat = storage.get("State", state_id)
    if stat:
        return jsonify(stat.to_dict()), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object & return empty dict"""
    stat = storage.get("State", state_id)
    if stat:
        stat.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_states():
    """Creates a State object"""
    n_dic = request.get_json()
    if not n_dic:
        abort(400, {"Not a JSON"})
    if 'name' not in n_dic:
        abort(400, {"Missing name"})
    state = State(**n_dic)
    storage.new(state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates State object"""
    n_dic = request.get_json()
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not n_dic:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in n_dic.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
