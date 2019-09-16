#!/usr/bin/python3
"""Uses view objects"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve user object"""
    user_l = []
    for u in storage.all("User").values():
        user_l.append = (u.to_dict())
    return jsonify(user_l)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_auser(user_id):
    """Retrieve one user"""
    neo = storage.get('User', user_id)
    if neo:
        return jsonify(neo.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_auser(user_id):
    """Deletes a State object"""
    neo = storage.get("User", user_id)
    if neo:
        neo.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_created():
    """Creates a User object"""
    d = request.get_json()
    if not d:
        abort(400, {"Not a JSON"})
    if 'email' not in d:
        abort(400, {"Missing email"})
    if 'password' not in d:
        abort(400, {"Missing password"})
    neo = User(**dic_t)
    storage.new(neo)
    storage.save()
    return jsonify(neo.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id=None):
    """Updates a User"""
    dic_t = request.get_json()
    x = storage.get("User", user_id)
    if not x:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    for key, value in request.get_json():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(x, key, value)
    storage.save()
    return jsonify(x.to_dict()), 200
