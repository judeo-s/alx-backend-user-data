#!/usr/bin/env python3
"""
A basic Flask application
"""
from flask import jsonify, Flask, request, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """The view function for the index page.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """The view function to handle register users to the database.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return {"message": "email already registered"}, 400

    return {"email": email, "message": "user created"}


@app.route("/sessions", methods=["POST"])
def login():
    """A view functions that handles login requests of registered users.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    response = make_response({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", AUTH._generate_uuid())
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
