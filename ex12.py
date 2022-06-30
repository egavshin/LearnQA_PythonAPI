import requests


class TestHeaders:
    def test_headers(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        assert "Date" in response.headers, "There is no 'Date' in headers"
        assert "Content-Type" in response.headers, "There is no 'Content-Type' in headers"
        assert "Content-Length" in response.headers, "There is no 'Content-Type' in headers"
        assert "Connection" in response.headers, "There is no 'Connection' in headers"
        assert "Keep-Alive" in response.headers, "There is no 'Keep-Alive' in headers"
        assert "Server" in response.headers, "There is no 'Server' in headers"
        assert "x-secret-homework-header" in response.headers, "There is no 'x-secret-homework-header' in headers"
        assert "Cache-Control" in response.headers, "There is no 'Cache-Control' in headers"
        assert "Expires" in response.headers, "There is no 'Expires' in headers"




