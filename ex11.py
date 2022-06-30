import requests


class TestCookies:
    def test_cookies(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(dict(response.cookies))
        assert "HomeWork" in response.cookies, "There is no 'HomeWork' in the response"
