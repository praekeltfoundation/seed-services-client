import responses

from seed_services_client import StageBasedMessagingApiClient
from unittest import TestCase


class TestStageBasedMessagingClientMessage(TestCase):

    def setUp(self):
        self.api = StageBasedMessagingApiClient(
            "token", "http://sbm.example.org/api/v1")

    @responses.activate
    def test_get_messages_one_page(self):
        # Setup
        response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "messageset": 1,
                    "sequence_number": 1,
                    "lang": "eng_ZA",
                    "text_content": "message 1 content",
                    "binary_content": None,
                    "created_at": "2016-09-23T14:12:09.876010Z",
                    "updated_at": "2016-09-23T14:12:09.876036Z"
                },
                {
                    "id": 2,
                    "messageset": 1,
                    "sequence_number": 1,
                    "lang": "eng_ZA",
                    "text_content": "message 2 content",
                    "binary_content": None,
                    "created_at": "2016-09-23T14:12:09.876010Z",
                    "updated_at": "2016-09-23T14:12:09.876036Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/message/",
                      json=response, status=200,
                      match_querystring=True)

        # Execute
        result = self.api.get_messages()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result1["text_content"], "message 1 content")
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result2["text_content"], "message 2 content")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_messages_multiple_pages(self):
        # Setup
        response = {
            "next": "http://sbm.example.org/api/v1/message/?cursor=1",
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "messageset": 1,
                    "sequence_number": 1,
                    "lang": "eng_ZA",
                    "text_content": "message 1 content",
                    "binary_content": None,
                    "created_at": "2016-09-23T14:12:09.876010Z",
                    "updated_at": "2016-09-23T14:12:09.876036Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/message/",
                      json=response, status=200,
                      match_querystring=True)
        response = {
            "next": None,
            "previous": "http://sbm.example.org/api/v1/message/?cursor=0",
            "results": [
                {
                    "id": 2,
                    "messageset": 1,
                    "sequence_number": 1,
                    "lang": "eng_ZA",
                    "text_content": "message 2 content",
                    "binary_content": None,
                    "created_at": "2016-09-23T14:12:09.876010Z",
                    "updated_at": "2016-09-23T14:12:09.876036Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/message/?cursor=1",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_messages()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result1["text_content"], "message 1 content")
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result2["text_content"], "message 2 content")
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_update_message(self):
        responses.add(responses.PATCH,
                      'http://sbm.example.org/api/v1/message/1/',
                      json={}, status=200, match_querystring=True)

        self.api.update_message(1, {'text_content': 'new content'})

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.method, 'PATCH')
        self.assertEqual(
            responses.calls[0].request.body,
            '{"text_content": "new content"}')
        self.assertEqual(
            responses.calls[0].request.url,
            'http://sbm.example.org/api/v1/message/1/')
