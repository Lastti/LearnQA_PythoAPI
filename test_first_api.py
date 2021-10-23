import pytest
import requests

class TestFirstApi:
    names = [
        ('Anya'),
        ('Alex'),
        ('')
    ]
    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = 'https://playground.learnqa.ru/api/hello'
        data = {'name': name}

        response = requests.get(url, params=data)
        assert response.status_code == 200, f'Wrong response code'

        response_dict = response.json()
        assert 'answer' in response_dict, f'There is no field "answer" in the response'

        if len(name) == 0:
            expected_response_text = 'Hello, someone'
        else:
            expected_response_text = f'Hello, {name}'

        actual_response = response_dict['answer']

        assert actual_response == expected_response_text, f'Actual text in the response is not correct'



