from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic('Get user data cases')
class TestUserGet(BaseCase):

    @allure.description('This test checks getting user data without auth')
    @allure.feature('Negative tests for Get user data')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')

    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.description('This test checks successful getting user data being authorized')
    @allure.feature('Positive tests for Get user data')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(f'/user/{user_id_from_auth_method}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid}
                                 )
        expected_fields = ['username', 'email', 'firstName', 'lastName']

        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description('This test checks getting user data authorized under other')
    @allure.feature('Negative tests for Get user data')
    @allure.testcase('URL of test case', 'Name of link for test case')
    @allure.severity('Critical')

    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        Assertions.assert_code_status(response1, 200)

        other_user_id = '15858'
        response2 = MyRequests.get(f'/user/{other_user_id}')

        Assertions.assert_json_has_key(response2, 'username')

        excepted_fields = ['email', 'firstName', 'lastName']
        Assertions.assert_json_has_not_keys(response2, excepted_fields)










