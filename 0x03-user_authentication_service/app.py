#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth
from typing import Union

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def hello() -> str:
    """
    Home route
    Returns:
        str: Home page payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register() -> Union[str, tuple]:
    """
    Register user route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Implement a login function to respond to the POST /sessions route.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
