import requests
import time


response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
print(response.text)

parsed_response_text = response.json()

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params= {'token':parsed_response_text['token']})
print(response.text)

time.sleep(parsed_response_text['seconds'])

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params= {'token':parsed_response_text['token']})
print(response.text)