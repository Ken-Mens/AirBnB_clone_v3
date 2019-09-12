#!/usr/bin/python3
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_app(code):
    """Handles teardown of storage"""
    storage.close()


@app.errorhandler(404)
def not_found_err(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
