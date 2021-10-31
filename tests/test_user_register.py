import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    exclude_params = [
        ('no_password'),
        ('no_username'),
        ('no_first_name'),
        ('no_last_name'),
        ('no_email')
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)

        expected_response = 'Invalid email format'
        Assertions.assert_response_text(response, expected_response)

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_with_no_params(self, condition):
        global data
        global param

        if condition == 'no_password':
            param = 'password'

            data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        elif condition == 'no_username':
            param = 'username'

            data = {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        elif condition == 'no_first_name':
            param = 'firstName'

            data = {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        elif condition == 'no_last_name':
            param = 'lastName'

            data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        elif condition == 'no_email':
            param = 'email'

            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa'
        }

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        expected_response = f'The following required params are missed: {param}'
        Assertions.assert_response_text(response, expected_response)

    def test_create_user_with_too_short_name(self):

        first_name = 'l'

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': first_name,
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)

        expected_response = "The value of 'firstName' field is too short"
        Assertions.assert_response_text(response, expected_response)

    def test_create_user_with_too_long_name(self):
        first_name = 'toomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsymtoomuchsym1'

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': first_name,
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)

        expected_response = "The value of 'firstName' field is too long"
        Assertions.assert_response_text(response, expected_response)


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 400)

        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

