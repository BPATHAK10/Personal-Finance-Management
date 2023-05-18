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

    # Scaling the Deposit Amount, Withdrawal Amount, and Balance columns by dividing them by 1000
    scaling_factor = 10000

    df_combined['Deposit Amount'] /= scaling_factor
    df_combined['Withdrawal Amount'] /= scaling_factor
    df_combined['Balance'] /= scaling_factor
    df_combined['Normalized Deposit Amount'] /= scaling_factor
    df_combined['Normalized Withdrawal Amount'] /= scaling_factor

    # List of values to choose from
    values = ['food','clothing', 'lend/borrow','transportation','housing','entertainment','saving','debt','miscellaneous']

    # Function to randomly choose a value
    def choose_random_value(row):
        return random.choice(values)

    # Apply the function to fill the column with random values
    df_combined['Transaction Category'] = df_combined.apply(choose_random_value, axis=1)

    df_combined.to_csv('aggregated_data.csv',index=False)

    return df_combined

def perform_analysis():
    data = {}
    df_combined = pd.read_csv('aggregated_data.csv')

    # spending habits based on category
    # Calculate total spending per category or transaction type
    spending_per_category = df_combined.groupby('Transaction Category')['Withdrawal Amount'].sum()


    # Sort the spending in descending order
    sorted_spending = spending_per_category.sort_values(ascending=False)
    #formating
    df_spending = pd.DataFrame(sorted_spending)['Withdrawal Amount'].apply(lambda x: '${:,.2f}'.format(x))

    # Print the top 5 spending categories
    data['spending_categories'] = df_spending.to_json(orient='index')

    # savings progress
    # Calculate savings rate as a percentage of income or total transactions
    savings_rate = (df_combined['Deposit Amount'].sum() / df_combined['Withdrawal Amount'].sum()) * 100
    data['savings_rate'] = savings_rate

    # financial recommendation
    # Convert 'Transaction Date' column to datetime data type
    df_combined['Transaction Date'] = pd.to_datetime(df_combined['Transaction Date'])
    # Calculate average monthly expenses
    monthly_expenses = df_combined.groupby(pd.Grouper(key='Transaction Date', freq='M'))['Withdrawal Amount'].sum()
    df_monthly_expenses = pd.DataFrame(monthly_expenses)

    # Calculate average monthly income
    monthly_income = df_combined.groupby(pd.Grouper(key='Transaction Date', freq='M'))['Deposit Amount'].sum()
    df_monthly_income= pd.DataFrame(monthly_income)

    # Calculate average monthly savings
    monthly_savings = monthly_income - monthly_expenses
    df_monthly_savings= pd.DataFrame(monthly_savings)
    df_monthly_savings.rename(columns={0:'saving'},inplace=True)

    # Calculate the total withdrawal, deposit, and balance
    total_withdrawal = df_combined['Withdrawal Amount'].sum()
    total_deposit = df_combined['Deposit Amount'].sum()

    # Plot a bar chart of the total amounts
    categories = ['Withdrawal', 'Deposit']
    amounts = [total_withdrawal, total_deposit]

    plt.bar(categories, amounts)
    plt.xlabel('Type of transaction')
    plt.ylabel('Amount')
    plt.title('Total Financial Amounts')
    plt.savefig('../frontend/personal-finance-frontend/src/assets/bar.png')

    # Line chart of monthly income 
    df_monthly_income.plot(kind='line')
    plt.xlabel('Month')
    plt.ylabel('Total Income')
    plt.title('Monthly Income')

    plt.savefig('../frontend/personal-finance-frontend/src/assets/line_income.png')
    # Line chart of monthly expenses
    df_monthly_expenses.plot(kind='line')
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.title('Monthly Expenses')

    plt.savefig('../frontend/personal-finance-frontend/src/assets/line_expense.png')

    # Budgeting
    # Set budget limits for each category
    budget = {'food': 5000, 'transportation': 20000, 'housing': 10000}

    # Calculate actual spending for each category
    actual_spending = df_combined.groupby('Transaction Category')['Withdrawal Amount'].sum()

    # Compare actual spending with budgeted amount
    budget_status = actual_spending - pd.Series(budget)

    # Identify categories exceeding or staying within the budget
    exceeded_budget = budget_status[budget_status > 0]
    within_budget = budget_status[budget_status <= 0]

    data['exceeded_budget'] = exceeded_budget.to_json(orient='index')

    data['within_budget'] = within_budget.to_json(orient='index')

    # Calculate savings and debt amounts
    savings = df_combined[df_combined['Transaction Category'] == 'saving']['Deposit Amount'].sum()
    debt = df_combined[df_combined['Transaction Category'] == 'debt']['Withdrawal Amount'].sum()

    # Calculate savings rate and debt-to-income ratio
    income = 50000000
    savings_rate = (savings / income) * 100
    debt_to_income_ratio = (debt / income)

    data['debt_to_income_ration'] = debt_to_income_ratio

    # Get the account numbers of all the banks
    acc = []
    account_numbers = df_combined['Account Number'].unique()
    for account_number in account_numbers:
        acc.append(account_number)

    data['accounts'] = acc

    # Convert 'Transaction Date' column to datetime data type
    df_combined['Transaction Date'] = pd.to_datetime(df_combined['Transaction Date'])
    # Get the latest date in the Transaction Date column
    latest_date = df_combined['Transaction Date'].max()

    # Calculate the starting date for the last 15 days
    fifteen_days_ago = latest_date - pd.DateOffset(days=14)

    # Filter the data for the last 15 days
    df_combined = df_combined[(df_combined['Transaction Date'] >= fifteen_days_ago) & (df_combined['Transaction Date'] <= latest_date)]

    # Get the latest balance
    latest_balance = df_combined['Balance'].iloc[-1]
    data['balance'] = latest_balance

    return data