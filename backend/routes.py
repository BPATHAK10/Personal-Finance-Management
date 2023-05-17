from flask import request, jsonify,session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from app import app, API_URL
from datetime import datetime
import requests
from utils import *


@app.route('/', methods=['GET'])
def home():
    print("dlafjalsdkf")

    return jsonify({"success": "yess"})

# Authenticate user and generate JWT token with the frontend
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    api_access_token = auth_with_api(username,password)
    if api_access_token:
        session['api_access_token'] = api_access_token
        session['token_created_at'] = datetime.now()
        print("the access token is in the login function with value::"+api_access_token)
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    # Add your own authentication logic here
    # Verify username and password, and generate the JWT token
    if username == 'biraj' and password == 'password123':
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

    # return jsonify({'try':'success'})


    
@app.route('/get-data',methods=["GET"])
def collect_data():
    # get the access token from the session 
    access_token = session.get('api_access_token')

    # Get data from all the sources
    bank1_data = get_data('bank1-data', access_token)
    bank2_data = get_data('bank2-data', access_token)
    payment_data= get_data('payment-data', access_token)
    investment_data = get_data('investment-data', access_token)

    if bank1_data is not None and bank2_data is not None and payment_data is not None and investment_data is not None:
    # All data is collected successfully
        processed_data = process_data(bank1_data,bank2_data,payment_data,investment_data)
        return jsonify({'success':'data successfully collected and normalized'}),200
    else:
        return jsonify({'error':'data could not be collected'}),401

