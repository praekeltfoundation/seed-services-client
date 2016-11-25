from unittest import TestCase
import responses

from seed_services_client.control_interface import ControlInterfaceApiClient


class TestControlInterfaceServiceClient(TestCase):

    def setUp(self):
        self.api = ControlInterfaceApiClient(
            "NO", "http://ci-service.example.org/api/v1")

    @responses.activate
    def test_get_definitions(self):
        # setup
        search_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "title": 'test title 1',
                    "description": "test desc 1",
                    "created_at": "2016-05-05T14:06:33.250602Z",
                    "created_by": 1,
                    "updated_at": "2016-05-05T14:06:33.250630Z",
                    "updated_by": 1
                },
                {
                    "title": 'test title 2',
                    "description": "test desc 2",
                    "created_at": "2016-05-05T14:06:33.250602Z",
                    "created_by": 1,
                    "updated_at": "2016-05-05T14:06:33.250630Z",
                    "updated_by": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://ci-service.example.org/api/v1/definition/",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_definitions()
        # Check
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["title"], 'test title 1')
        self.assertEqual(result["results"][0]["description"], "test desc 1")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci-service.example.org/api/v1/definition/")

    @responses.activate
    def test_get_definition(self):
        # setup
        definition_response = {
            "id": "ba79f008-cc34-437e-ba6a-02b3c2e5fc9e",
            "title": 'test title 1',
            "description": "test desc 1",
            "created_at": "2016-05-05T14:06:33.250602Z",
            "created_by": 1,
            "updated_at": "2016-05-05T14:06:33.250630Z",
            "updated_by": 1
        }
        responses.add(responses.GET,
                      "http://ci-service.example.org/api/v1/definition/ba79f008-cc34-437e-ba6a-02b3c2e5fc9e/",  # noqa
                      json=definition_response, status=200)
        # Execute
        result = self.api.get_definition("ba79f008-cc34-437e-ba6a-02b3c2e5fc9e")  # noqa
        # Check
        self.assertEqual(result["title"], "test title 1")
        self.assertEqual(result["description"], "test desc 1")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci-service.example.org/api/v1/definition/ba79f008-cc34-437e-ba6a-02b3c2e5fc9e/")  # noqa

    @responses.activate
    def test_update_definition(self):
        # Setup
        uid = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        response = {
            "id": uid,
            "title": 'updated title 1',
            "description": "test desc 1",
            "created_at": "2016-05-05T14:06:33.250602Z",
            "created_by": 1,
            "updated_at": "2016-05-05T14:06:33.250630Z",
            "updated_by": 1
        }
        responses.add(responses.PATCH,
                      "http://ci-service.example.org/api/v1/definition/%s/" % uid,  # noqa
                      json=response, status=200)
        data = {
            "title": "updated title 1"
        }
        # Execute
        result = self.api.update_definition(uid, data)

        # Check
        self.assertEqual(result["id"], uid)
        self.assertEqual(result["title"], "updated title 1")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ci-service.example.org/api/v1/definition/%s/" % uid)  # noqa

    @responses.activate
    def test_create_definition(self):
        # Setup
        definition = {
            "id": "4275a063-3129-45ac-853b-0d64aaefd8c5",
            "title": 'test title 1',
            "description": "test desc 1",
            "created_at": "2016-05-05T14:06:33.250602Z",
            "created_by": 1,
            "updated_at": "2016-05-05T14:06:33.250630Z",
            "updated_by": 1
        }
        responses.add(responses.POST,
                      "http://ci-service.example.org/api/v1/definition/",
                      json=definition, status=201)

        # Execute
        result = self.api.create_definition(definition)

        # Check
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(result["title"], "test title 1")
        self.assertEqual(result["description"], "test desc 1")
        self.assertEqual(
            responses.calls[0].request.url,
            "http://ci-service.example.org/api/v1/definition/")

    @responses.activate
    def test_delete_definition(self):
        definition_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": definition_id,
            "foo": "bar",
        }
        responses.add(
            responses.DELETE,
            "http://ci-service.example.org/api/v1/definition/%s/" % (
                definition_id,),
            json=response, status=201)
        # Execute
        result = self.api.delete_definition(definition_id)
        # Check
        self.assertEqual(result["success"], True)
        self.assertEqual(len(responses.calls), 1)
