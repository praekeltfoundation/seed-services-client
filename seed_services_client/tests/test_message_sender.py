from unittest import TestCase
import json
import responses
import re

from seed_services_client.message_sender \
    import MessageSenderApiClient


class TestMessageSenderClient(TestCase):

    def setUp(self):
        self.api = MessageSenderApiClient(
            "NO", "http://ms.example.org/api/v1")

    @responses.activate
    def test_create_inbound(self):
        # Catch all requests
        responses.add(
            responses.POST, re.compile(r'.*'), json={'test': 'response'},
            status=200)

        inbound_payload = {
            'from_addr': '+1234'
        }

        response = self.api.create_inbound(inbound_payload)

        # Check
        self.assertEqual(response, {'test': 'response'})
        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.url, "http://ms.example.org/api/v1/inbound/")
        self.assertEqual(json.loads(request.body), inbound_payload)

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

    @responses.activate
    def test_get_outbounds_single_page(self):
        outbounds = {
            "next": None,
            "previous": None,
            "results": [
                {'to_addr': 'addr1', 'content': 'content1'},
                {'to_addr': 'addr2', 'content': 'content2'},
            ]
        }

        responses.add(
            responses.GET,
            "http://ms.example.org/api/v1/outbound/",
            json=outbounds,
            status=200, content_type='application/json',
        )
        # Execute
        result = self.api.get_outbounds()

        # Check
        self.assertEqual(list(result["results"]), [
            {'to_addr': 'addr1', 'content': 'content1'},
            {'to_addr': 'addr2', 'content': 'content2'}])
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://ms.example.org/api/v1/outbound/"
        )

    @responses.activate
    def test_get_outbounds_mulitple_pages(self):
        outbounds = {
            "next": "http://ms.example.org/api/v1/outbound/?cursor=1",
            "previous": None,
            "results": [
                {'to_addr': 'addr1', 'content': 'content1'},
                {'to_addr': 'addr2', 'content': 'content2'},
            ]
        }
        responses.add(
            responses.GET,
            "http://ms.example.org/api/v1/outbound/",
            json=outbounds,
            status=200, content_type='application/json', match_querystring=True
        )

        outbounds = {
            "next": None,
            "previous": "http://ms.example.org/api/v1/outbound/?cursor=0",
            "results": [
                {'to_addr': 'addr3', 'content': 'content3'},
            ]
        }
        responses.add(
            responses.GET,
            "http://ms.example.org/api/v1/outbound/?cursor=1",
            json=outbounds,
            status=200, content_type='application/json', match_querystring=True
        )
        # Execute
        result = self.api.get_outbounds()

        # Check
        self.assertEqual(list(result["results"]), [
            {'to_addr': 'addr1', 'content': 'content1'},
            {'to_addr': 'addr2', 'content': 'content2'},
            {'to_addr': 'addr3', 'content': 'content3'}])
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://ms.example.org/api/v1/outbound/"
        )
        self.assertEqual(
            responses.calls[1].request.url,
            "http://ms.example.org/api/v1/outbound/?cursor=1"
        )

    @responses.activate
    def test_get_inbounds_single_page(self):
        inbounds = {
            "next": None,
            "previous": None,
            "results": [
                {'from_addr': '+1234', 'content': 'content1'},
                {'from_addr': '+1234', 'content': 'content2'},
            ]
        }
        # Catch all requests
        responses.add(
            responses.GET, "http://ms.example.org/api/v1/inbound/",
            json=inbounds, status=200)

        # Execute
        response = self.api.get_inbounds({'from_addr': '+1234'})

        # Check
        self.assertEqual(list(response["results"]), [
            {'from_addr': '+1234', 'content': 'content1'},
            {'from_addr': '+1234', 'content': 'content2'}])
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.method, 'GET')
        self.assertEqual(
            responses.calls[0].request.url,
            "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234"
        )

    @responses.activate
    def test_get_inbounds_mulitple_pages(self):
        inbounds = {
            "next": "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234"
                    "&cursor=1",
            "previous": None,
            "results": [
                {'from_addr': '+1234', 'content': 'content1'},
                {'from_addr': '+1234', 'content': 'content2'},
            ]
        }
        # Catch all requests
        responses.add(
            responses.GET,
            "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234",
            json=inbounds, status=200, match_querystring=True)

        inbounds = {
            "next": None,
            "previous": "http://ms.example.org/api/v1/inbound/?"
                        "from_addr=%2B1234&cursor=1",
            "results": [
                {'from_addr': '+1234', 'content': 'content3'},
            ]
        }
        responses.add(
            responses.GET,
            "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234&cursor=1",
            json=inbounds, status=200, match_querystring=True)

        # Execute
        response = self.api.get_inbounds({'from_addr': '+1234'})

        # Check
        self.assertEqual(list(response["results"]), [
            {'from_addr': '+1234', 'content': 'content1'},
            {'from_addr': '+1234', 'content': 'content2'},
            {'from_addr': '+1234', 'content': 'content3'}])
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.method, 'GET')
        self.assertEqual(
            responses.calls[0].request.url,
            "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234"
        )
        self.assertEqual(responses.calls[1].request.method, 'GET')
        self.assertEqual(
            responses.calls[1].request.url,
            "http://ms.example.org/api/v1/inbound/?from_addr=%2B1234&cursor=1"
        )
