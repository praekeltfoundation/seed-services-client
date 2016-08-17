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

    @responses.activate
    def test_create_user(self):
        # setup
        user_response = {
            "id": "3",
            "url": "http://auth.example.org/users/9/",
            "first_name": "First",
            "last_name": "Last",
            "email": "test@example.com",
            "admin": False,
            "teams": [],
            "organizations": [],
            "active": True
        }
        responses.add(responses.POST,
                      "http://auth.example.org/users/",
                      json=user_response, status=200)
        # Execute
        user = {
            "first_name": "First",
            "last_name": "Last",
            "email": "test@example.com",
            "password": "pass",
            "admin": False
        }
        result = self.api.create_user(user)
        # Check
        self.assertEqual(result["id"], "3")
        self.assertEqual(result["organizations"], [])
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://auth.example.org/users/")

        @responses.activate
        def test_get_teams(self):
            # setup
            teams_response = [{
                "id": "1",
                "title": "Operational Admins",
                "permissions": [{
                    "id": "1",
                    "type": "org:admins",
                    "object_id": "1",
                    "namespace": "__auth__"
                }, {
                    "id": "2",
                    "type": "ci:view",
                    "object_id": None,
                    "namespace": "__auth__"
                }],
                "users": [{
                    "id": "3",
                    "url": "http://auth.example.org/users/3/"
                }],
                "url": "http://auth.example.org/teams/1/",
                "organization": {
                    "id": "1",
                    "url": "http://auth.example.org/organizations/1/"
                },
                "archived": False
            }]
            responses.add(responses.GET,
                          "http://auth.example.org/teams/",
                          json=teams_response, status=200)
            # Execute
            result = self.api.get_teams()
            # Check
            self.assertEqual(len(result), 1)
            self.assertEqual(result["archived"], False)
            self.assertEqual(result["title"], "Operational Admins")
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(responses.calls[0].request.url,
                             "http://auth.example.org/teams/")

    @responses.activate
    def test_add_user_to_team(self):
        # setup
        responses.add(responses.PUT,
                      "http://auth.example.org/teams/2/users/3/", status=204)
        # Execute

        result = self.api.add_user_to_team(3, 2)
        # Check
        self.assertEqual(result, True)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://auth.example.org/teams/2/users/3/")
