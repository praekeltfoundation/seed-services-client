from unittest import TestCase
import responses

from seed_services_client.control_interface import ControlInterfaceApiClient


class TestControlInterfaceClient(TestCase):

    def setUp(self):
        self.api = ControlInterfaceApiClient("NO",
                                             "http://ci.example.org/api/v1")

    @responses.activate
    def test_get_user_service_tokens_one_page(self):
        # setup
        search_response = {
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
        result1 = next(result["results"], [])
        self.assertEqual(result1["user_id"], 1)
        self.assertEqual(result1["token"], "testtoken")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=t%40eg.org")  # noqa

    @responses.activate
    def test_get_user_service_tokens_multiple_pages(self):
        # setup
        qs = "?email=t%40eg.org"
        search_response = {
            "next": "http://ci.example.org/api/v1/userservicetoken/"
                    "%s&cursor=1" % qs,
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
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userservicetoken/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://ci.example.org/api/v1/userservicetoken/"
                        "%s&cursor=0" % qs,
            "results": [
                {
                    "user_id": 1,
                    "email": "t@eg.org",
                    "service": "Test Another Service",
                    "token": "testanothertoken",
                    "created_at": "2016-08-03T13:14:18.874925Z",
                    "updated_at": "2016-08-03T13:14:18.874953Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userservicetoken/"
                      "%s&cursor=1" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_user_service_tokens(params={"email": "t@eg.org"})
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["user_id"], 1)
        self.assertEqual(result1["token"], "testtoken")
        self.assertEqual(result2["user_id"], 1)
        self.assertEqual(result2["token"], "testanothertoken")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=t%40eg.org")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=t%40eg.org&cursor=1")  # noqa

    @responses.activate
    def test_get_user_service_tokens_no_results(self):
        # setup
        search_response = {
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
        self.assertEqual(len(list(result["results"])), 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://ci.example.org/api/v1/userservicetoken/?email=n%40eg.org")  # noqa

    @responses.activate
    def test_get_services_one_page(self):
        # setup
        services_response = {
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
        result1 = next(result["results"])
        self.assertEqual(result1["name"], "SEED_IDENTITY_STORE")
        self.assertEqual(result1["token"], "id_store_token")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/service/")

    @responses.activate
    def test_get_services_multiple_pages(self):
        # setup
        services_response = {
            "next": "http://ci.example.org/api/v1/service/?cursor=1",
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
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/service/",
                      json=services_response, status=200,
                      match_querystring=True)
        services_response = {
            "next": None,
            "previous": "http://ci.example.org/api/v1/service/?cursor=0",
            "results": [
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
                      "http://ci.example.org/api/v1/service/?cursor=1",
                      json=services_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_services()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["name"], "SEED_IDENTITY_STORE")
        self.assertEqual(result1["token"], "id_store_token")
        self.assertEqual(result2["name"], "SEED_STAGE_BASED_MESSAGING")
        self.assertEqual(result2["token"], "sbm_store_token")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/service/")
        self.assertEqual(responses.calls[1].request.url,
                         "http://ci.example.org/api/v1/service/?cursor=1")

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
    def test_get_service_status_one_page(self):
        # setup
        status_response = {
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
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["up"], True)
        self.assertEqual(result2["up"], False)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_service_status_multiple_pages(self):
        # setup
        qs = "?ordering=-created_at&service=serviceuuid"
        status_response = {
            "next": "http://ci.example.org/api/v1/status/%s&cursor=1" % qs,
            "previous": None,
            "results": [
                {
                    "id": "a01d97ee-669e-4a22-b4fd-8d0a81e57691",
                    "service": "SEED_IDENTITY_STORE",
                    "up": True,
                    "created_at": "2016-05-05T14:14:59.294611Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/status/%s" % qs,
                      json=status_response, status=200,
                      match_querystring=True)
        status_response = {
            "next": None,
            "previous": "http://ci.example.org/api/v1/status/%s&cursor=0" % qs,
            "results": [
                {
                    "id": "5d078cf1-c5ea-4e7a-a191-c54f79d4a59e",
                    "service": "SEED_IDENTITY_STORE",
                    "up": False,
                    "created_at": "2016-05-05T14:14:54.782284Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/status/%s&cursor=1" % qs,
                      json=status_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_service_status("serviceuuid")
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["up"], True)
        self.assertEqual(result2["up"], False)
        self.assertEqual(len(responses.calls), 2)

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
    def test_get_user_dashboards_single_page(self):
        # setup
        search_response = {
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
        result1 = next(result["results"])
        self.assertEqual(result1["user_id"], 1)
        self.assertEqual(result1["dashboards"][0]["id"], 1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/userdashboard/?user_id=1")  # noqa

    @responses.activate
    def test_get_user_dashboards_multiple_pages(self):
        # setup
        qs = "?user_id=1"
        search_response = {
            "next": "http://ci.example.org/api/v1/userdashboard/%s&cursor=1"
                    % qs,
            "previous": None,
            "results": [
                {
                    "user_id": 1,
                    "dashboards": [{
                        "id": 1,
                        "name": "Overview"
                    }],
                    "default_dashboard": {
                        "id": 1,
                        "name": "Overview"
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userdashboard/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://ci.example.org/api/v1/userdashboard/%s"
                        "&cursor=0" % qs,
            "results": [
                {
                    "user_id": 1,
                    "dashboards": [{
                        "id": 2,
                        "name": "Registrations"
                    }]
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/userdashboard/%s&cursor=1"
                      % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_user_dashboards(user_id=1)
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["user_id"], 1)
        self.assertEqual(result1["dashboards"][0]["id"], 1)
        self.assertEqual(result2["user_id"], 1)
        self.assertEqual(result2["dashboards"][0]["id"], 2)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/userdashboard/?user_id=1")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                         "http://ci.example.org/api/v1/userdashboard/?user_id=1&cursor=1")  # noqa

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

    @responses.activate
    def test_get_definition_page(self):
        # setup
        definition_page_response = {
            "id": 1,
            "title": "Overview",
            "description": "Overview_Description"
        }
        responses.add(responses.GET,
                      "http://ci.example.org/api/v1/definition/1/",
                      json=definition_page_response, status=200)
        # Execute
        result = self.api.get_definition_page(definition=1)
        # Check
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["title"], "Overview")
        self.assertEqual(result["description"], "Overview_Description")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci.example.org/api/v1/definition/1/")
