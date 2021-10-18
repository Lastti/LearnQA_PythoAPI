import requests
import time

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
print(response.text)
response = response.json()
seconds = response["seconds"]
token = response["token"]

payload = {"token": token}
response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job',params=payload)
response2 = response2.json()
status = response2["status"]
if status == 'Job is NOT ready':
    print('Status is correct. Job is NOT ready')
else:
    print('Wrong status. Job is ready')

time.sleep(seconds)

payload = {"token": token}
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job',params=payload)
response3 = response3.json()
result = response3["result"]
status = response3["status"]
if status == 'Job is ready' and result != '':
    print('Status is correct. Result received')
    print('Result:' + result)
else:
    print('Wrong status. Job is NOT ready')