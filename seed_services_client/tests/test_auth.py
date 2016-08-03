from unittest import TestCase
import responses

from seed_services_client.auth import AuthApiClient


class TestAuthClient(TestCase):

    @responses.activate
    def setUp(self):
        # setup
        login_response = {
            "token": "3e6de6f2cace86d3ac22d0a58e652f4b283ab58c"
        }
        responses.add(responses.POST,
                      "http://auth.example.org/user/tokens/",
                      json=login_response, status=201)
        self.api = AuthApiClient("t@eg.org", "pass", "http://auth.example.org")

    @responses.activate
    def test_get_permissions(self):
        # setup
        user_response = {
            "id": "2",
            "url": "http://auth.example.org/users/2/",
            "first_name": "Test",
            "last_name": "User",
            "email": "t@eg.org",
            "admin": False,
            "active": True,
            "permissions": [
                {
                    "id": "1",
                    "type": "org:admin",
                    "object_id": "1",
                    "namespace": "__auth__"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://auth.example.org/user/",
                      json=user_response, status=200)
        # Execute
        result = self.api.get_permissions()
        # Check
        self.assertEqual(self.api.token,
                         "3e6de6f2cace86d3ac22d0a58e652f4b283ab58c")
        self.assertEqual(result["id"], "2")
        self.assertEqual(result["permissions"][0]["type"],
                         "org:admin")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://auth.example.org/user/")
