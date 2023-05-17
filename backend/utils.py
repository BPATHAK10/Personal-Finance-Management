import requests
from app import API_URL
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

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
def process_data(bank1_data, bank2_data,payment_data):

    bank1_df = pd.DataFrame(bank1_data)
    bank2_df= pd.DataFrame(bank2_data)
    payment_df= pd.DataFrame(payment_data)

    # aggregating the data using pandas
    #renaming the columns
    # Rename columns in each dataset
    bank1_df = bank1_df.rename(columns={'Account No': 'Account Number', 'DATE': 'Transaction Date', 'TRANSACTION DETAILS': 'Transaction Details', 'CHQ.NO.': 'CHQ.NO.', 'VALUE DATE': 'Value Date', 'WITHDRAWAL AMT': 'Withdrawal Amount', 'DEPOSIT AMT': 'Deposit Amount', 'BALANCE AMT': 'Balance'})
    bank2_df = bank2_df.rename(columns={'Bank Account': 'Account Number', 'Transaction Date': 'Transaction Date', 'Transaction Details': 'Transaction Details', 'Value Date': 'Value Date', 'Withdrawal Amount': 'Withdrawal Amount', 'Deposit Amount': 'Deposit Amount', 'Current Balance': 'Balance'})
    payment_df = payment_df.rename(columns={'Account Number': 'Account Number', 'Date of transaction': 'Transaction Date', 'Remarks': 'Transaction Details', 'Withdrawal Amount': 'Withdrawal Amount', 'Deposit Amount': 'Deposit Amount', 'Balance': 'Balance'})

    # Add a column indicating the source for each dataframe
    bank1_df['Source'] = 'Bank 1'
    bank2_df['Source'] = 'Bank 2'
    payment_df['Source'] = 'Payment Processor'

    # Assume you have three DataFrames: df1, df2, df3
    common_columns = list(set(bank1_df.columns).intersection(bank2_df.columns).intersection(payment_df.columns))
    # Select common columns and drop the rest
    bank1_df = bank1_df[common_columns]
    bank2_df = bank2_df[common_columns]
    payment_df = payment_df[common_columns]

    #Concatenate dataframes
    df_combined = pd.concat([bank1_df[common_columns], bank2_df[common_columns], payment_df[common_columns]], ignore_index=True)

    # cleaning
    #handle missing values
    df_combined.fillna(0,inplace=True)  # Fill missing values with 0

    df_combined.drop_duplicates(inplace=True)  # Drop duplicate rows

    # normalization
    # Calculate min, max, mean, and standard deviation for the columns
    min_deposit = df_combined['Deposit Amount'].min()
    max_deposit = df_combined['Deposit Amount'].max()
    min_withdrawal = df_combined['Withdrawal Amount'].min()
    max_withdrawal = df_combined['Withdrawal Amount'].max()
    mean_balance = df_combined['Balance'].mean()
    std_balance = df_combined['Balance'].std()

    # Min-max scaling for Deposit Amount and Withdrawal Amount
    df_combined['Normalized Deposit Amount'] = (df_combined['Deposit Amount'] - min_deposit) / (max_deposit - min_deposit)
    df_combined['Normalized Withdrawal Amount'] = (df_combined['Withdrawal Amount'] - min_withdrawal) / (max_withdrawal - min_withdrawal)

    # Z-score normalization for Balance
    df_combined['Normalized Balance'] = (df_combined['Balance'] - mean_balance) / std_balance

    # Decrease the Deposit Amount, Withdrawal Amount, and Balance columns by dividing them by 1000
    scaling_factor = 10000

    df_combined['Deposit Amount'] /= scaling_factor
    df_combined['Withdrawal Amount'] /= scaling_factor
    df_combined['Balance'] /= scaling_factor
    df_combined['Normalized Deposit Amount'] /= scaling_factor
    df_combined['Normalized Withdrawal Amount'] /= scaling_factor

    df_combined.to_csv('aggregated_data.csv',index=False)

    return df_combined

def perform_analysis(df_combined):
     pass