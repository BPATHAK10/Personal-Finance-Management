import requests
from app import API_URL
import pandas as pd

# Authenticate with the api server
def auth_with_api(username,password):
     # Create a JSON object with the username and password
    payload = {'username': username, 'password': password}

    # Set the headers with the content type
    headers = {'Content-Type': 'application/json'}

    # Send a POST request to the API endpoint with the payload
    response = requests.post(API_URL+'auth/login', json=payload, headers=headers)

    if response.status_code == 200:
        # Authentication successful
        access_token = response.json().get('access_token')
        # print("success with token"+access_token)
        return access_token
    else:
        # Authentication failed
        error_message = response.json().get('message')
        print(f'Authentication failed: {error_message}')
        return None

# Fetch the data from the corresponding api endpoint
def get_data(endpoint, access_token):
        # Set the headers with the access token
        headers = {'Authorization': f'Bearer {access_token}'}

        # Send a GET request to the API endpoint with the headers
        response = requests.get(f'{API_URL}/{endpoint}', headers=headers)

        if response.status_code == 200:
            # Request successful
            data = response.json()
            return data
        else:
            # Request failed
            error_message = response.json().get('message')
            print(f'Request failed: {error_message}')
            return None

# aggregate and normalize the data
def process_data(bank1_data, bank2_data,payment_data,investment_data):

    bank1_df = pd.DataFrame(bank1_data)
    print(bank1_df)

    bank2_df= pd.DataFrame(bank2_data)
    print(bank2_df)

    payment_df= pd.DataFrame(payment_data)
    print(payment_df)

    investment_df = pd.DataFrame(investment_data)
    print(investment_df)

    return []