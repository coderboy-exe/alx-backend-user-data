#!/usr/bin/env python3
""" App module (entry point) """
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ Index route. returns JSON payload """
    return jsonify(message="Bienvenue")


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        users route
        Args:
            email: form data field
            password: form data field
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message="user created")
    except ValueError:
        return jsonify(message="email already registered"), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Login handler """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.valid_login(email, password)
        if user:
            session_id = AUTH.create_session(email)
            response = jsonify(email=email, message="logged in")
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logout handler """
    try:
        cookie = request.headers.get('session_id')
        user = AUTH.get_user_from_session_id(cookie)

        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
