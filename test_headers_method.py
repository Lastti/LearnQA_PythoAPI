import requests

class TestHeadersMethod:
    def test_headers_method(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_header')

        assert response.status_code == 200, f'Wrong status code: {response.status_code}'

        print(response.headers)

        assert 'x-secret-homework-header' in response.headers, 'There is not Secret homework header in the response'

        expected_token = 'Some secret value'
        actual_token = response.headers.get('x-secret-homework-header')
        assert actual_token == expected_token, 'Actual header is nor correct'

