from unittest import TestCase
import responses

from seed_services_client.service_rating import ServiceRatingApiClient


class TestServiceRatingApiClient(TestCase):

    def setUp(self):
        self.api = ServiceRatingApiClient("NO", "http://example.org/api/v1")

    # Invite testing
    @responses.activate
    def test_get_invites(self):
        # setup
        search_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "foo",
                    "key": "bar",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/invite/?foo=bar",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_invites(params={"foo": "bar"})
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["id"], "foo")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_invite(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar"
        }
        invite_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        responses.add(
            responses.GET,
            "http://example.org/api/v1/invite/%s/" % invite_id,
            json=response, status=200)

        # Execute
        result = self.api.get_invite(
            "7bfffecf-abe8-4302-bd91-fd617e1c592e")
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_invite(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar",
        }
        responses.add(responses.POST,
                      "http://example.org/api/v1/invite/",
                      json=response, status=201)
        # Execute
        result = self.api.create_invite({})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update_invite(self):
        # setup
        invite_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": invite_id,
            "foo": "bar",
        }
        responses.add(
            responses.PATCH,
            "http://example.org/api/v1/invite/%s/" % (
                invite_id,),
            json=response, status=201)
        # Execute
        result = self.api.update_invite(invite_id, {})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete_invite(self):
        invite_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": invite_id,
            "foo": "bar",
        }
        responses.add(
            responses.DELETE,
            "http://example.org/api/v1/invite/%s/" % (
                invite_id,),
            json=response, status=201)
        # Execute
        result = self.api.delete_invite(invite_id)
        # Check
        self.assertEqual(result["success"], True)
        self.assertEqual(len(responses.calls), 1)

    # Rating testing
    @responses.activate
    def test_get_ratings(self):
        # setup
        search_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "foo",
                    "key": "bar",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/rating/?foo=bar",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_ratings(params={"foo": "bar"})
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["id"], "foo")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_rating(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar"
        }
        rating_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        responses.add(
            responses.GET,
            "http://example.org/api/v1/rating/%s/" % rating_id,
            json=response, status=200)

        # Execute
        result = self.api.get_rating(
            "7bfffecf-abe8-4302-bd91-fd617e1c592e")
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_rating(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar",
        }
        responses.add(responses.POST,
                      "http://example.org/api/v1/rating/",
                      json=response, status=201)
        # Execute
        result = self.api.create_rating({})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update_rating(self):
        # setup
        rating_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": rating_id,
            "foo": "bar",
        }
        responses.add(
            responses.PATCH,
            "http://example.org/api/v1/rating/%s/" % (
                rating_id,),
            json=response, status=201)
        # Execute
        result = self.api.update_rating(rating_id, {})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete_rating(self):
        rating_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": rating_id,
            "foo": "bar",
        }
        responses.add(
            responses.DELETE,
            "http://example.org/api/v1/rating/%s/" % (
                rating_id,),
            json=response, status=201)
        # Execute
        result = self.api.delete_rating(rating_id)
        # Check
        self.assertEqual(result["success"], True)
        self.assertEqual(len(responses.calls), 1)
