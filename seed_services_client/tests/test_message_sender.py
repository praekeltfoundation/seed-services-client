from unittest import TestCase
import responses

from seed_services_client.message_sender \
    import MessageSenderApiClient


class TestMessageSenderClient(TestCase):

    def setUp(self):
        self.api = MessageSenderApiClient(
            "NO", "http://ms.example.org/api/v1")

    @responses.activate
    def test_create_outbound(self):
        # Setup
        outbound_payload = {
            "to_addr": "+27123",
            "content": "my outbound message",
            "metadata": {}
        }
        response = {
            'attempts': 0,
            'updated_at': '2016-08-18T11:32:17.750207Z',
            'content': outbound_payload["content"],
            'created_at': '2016-08-18T11:32:17.750236Z',
            'vumi_message_id': '075a32da-e1e4-4424-be46-1d09b71056fd',
            'to_addr': outbound_payload["to_addr"],
            'metadata': outbound_payload["metadata"],
            'id': 'c99bd21e-6b9d-48ba-9f07-1e8e406737fe',
            'delivered': False,
            'version': 1,
            'url': 'http://ms.example.org/api/v1/outbound/c99bd21e-6b9d-48ba-9f07-1e8e406737fe/'  # noqa
        }
        responses.add(
            responses.POST,
            "http://ms.example.org/api/v1/outbound/",
            json=response,
            status=200, content_type='application/json',
        )
        # Execute
        result = self.api.create_outbound(outbound_payload)
        # Check
        self.assertEqual(result["id"], "c99bd21e-6b9d-48ba-9f07-1e8e406737fe")
        self.assertEqual(result["content"], outbound_payload["content"])
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://ms.example.org/api/v1/outbound/")
