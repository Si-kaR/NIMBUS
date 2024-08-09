import unittest
from entry import app 
from unittest.mock import patch

class RegisterUserTests(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()