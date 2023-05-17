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

if __name__ == '__main__':
    app.run(debug=True)