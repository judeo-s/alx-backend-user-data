#!/usr/bin/env python3
"""
A basic Flask application
"""
from flask import jsonify, Flask


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """The view function for the index page.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
