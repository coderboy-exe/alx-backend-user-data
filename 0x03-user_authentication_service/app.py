#!/usr/bin/env python3
""" App module (entry point) """
from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
