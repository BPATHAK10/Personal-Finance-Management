from flask import Flask, render_template, request, redirect, jsonify,session
from flask_cors import CORS

import requests
import json
from datetime import datetime, timedelta
import requests
import pandas as pd
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
app.secret_key = "this is a secret key"
app.config['JWT_SECRET_KEY'] = 'personal-finance-manager-backend'  # Replace with your own secret key
jwt = JWTManager(app)

API_URL = 'http://127.0.0.1:5001/'

from routes import *

# Set token expiration time in minutes
TOKEN_EXPIRATION_MINUTES = 30

# @app.before_request
# def check_token_expiration():
#     # Check if the access token is present in the session
#     if 'api_access_token' in session:
#         # Retrieve the token creation time from the session
#         token_created_at = session.get('token_created_at')

#         # Calculate the expiration time based on the creation time and token expiration duration
#         token_expiration_time = token_created_at + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

#         # Check if the token has expired
#         if datetime.now() > token_expiration_time:
#             # Token has expired, remove it from the session
#             session.pop('api_access_token', None)
#             session.pop('token_created_at', None)

if __name__ == '__main__':
    app.run(debug=True)