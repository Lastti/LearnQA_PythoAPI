from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_user_2(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, 'user_id')

        # DELETE
        response2 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    def test_delete_user_successfully(self):
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

        # DELETE
        response3 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response3, 200)

        # GET DATA
        response4 = MyRequests.get(f'/user/{user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_response_text(response4, 'User not found')

    def test_delete_user_auth_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # LOGIN AS OTHER
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        print(login_data)

        response3 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response3, 'auth_sid')
        token = self.get_header(response3, 'x-csrf-token')

        # DELETE
        response4 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response4, 400)

        # GET DATA FIRST USER
        response5 = MyRequests.get(f'/user/{user_id}')

        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, 'username')
