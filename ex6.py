import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')

for i in range(len(response.history)):
    print(response.history[i].url)

print(f"Итоговый URL {response.url}")
print(f"Количество редиректов {len(response.history)}")