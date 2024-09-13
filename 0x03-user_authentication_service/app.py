#!/usr/bin/env python3
"""
A basic Flask application
"""
from flask import jsonify, Flask, request, make_response, abort, redirect
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
    response.set_cookie("session_id", AUTH.create_session(email))
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """A view function that handles logout requests of logged in users.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    if AUTH.delete_session(session_id):
        redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """A view function to retrieve profile of registered users.
    """
    session_id = request.cookies.get("session_id")
    email = AUTH.user_email_by_session_id(session_id)
    if email:
        return {"email": f"{email}"}
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """A view function for registered users to request reset tokens
    """
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return {"email": email, "reset_token": reset_token}
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
