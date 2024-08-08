from ContentGeneration import *
from ContextWindowManager import *
from Database import *
from FAQManager import *
from UserManager import *
from Income_Allocation import *
from UserManager import *

database = Database(host="localhost", database="nimbus", user="root", password="")
database.connect()


context_window = ContextWindowManager(database)
faq_manager = FAQManager(database)
user_manager = UserManager(database)

from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify

app = Flask(__name__)

@app.route('/register_user', methods=['POST'])
def register_user():
    """
    Register a new user with the specified username.

    Args:
    - username (str): The username of the new user.

    Returns:
    - response (json): A JSON object containing the status of the registration and the assigned user ID.
    """
    try:
        username = request.form['username']
        assigned_id = user_manager.register_user(username)
        return jsonify({'status': 'success', 'user_id': assigned_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_user', methods=['GET'])
def get_user():
    """
    Retrieve the user id for a user specified by their username.

    Args:
    - username (str): The username of the user.

    Returns:
    - response (json): A JSON object containing the user data.
    """
    try:
        user_id = request.form('username')
        user_data = user_manager.get_user_id_by_username(user_id)
        return jsonify({'status': 'success', 'user_data': user_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/definition', methods=['GET'])
def get_definition():
    """
    Retrieve the definition for the specified term.

    Args:
    - term (str): The term to retrieve the definition for.

    Returns:
    - response (json): A JSON object containing the definition of the term.
    """
    try:
        term = request.args.get('term')
        faq_manager.add_faq(term)
        user_id = request.args.get('user_id')
        existing_context = context_window.get_last_response(user_id)
        if existing_context:
            context = existing_context[1]
            definition = get_term_meaning(term, context)
        else:
            definition = get_term_meaning(term)
        
        context_window.add_context_window(user_id, term)
        return jsonify({'status': 'success', 'definition': definition})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


app.route('/get_risk_assessment', methods=['POST', 'GET'])
def get_risk_assessment_questions():
    """
    Generates a set of AI-backed risk assessment questions for the user.

    Returns:
    - response (json): A JSON object containing the risk assessment questions.
    """
    try:
        questions = risk_assessment_questions()
        return jsonify({'status': 'success', 'questions': questions})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/risk_level_assignment', methods=['POST', 'GET'])
def assign_risk_level():
    """
    Assigns a risk level to the user based on their responses to the risk assessment questions.

    Args:
    - user_id (int): The ID of the user.
    - quiz (list): The questions and responses to the risk assessment quiz.

    Returns:
    - response (json): A JSON object containing the assigned risk level.
    """
    try:
        user_id = request.form['user_id']
        responses = request.form['quiz']
        risk_profile = risk_level_assignment(responses)
        user_manager.update_user(user_id, risk_id=risk_profile['RiskNo'])
        return jsonify({'status': 'success', 'risk_level': risk_profile})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

@app.route('/investment_options', methods=['POST', 'GET'])
def get_investment_options():
    """
    Retrieve the investment options available for the specified user.

    Args:
    - user_id (int): The ID of the user.

    Returns:
    - response (json): A JSON object containing the investment options.
    """
    try:
        user_id = request.args.get('user_id')
        risk_level = user_manager.get_risk_level(user_id)
        options = investment_option_generation(risk_level)
        return jsonify({'status': 'success', 'options': options})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/diverse_portfolio', methods=['POST', 'GET'])
def generate_portfolio():
    """
    Generate a diverse investment portfolio for the specified user.

    Args:
    - user_id (int): The ID of the user.

    Returns:
    - response (json): A JSON object containing the generated portfolio.
    """
    try:
        user_id = request.args.get('user_id')
        risk_level = user_manager.get_risk_level(user_id)
        portfolio = generate_diversified_portfolio(risk_level)
        return jsonify({'status': 'success', 'portfolio': portfolio})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/quiz_content', methods=['POST', 'GET'])
def get_finance_quiz():
    """
    Retrieve finance-related quiz questions for the specified user.

    Args:
    - user_id (int): The ID of the user.

    Returns:
    - response (json): A JSON object containing the quiz questions.
    """
    try:
        user_id = request.args.get('user_id')
        risk_level = user_manager.get_risk_level(user_id)
        quiz = generate_quizzes(risk_level)
        return jsonify({'status': 'success', 'quiz': quiz})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    """
    Retrieve the frequently asked questions for the specified search term.

    Returns:
    - response (json): A JSON object containing the FAQs.
    """
    try:
        faq_list = faq_manager.get_faq()
        response = return_faqs(faq_list)
        return jsonify({'status': 'success', 'faqs': response})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

@app.route('/finance_content', methods=['POST', 'GET'])
def get_finance_content():
    """
    Retrieve finance-related content for the specified user.

    Args:
    - risk_levels (list): A list of risk levels that the user wants content for.
    - categories (list): A list of content categories that the user wants to explore.

    Returns:
    - response (json): A JSON object containing the finance-related content.
    """
    try:
        risk_levels = request.form.getlist('risk_levels')
        categories = request.form.getlist('categories')
        content = generate_content(risk_levels, categories)
        return jsonify({'status': 'success', 'content': content})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

app.route('/income_allocation', methods=['POST'])
def allocate_income():
    """
    Allocate the user's income based on the specified financial data.

    Args:
    - user_data (dict): Dictionary containing the user's financial data.

    Returns:
    - response (json): A JSON object containing the updated user data.
    """
    try:
        user_data = request.form
        acceptable = enforce_100_percent_rule(user_data)
        updated_data = ai_recommendations(acceptable)
        return jsonify({'status': 'success', 'updated_data': updated_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)