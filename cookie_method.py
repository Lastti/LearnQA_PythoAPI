import requests

class TestCookieMethod:

    def test_get_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')

        assert response.status_code == 200, f'Wrong status code: {response.status_code}'

        print(response.cookies)
        assert 'HomeWork' in response.cookies, 'There is no "HomeWork" cookie in the response'

        expected_cookie = 'hw_value'
        cookie = response.cookies.get('HomeWork')
        assert cookie ==  expected_cookie, f'Actual cookie in the response is not correct'

