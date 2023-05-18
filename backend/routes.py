from flask import request, jsonify,session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from app import app, API_URL
from datetime import datetime
from utils import *

@app.route('/', methods=['GET'])
def home():
    return jsonify({"success": "api working"})

# Authenticate user and generate JWT token with the frontend
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # get the access token from the api
    api_access_token = auth_with_api(username,password)
    if api_access_token:
        # store the api access token in the session
        session['api_access_token'] = api_access_token
        session['token_created_at'] = datetime.now()
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Verify username and password, and generate the JWT token
    if username == 'biraj' and password == 'password123':
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@jwt_required()    
@app.route('/get-data',methods=["GET"])
def collect_data():
    # get the access token from the session 
    access_token = session.get('api_access_token')

    # Get data from all the sources
    bank1_data = get_data('bank1-data', access_token)
    bank2_data = get_data('bank2-data', access_token)
    payment_data= get_data('payment-data', access_token)

    if bank1_data is not None and bank2_data is not None and payment_data is not None:
    # All data is collected successfully
        processed_data = process_data(bank1_data,bank2_data,payment_data)

        return jsonify({'success':'data successfully collected and normalized'}),200
    else:
        return jsonify({'error':'data could not be collected'}),401

@jwt_required
@app.route('/dashboard',methods=["GET"])
def get_dashboard_data():
    # performs the analysis and stores the result to display in the dashboard
    results = perform_analysis()
    
    return jsonify({'data': results}),200