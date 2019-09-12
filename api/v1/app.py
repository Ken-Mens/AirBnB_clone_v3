#!/usr/bin/python3
""" contains teardown and error handler"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")


@app.teardown_appcontext
def teardown_app(exception):
    """Handles teardown of storage"""
    storage.close()


@app.errorhandler(404)
def not_found_err(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
