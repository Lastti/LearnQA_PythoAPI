from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic('User creation cases')
class TestUserEdit(BaseCase):

    @allure.description('This test successfully edit user')
    @allure.feature('Positive tests for Creation')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        print(login_data, user_id)

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = 'Changed name'

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    @allure.description('This test the impossibility of editing a user without auth')
    @allure.feature('Negative tests for Creation')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')
    def test_user_edit_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = 'Changed name'

        response2 = MyRequests.put(
            f'/user/{user_id}',
            headers=None,
            cookies=None,
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, 'Auth token not supplied')

    @allure.description('This test checks the impossibility of editing user being authorized under another')
    @allure.feature('Negative tests for Creation')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')
    def test_user_edit_auth_as_other_user(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email_of_new_user = register_data['email']
        password_of_new_user = register_data['password']
        username_of_new_user = register_data['username']
        user_id_of_new_user = self.get_json_value(response1, 'id')

        username_before_edit = username_of_new_user

        # LOGIN AS OTHER USER
        login_data = {
             'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid_from_auth_user = self.get_cookie(response2, 'auth_sid')
        token_from_auth_user = self.get_header(response2, 'x-csrf-token')

        # EDIT USER AUTH BY OTHER
        new_name = 'Changed name'

        response3 = MyRequests.put(
            f'/user/{user_id_of_new_user}',
            headers={'x-csrf-token': token_from_auth_user},
            cookies={'auth_sid': auth_sid_from_auth_user},
            data={'username': new_name}
        )

        Assertions.assert_code_status(response3,400)

        # LOGIN AS NEW USER
        login_data = {
            'email': email_of_new_user,
            'password': password_of_new_user
        }

        response4 = MyRequests.post('/user/login', data=login_data)
        user_id_of_new_user = self.get_json_value(response4, 'user_id')

        # GET DATA NEW USER
        response5 = MyRequests.get(f'/user/{user_id_of_new_user}')

        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(
            response5,
            'username',
            username_before_edit,
            'Wrong name of the user after edit'
        )

    @allure.description('This test checks the impossibility of editing user email for an invalid value')
    @allure.feature('Negative tests for Creation')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')
    def test_user_edit_to_wrong_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        print(login_data, user_id)

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_email = 'vinkotovexample.com'

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'email': new_email}
        )

        print(response3.status_code)
        print(response3.text)

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, 'Invalid email format')

    @allure.description('This test checks the impossibility of editing first name for too short value')
    @allure.feature('Negative tests for Creation')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')
    def test_user_edit_to_short_first_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        print(login_data, user_id)

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_first_name = 'v'

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_first_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, 'error')
