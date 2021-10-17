import requests

response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response.text)

response2 = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response2.status_code, response2.text)

response3 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': 'GET'})
print(response3.text)

methods = ['POST', 'GET', 'PUT', 'DELETE']
for method in methods:
    for parameter in methods:
        payload = {'method': f'{parameter}'}
        if method == 'POST':
            response4 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=payload)
        elif method == 'PUT':
            response4 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=payload)
        elif method == 'DELETE':
            response4 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=payload)
        elif method == 'GET':
            response4 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=payload)
        print('method: ' + method, 'payload: ' + parameter, 'answer: ' + response4.text)
