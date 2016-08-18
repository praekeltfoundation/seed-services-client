from unittest import TestCase
import responses

from seed_services_client.control_interface import ControlInterfaceApiClient


class TestControlInterfaceClient(TestCase):

    def setUp(self):
        self.api = ControlInterfaceApiClient("NO",
                                             "http://ci.example.org/api/v1")

    @responses.activate
    def test_get_user_service_tokens(self):
        # setup
        search_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "user_id": 1,
                    "email": "t@eg.org",
                    "service": "Test Service",
                    "token": "testtoken",
                    "created_at": "2016-08-03T13:14:18.874925Z",
                    "updated_at": "2016-08-03T13:14:18.874953Z"
                }
            ]
        }
        qs = "?email=t%40eg.org"
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userservicetoken/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_user_service_tokens(params={"email": "t@eg.org"})
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["user_id"], 1)
        self.assertEqual(result["results"][0]["token"], "testtoken")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=t%40eg.org")  # noqa

    @responses.activate
    def test_get_user_service_tokens_no_results(self):
        # setup
        search_response = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        qs = "?email=n%40eg.org"
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userservicetoken/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_user_service_tokens(params={"email": "n@eg.org"})
        # Check
        self.assertEqual(result["count"], 0)
        self.assertEqual(len(result["results"]), 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=n%40eg.org")  # noqa

    @responses.activate
    def test_get_services(self):
        # setup
        services_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "ba79f008-cc34-437e-ba6a-02b3c2e5fc9e",
                    "name": "SEED_IDENTITY_STORE",
                    "url": "http://id.seed.example.org",
                    "token": "id_store_token",
                    "up": True,
                    "metadata": None,
                    "created_at": "2016-05-05T14:06:33.250602Z",
                    "created_by": 1,
                    "updated_at": "2016-05-05T14:06:33.250630Z",
                    "updated_by": 1
                },
                {
                    "id": "df7f3f44-aed1-4e75-a1f9-b6398ef4760e",
                    "name": "SEED_STAGE_BASED_MESSAGING",
                    "url": "http://sbm.seed.example.org",
                    "token": "sbm_store_token",
                    "up": True,
                    "metadata": None,
                    "created_at": "2016-08-03T13:12:18.296637Z",
                    "created_by": 1,
                    "updated_at": "2016-08-03T13:12:18.296794Z",
                    "updated_by": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/service/",
                      json=services_response, status=200)
        # Execute
        result = self.api.get_services()
        # Check
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["name"], "SEED_IDENTITY_STORE")
        self.assertEqual(result["results"][0]["token"], "id_store_token")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/service/")

    @responses.activate
    def test_get_service(self):
        # setup
        service_response = {
            "id": "ba79f008-cc34-437e-ba6a-02b3c2e5fc9e",
            "name": "SEED_IDENTITY_STORE",
            "url": "http://id.seed.example.org",
            "token": "id_store_token",
            "up": True,
            "metadata": None,
            "created_at": "2016-05-05T14:06:33.250602Z",
            "created_by": 1,
            "updated_at": "2016-05-05T14:06:33.250630Z",
            "updated_by": 1
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/service/ba79f008-cc34-437e-ba6a-02b3c2e5fc9e/",  # noqa
                      json=service_response, status=200)
        # Execute
        result = self.api.get_service("ba79f008-cc34-437e-ba6a-02b3c2e5fc9e")
        # Check
        self.assertEqual(result["name"], "SEED_IDENTITY_STORE")
        self.assertEqual(result["token"], "id_store_token")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/service/ba79f008-cc34-437e-ba6a-02b3c2e5fc9e/")  # noqa

    @responses.activate
    def test_get_service_status(self):
        # setup
        status_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "a01d97ee-669e-4a22-b4fd-8d0a81e57691",
                    "service": "SEED_IDENTITY_STORE",
                    "up": True,
                    "created_at": "2016-05-05T14:14:59.294611Z"
                },
                {
                    "id": "5d078cf1-c5ea-4e7a-a191-c54f79d4a59e",
                    "service": "SEED_IDENTITY_STORE",
                    "up": False,
                    "created_at": "2016-05-05T14:14:54.782284Z"
                }
            ]
        }
        qs = "?ordering=-created_at&service=serviceuuid"
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/status/%s" % qs,
                      json=status_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_service_status("serviceuuid")
        # Check
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["up"], True)
        self.assertEqual(result["results"][1]["up"], False)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_generate_user_service_tokens(self):
        # setup
        ust_response = {
            "user_service_token_initiated": True,
            "count": 2
        }
        responses.add(responses.POST,
                      "http://ci.example.org/api/v1/userservicetoken/generate/",  # noqa
                      json=ust_response, status=201)
        # Execute
        user = {
            "user_id": 2,
            "email": "t@eg.org"
        }
        result = self.api.generate_user_service_tokens(user)
        # Check
        self.assertEqual(result["user_service_token_initiated"], True)
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/userservicetoken/generate/")  # noqa

    @responses.activate
    def test_get_user_dashboards(self):
        # setup
        search_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "user_id": 1,
                    "dashboards": [
                        {
                            "id": 1,
                            "name": "Overview"
                        }
                    ],
                    "default_dashboard": {
                        "id": 1,
                        "name": "Overview"
                    }
                }
            ]
        }
        qs = "?user_id=1"
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userdashboard/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_user_dashboards(user_id=1)
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["user_id"], 1)
        self.assertEqual(result["results"][0]["dashboards"][0]["id"], 1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/userdashboard/?user_id=1")  # noqa

    @responses.activate
    def test_get_dashboard(self):
        # setup
        dashboard_response = {
            "id": 1,
            "name": "Overview",
            "widgets": [
                {
                    "id": 1,
                    "title": "Unique Identities Created last 30 days",
                    "type_of": "last",
                    "data_from": "-30d",
                    "interval": "1d",
                    "nulls": "omit",
                    "data": [
                        {
                            "id": 1,
                            "title": "Identities Created",
                            "key": "identities.created.last",
                            "service": "identity store"
                        }
                    ]
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/dashboard/1/",
                      json=dashboard_response, status=200)
        # Execute
        result = self.api.get_dashboard(dashboard=1)
        # Check
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Overview")
        self.assertEqual(result["widgets"][0]["id"], 1)
        self.assertEqual(result["widgets"][0]["type_of"], "last")
        self.assertEqual(result["widgets"][0]["data"][0]["id"], 1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/dashboard/1/")
