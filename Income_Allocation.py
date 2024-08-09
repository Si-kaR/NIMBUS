import joblib
import pandas as pd
import json

def validate_user_data(user_data):
    """
    Validate the user data to ensure that all required fields are present and contain valid values.

    Args:
    - user_data (dict): Dictionary containing user financial data.

    Raises:
    - ValueError: If any required key is missing, if any value is None, 
                  if percentages are out of the 0-100 range, or if income is not positive.
    """
    # List of required keys that must be present in user_data
    required_keys = ['total_income', 'essentials_percentage', 'investments_percentage', 
                     'discretionary_percentage', 'risk_tolerance', 'disposable_percentage']
    # Check for missing keys and None values
    for key in required_keys:
        if key not in user_data:
            raise ValueError(f"Missing key: {key} in user_data")
        if user_data[key] is None:
            raise ValueError(f"Value for {key} cannot be None")

    # Ensure percentage values are within the 0-100 range
    percentage_keys = ['essentials_percentage', 'investments_percentage', 'discretionary_percentage', 'disposable_percentage']
    for key in percentage_keys:
        if not (0 <= user_data[key] <= 100):
            raise ValueError(f"{key} must be between 0 and 100, got {user_data[key]}")
    
    # Ensure that total income is a positive number
    if user_data['total_income'] <= 0:
        raise ValueError(f"total_income must be greater than 0, got {user_data['total_income']}")

    return True

def enforce_100_percent_rule(user_data):
    """
    Ensure that the sum of the 'amount_invested', 'amount_essentials', and 'amount_discretionary'
    equals 100%. If not, raise an error.

    Args:
    - user_data (dict): Dictionary containing user financial data.

    Raises:
    - ValueError: If the sum of the specified percentages is not equal to 100%.

    Returns:
    - user_data (dict): Updated user data.
    """
    total = user_data['amount_invested'] + user_data['amount_essentials'] + user_data['amount_discretionary']
    
    if total != 100:
        raise ValueError(f"The sum of 'amount_invested', 'amount_essentials', and 'amount_discretionary' must equal 100%, but got {total}%")
    
    return user_data

def ai_recommendations(total_income, amount_invested, amount_essentials, amount_discretionary, risk_tolerance):
    """
    Generate AI-based financial recommendations based on the user's financial data.

    Args:
    - user_data (dict): Dictionary containing user financial data.

    Returns:
    - recommendations (dict): Dictionary containing the AI-generated financial recommendations.

    Raises:
    - RuntimeError: If an error occurs during the financial status, savings, or investments prediction.
    """
    user_data = {}
    user_data['total_income'] = total_income
    user_data['amount_invested'] = amount_invested
    user_data['amount_essentials'] = amount_essentials
    user_data['amount_discretionary'] = amount_discretionary
    user_data['risk_tolerance'] = risk_tolerance
    
    user_data['essentials_percentage'] = user_data['amount_essentials'] / user_data['total_income'] * 100
    user_data['investments_percentage'] = user_data['amount_invested'] / user_data['total_income'] * 100
    user_data['discretionary_percentage'] = user_data['amount_discretionary'] / user_data['total_income'] * 100
    user_data['disposable_percentage'] = 100 - (user_data['essentials_percentage'] + user_data['investments_percentage'] + user_data['discretionary_percentage'])


    # Validate the user data before processing
    validate_user_data(user_data)
    
    # Prepare the data for financial status prediction
    user_df_status = pd.DataFrame([{
        'total_income': user_data['total_income'],
        'essentials_percentage': user_data['essentials_percentage'],
        'investments_percentage': user_data['investments_percentage'],
        'discretionary_percentage': user_data['discretionary_percentage'],
        'risk_tolerance': user_data['risk_tolerance']
    }])

    try:
        # Transform data and predict financial status
        processed_status_data = status_preprocessor.transform(user_df_status)
        financial_status_prediction = status_model.predict(processed_status_data)[0]
    except Exception as e:
        raise RuntimeError(f"Error during financial status prediction: {e}")
    
    # Store the financial status prediction in the user data
    user_data['financial_status'] = financial_status_prediction

    # Prepare the data for savings and investments prediction
    user_df_savings_investments = pd.DataFrame([{
        'total_income': user_data['total_income'],
        'disposable_percentage': user_data['disposable_percentage'],
        'financial_status': user_data['financial_status'],
        'risk_tolerance': user_data['risk_tolerance']
    }])

    try:
        # Transform data and predict savings and investments
        processed_savings_data = savings_preprocessor.transform(user_df_savings_investments)
        savings_predictions = savings_model.predict(processed_savings_data)

        processed_investments_data = investments_preprocessor.transform(user_df_savings_investments)
        investments_predictions = investments_model.predict(processed_investments_data)
    except Exception as e:
        raise RuntimeError(f"Error during savings or investments prediction: {e}")

    # Calculate remaining percentage after savings and investments
    total_savings_investments_percentage = savings_predictions[0] + investments_predictions[0]
    remaining_percentage = 100 - total_savings_investments_percentage

    if remaining_percentage < 0:
        raise ValueError(f"Total savings and investments percentage exceeds 100%, got {total_savings_investments_percentage}%")

    # Ensure essentials get a higher percentage than discretionary spending
    total_initial_non_saving_investing_percentage = user_data['essentials_percentage'] + user_data['discretionary_percentage']
    if total_initial_non_saving_investing_percentage == 0:
        raise ValueError("Essentials and discretionary percentages cannot both be zero.")

    remaining_essentials_percentage = remaining_percentage * (user_data['essentials_percentage'] / total_initial_non_saving_investing_percentage)
    remaining_discretionary_percentage = remaining_percentage - remaining_essentials_percentage

    # Update the user data with calculated percentages
    user_data['essentials_percentage'] = remaining_essentials_percentage
    user_data['discretionary_percentage'] = remaining_discretionary_percentage

    # Compile the recommendations into a dictionary
    recommendations = {
        'financial_status': financial_status_prediction,
        'savings_percentage': savings_predictions[0],
        'investments_percentage': investments_predictions[0],
        'essentials_percentage': user_data['essentials_percentage'],
        'discretionary_percentage': user_data['discretionary_percentage'],
        'percentage_left': remaining_percentage
    }

    return json.dumps(recommendations, indent=4)

# Load the pipelines and models
try:
    status_pipeline_loaded = joblib.load('status_pipeline.pkl')
    savings_pipeline_loaded = joblib.load('savings_pipeline.pkl')
    investments_pipeline_loaded = joblib.load('investments_pipeline.pkl')

    status_model = status_pipeline_loaded.named_steps['classifier']
    status_preprocessor = status_pipeline_loaded.named_steps['preprocessor']

    savings_model = savings_pipeline_loaded.named_steps['regressor']
    savings_preprocessor = savings_pipeline_loaded.named_steps['preprocessor']

    investments_model = investments_pipeline_loaded.named_steps['regressor']
    investments_preprocessor = investments_pipeline_loaded.named_steps['preprocessor']
except FileNotFoundError as e:
    raise RuntimeError(f"Pipeline file not found: {e}")
except Exception as e:
    raise RuntimeError(f"Error loading pipelines: {e}")

def main():
    # User data example with necessary fields
    user_data = {
        'total_income': 1000,
        'amount_invested': 40,
        'amount_essentials': 10,
        'amount_discretionary': 50,
        'risk_tolerance': 'High'
    }

    # Enforce the 100% rule on initial amounts
    try:
        user_data = enforce_100_percent_rule(user_data)
    except ValueError as e:
        print(f"An error occurred: {e}")
        # Exit or prompt user to correct inputs
    else:
        # Calculate user percentages based on income and amounts
        user_data['essentials_percentage'] = user_data['amount_essentials'] / user_data['total_income'] * 100
        user_data['investments_percentage'] = user_data['amount_invested'] / user_data['total_income'] * 100
        user_data['discretionary_percentage'] = user_data['amount_discretionary'] / user_data['total_income'] * 100
        user_data['disposable_percentage'] = 100 - (user_data['essentials_percentage'] + user_data['investments_percentage'] + user_data['discretionary_percentage'])

        # Ensure the sum of the percentages is exactly 100%
        total_percentage = user_data['essentials_percentage'] + user_data['investments_percentage'] + user_data['discretionary_percentage'] + user_data['disposable_percentage']
        if total_percentage != 100:
            user_data['disposable_percentage'] += (100 - total_percentage)

        # Generate AI recommendations based on the user data
        try:
            recommendations = ai_recommendations(user_data)
            print("Financial Status Prediction: {}".format(recommendations['financial_status']))
            print("Recommended Savings Percentage: {:.2f}%".format(recommendations['savings_percentage']))
            print("Recommended Investments Percentage: {:.2f}%".format(recommendations['investments_percentage']))
            print("After investing {:.2f}% and saving {:.2f}%, you should manage {:.2f}% for essentials and discretionary expenses.".format(
                recommendations['investments_percentage'],
                recommendations['savings_percentage'],
                recommendations['percentage_left']
            ))
        except Exception as e:
            print(f"An error occurred: {e}")