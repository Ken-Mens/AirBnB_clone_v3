#!/usr/bin/python3
"""places review"""

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort


@app_views.route("/reviews", methods=["GET"], strict_slashes=False)
def n_reviews():
    """Returns place review json"""
    pl_li = []
    dic_neo = storage.all('Review').values()
    for x in dic_neo:
        pl_li.append(x.to_dict())
    return jsonify(pl_li)


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def n_review_places(place_id):
    """Returns Review objects based on Place"""
    pl_li = []
    dic_neo = storage.get("Place", place_id)
    dic_rev = storage.all("Review").values()
    if not dic_neo:
        abort(404)
    for x in dic_rev:
        if rev.to_dict()["place_id"] == place_id:
            pl_li.append(rev.to_dict())
    return jsonify(pl_li)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review_id(review_id):
    """Returns Review object based on a review_id"""
    x = storage.get("Review", review_id)
    if x:
        return jsonify(x.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_id(review_id):
    """Deletes a Review object"""
    d = storage.get("Review", review_id)
    if d:
        d.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    dic_n = request.get_json()
    ok = storage.get("Place", place_id)
    if not ok:
        abort(404)
    if not dic_n:
        abort(400, {"Not a JSON"})
    if 'user_id' not in dic_n:
        abort(400, {"Missing user_id"})
    if not storage.get("User", dic_n["user_id"]):
        abort(404)
    if 'text' not in dic_n:
        abort(400, {"Missing text"})
    dic_n["place_id"] = place_id
    new_rev = Review(**dic_t)
    new_rev.new()
    storage.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_reviews(review_id):
    """Updates Review object"""
    dic_t = request.get_json()
    dot = storage.get("Review", review_id)
    if not dot:
        abort(404)
    if not dic_t:
        abort(400, {"Not a JSON"})
    for key, val in dic_t.items():
        if key == 'text':
            setattr(dot, key, val)
            storage.save()
    to_d = dot.to_dict()
    return jsonify(to_d), 200
