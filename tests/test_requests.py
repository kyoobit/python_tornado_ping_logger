import json

import tornado

from app import make_app


class TestApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_request(self):
        for path, options, status_code, payload in [
            # REQUEST: tuple = (path: str, options: dict, status_code: int, payload),
            ("/foo", {"method": "GET"}, 204, None),
            ("/bar", {"method": "GET"}, 204, None),
            ("/blast", {"method": "HEAD"}, 405, None),
            ("/blast", {"method": "OPTIONS"}, 405, None),
            ("/blast", {"method": "DELETE"}, 405, None),
            ("/ping", {"method": "GET"}, 200, b"Pong!\n"),
        ]:
            print(f"path: {path!r}, options: {options!r}, status_code: {status_code}")
            # Make the HTTP request
            response = self.fetch(f"{path}", **options)
            # Check response code for the expected value
            self.assertEqual(response.code, status_code)
            # Check response body for expected values
            if status_code == 200 and payload is not None:
                self.assertEqual(response.body, payload)

    def test_ping(self):
        for ping in [
            {"test": True}
        ]:
            # Make the HTTP request
            response = self.fetch("/ping", method='POST', body=json.dumps(ping))
            # Check response code for the expected value
            self.assertEqual(response.code, 204)
