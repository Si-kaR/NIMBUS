import unittest
from entry import app 
from unittest.mock import patch



class NimbusTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_register_user_success(self):
        # Test the POST request with valid data
        data = {
            'username': 'testuser'
        }
        response = self.client.post('/register_user', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('user_id', response.json)

    def test_register_user_missing_username(self):
        # Test the POST request with missing username
        data = {
            # 'username' is missing
        }
        response = self.client.post('/register_user', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_register_user_exception(self):
        # Mock the user_manager to raise an exception
        with unittest.mock.patch('entry.user_manager.register_user', side_effect=Exception('Test Exception')):
            data = {
                'username': 'testuser'
            }
            response = self.client.post('/register_user', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')


    def test_get_user_success(self):
        # Mock the user_manager.get_user_id_by_username method to return a user data
        with patch('entry.user_manager.get_user_id_by_username') as mock_get_user:
            mock_get_user.return_value = {'id': 1, 'username': 'testuser'}
            
            # Test the GET request with valid username
            response = self.client.get('/get_user', data={'username': 'testuser'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('user_data', response.json)
            self.assertEqual(response.json['user_data']['username'], 'testuser')

    def test_get_user_missing_username(self):
        # Test the GET request with missing username
        response = self.client.get('/get_user', data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_get_user_exception(self):
        # Mock the user_manager.get_user_id_by_username to raise an exception
        with patch('entry.user_manager.get_user_id_by_username', side_effect=Exception('Test Exception')):
            response = self.client.get('/get_user', data={'username': 'testuser'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_definition_success_with_context(self):
        # Mock the necessary methods
        with patch('entry.faq_manager.add_faq') as mock_add_faq, \
             patch('entry.context_window.get_last_response') as mock_get_last_response, \
             patch('entry.get_term_meaning') as mock_get_term_meaning, \
             patch('entry.context_window.add_context_window') as mock_add_context_window:

            mock_get_last_response.return_value = (None, 'existing context')
            mock_get_term_meaning.return_value = 'mocked definition'

            # Test the GET request with valid term and user_id
            response = self.client.get('/definition', data={'term': 'testterm'}, query_string={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['definition'], 'mocked definition')

    def test_get_definition_success_without_context(self):
        # Mock the necessary methods
        with patch('entry.faq_manager.add_faq') as mock_add_faq, \
             patch('entry.context_window.get_last_response') as mock_get_last_response, \
             patch('entry.get_term_meaning') as mock_get_term_meaning, \
             patch('entry.context_window.add_context_window') as mock_add_context_window:

            mock_get_last_response.return_value = None
            mock_get_term_meaning.return_value = 'mocked definition'

            # Test the GET request with valid term and user_id
            response = self.client.get('/definition', data={'term': 'testterm'}, query_string={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['definition'], 'mocked definition')

    def test_get_definition_missing_term(self):
        # Test the GET request with missing term
        response = self.client.get('/definition', data={}, query_string={'user_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_get_definition_exception(self):
        # Mock the necessary methods to raise an exception
        with patch('entry.faq_manager.add_faq', side_effect=Exception('Test Exception')):
            response = self.client.get('/definition', data={'term': 'testterm'}, query_string={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_risk_assessment_success(self):
        # Mock the risk_assessment_questions method to return a list of questions
        with patch('entry.risk_assessment_questions') as mock_risk_assessment_questions:
            mock_risk_assessment_questions.return_value = ['Question 1', 'Question 2']

            # Test the GET request
            response = self.client.get('/get_risk_assessment')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('questions', response.json)
            self.assertEqual(response.json['questions'], ['Question 1', 'Question 2'])

    def test_get_risk_assessment_exception(self):
        # Mock the risk_assessment_questions method to raise an exception
        with patch('entry.risk_assessment_questions', side_effect=Exception('Test Exception')):
            # Test the GET request
            response = self.client.get('/get_risk_assessment')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_assign_risk_level_success(self):
        # Mock the risk_level_assignment and user_manager.update_user methods
        with patch('entry.risk_level_assignment') as mock_risk_level_assignment, \
             patch('entry.user_manager.update_user') as mock_update_user:

            mock_risk_level_assignment.return_value = ('Low', 1)

            # Test the POST request with valid data
            data = {
                'user_id': '1',
                'quiz': ['Question 1', 'Question 2'],
                'responses': ['Answer 1', 'Answer 2']
            }
            response = self.client.post('/risk_level_assignment', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('risk_level', response.json)
            self.assertEqual(response.json['risk_level'], ['Low', 1])

    def test_assign_risk_level_missing_data(self):
        # Test the POST request with missing data
        data = {
            'user_id': '1',
            # 'quiz' and 'responses' are missing
        }
        response = self.client.post('/risk_level_assignment', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_assign_risk_level_exception(self):
        # Mock the risk_level_assignment method to raise an exception
        with patch('entry.risk_level_assignment', side_effect=Exception('Test Exception')):
            data = {
                'user_id': '1',
                'quiz': ['Question 1', 'Question 2'],
                'responses': ['Answer 1', 'Answer 2']
            }
            response = self.client.post('/risk_level_assignment', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_investment_options_success(self):
        # Mock the user_manager.get_risk_level and investment_option_generation methods
        with patch('entry.user_manager.get_risk_level') as mock_get_risk_level, \
             patch('entry.investment_option_generation') as mock_investment_option_generation:

            mock_get_risk_level.return_value = 'Low'
            mock_investment_option_generation.return_value = ['Option 1', 'Option 2']

            # Test the POST request with valid user_id
            data = {'user_id': '1'}
            response = self.client.post('/investment_options', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('options', response.json)
            self.assertEqual(response.json['options'], ['Option 1', 'Option 2'])

    def test_get_investment_options_missing_user_id(self):
        # Test the POST request with missing user_id
        data = {}
        response = self.client.post('/investment_options', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_get_investment_options_exception(self):
        # Mock the user_manager.get_risk_level method to raise an exception
        with patch('entry.user_manager.get_risk_level', side_effect=Exception('Test Exception')):
            data = {'user_id': '1'}
            response = self.client.post('/investment_options', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')


    def test_generate_portfolio_success(self):
        # Mock the user_manager.get_risk_level and generate_diversified_portfolio methods
        with patch('entry.user_manager.get_risk_level') as mock_get_risk_level, \
             patch('entry.generate_diversified_portfolio') as mock_generate_portfolio:

            mock_get_risk_level.return_value = 'Low'
            mock_generate_portfolio.return_value = ['Stock A', 'Bond B']

            # Test the GET request with valid user_id
            response = self.client.get('/diverse_portfolio', query_string={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('portfolio', response.json)
            self.assertEqual(response.json['portfolio'], ['Stock A', 'Bond B'])

    def test_generate_portfolio_missing_user_id(self):
        # Test the GET request with missing user_id
        response = self.client.get('/diverse_portfolio')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success') # Automatically assumes a risk level of medium
        self.assertIn('portfolio', response.json)

    def test_generate_portfolio_exception(self):
        # Mock the user_manager.get_risk_level method to raise an exception
        with patch('entry.user_manager.get_risk_level', side_effect=Exception('Test Exception')):
            response = self.client.get('/diverse_portfolio', query_string={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_finance_quiz_success(self):
        # Mock the user_manager.get_risk_level and generate_quizzes methods
        with patch('entry.user_manager.get_risk_level') as mock_get_risk_level, \
             patch('entry.generate_quizzes') as mock_generate_quizzes:

            mock_get_risk_level.return_value = 'Low'
            mock_generate_quizzes.return_value = ['Question 1', 'Question 2']

            # Test the POST request with valid user_id
            data = {'user_id': '1'}
            response = self.client.post('/quiz_content', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('quiz', response.json)
            self.assertEqual(response.json['quiz'], ['Question 1', 'Question 2'])

    def test_get_finance_quiz_missing_user_id(self):
        # Test the POST request with missing user_id
        data = {}
        response = self.client.post('/quiz_content', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_get_finance_quiz_exception(self):
        # Mock the user_manager.get_risk_level method to raise an exception
        with patch('entry.user_manager.get_risk_level', side_effect=Exception('Test Exception')):
            data = {'user_id': '1'}
            response = self.client.post('/quiz_content', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_faqs_success(self):
        # Mock the faq_manager.get_faq and return_faqs methods
        with patch('entry.faq_manager.get_faq') as mock_get_faq, \
             patch('entry.return_faqs') as mock_return_faqs:

            mock_get_faq.return_value = ['FAQ 1', 'FAQ 2']
            mock_return_faqs.return_value = ['FAQ 1', 'FAQ 2']

            # Test the GET request
            response = self.client.get('/get_faqs')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('faqs', response.json)
            self.assertEqual(response.json['faqs'], ['FAQ 1', 'FAQ 2'])

    def test_get_faqs_exception(self):
        # Mock the faq_manager.get_faq method to raise an exception
        with patch('entry.faq_manager.get_faq', side_effect=Exception('Test Exception')):
            response = self.client.get('/get_faqs')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_get_finance_content_success(self):
        # Mock the generate_content method
        with patch('entry.generate_content') as mock_generate_content:
            mock_generate_content.return_value = ['Content 1', 'Content 2']

            # Test the POST request with valid risk_levels
            data = {'risk_levels': ['Low']}
            response = self.client.post('/finance_content', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('content', response.json)
            self.assertEqual(response.json['content'], ['Content 1', 'Content 2'])

    def test_get_finance_content_missing_risk_levels(self):
        # Test the POST request with missing risk_levels
        data = {}
        response = self.client.post('/finance_content', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('content', response.json)
        self.assertEqual(response.json['content'], {})

    def test_get_finance_content_exception(self):
        # Mock the generate_content method to raise an exception
        with patch('entry.generate_content', side_effect=Exception('Test Exception')):
            data = {'risk_levels': ['Low', 'Medium']}
            response = self.client.post('/finance_content', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

    def test_allocate_income_success(self):
        # Mock the ai_recommendations method
        with patch('entry.ai_recommendations') as mock_ai_recommendations:
            mock_ai_recommendations.return_value = {'investment': 1000, 'essentials': 2000, 'discretionary': 500}

            # Test the POST request with valid data
            data = {
                'total_income': '5000',
                'amount_invested': '1000',
                'amount_essentials': '2000',
                'amount_discretionary': '500',
                'risk_tolerance': 'Medium'
            }
            response = self.client.post('/income_allocation', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertIn('updated_data', response.json)
            self.assertEqual(response.json['updated_data'], {'investment': 1000, 'essentials': 2000, 'discretionary': 500})

    def test_allocate_income_missing_data(self):
        # Test the POST request with missing data
        data = {
            'total_income': '5000',
            'amount_invested': '1000'
            # Missing amount_essentials, amount_discretionary, and risk_tolerance
        }
        response = self.client.post('/income_allocation', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error') # Automatically assumes a risk level of medium, and sets values to 0
        self.assertNotIn('updated_data', response.json)

    def test_allocate_income_exception(self):
        # Mock the ai_recommendations method to raise an exception
        with patch('entry.ai_recommendations', side_effect=Exception('Test Exception')):
            data = {
                'total_income': '5000',
                'amount_invested': '1000',
                'amount_essentials': '2000',
                'amount_discretionary': '500',
                'risk_tolerance': 'Medium'
            }
            response = self.client.post('/income_allocation', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], 'Test Exception')

if __name__ == '__main__':
    unittest.main(verbosity=2)