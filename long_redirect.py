import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
print(response.history)
last_response = response.history[2]

print(last_response.url)