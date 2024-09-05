#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_session_login() -> str:
    """ GET /auth_session/login
    Return:
      - New session ID for the user if given credentials are valid
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    # Find user with given email in DB
    users = User().search({'email': email})
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404

    # Check if found user has given password
    user = users[0] if users and users[0].is_valid_password(password) else None
    if not user:
        return jsonify({'error': 'wrong password'}), 401

    # Create session ID and log the current user in with a browser cookie
    from api.v1.app import auth
    from os import getenv
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def view_session_logout() -> str:
    """ GET /auth_session/logout
    Return:
      - Status of given session after deletion attempt
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
