from unittest import TestCase
import responses

from seed_services_client.service_rating import ServiceRatingApiClient


class TestServiceRatingApiClient(TestCase):

    def setUp(self):
        self.api = ServiceRatingApiClient("NO", "http://example.org/api/v1")

    # Invite testing
    @responses.activate
    def test_get_invites_single_page(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "foo_1",
                    "key": "bar_1",
                },
                {
                    "id": "foo_2",
                    "key": "bar_2",
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
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "foo_1")
        self.assertEqual(result1["key"], "bar_1")
        self.assertEqual(result2["id"], "foo_2")
        self.assertEqual(result2["key"], "bar_2")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://example.org/api/v1/invite/?foo=bar")

    @responses.activate
    def test_get_invites_multiple_pages(self):
        # setup
        search_response = {
            "next": "http://example.org/api/v1/invite/?foo=bar&cursor=1",
            "previous": None,
            "results": [
                {
                    "id": "foo_1",
                    "key": "bar_1",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/invite/?foo=bar",
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://example.org/api/v1/invite/?foo=bar&cursor=0",
            "results": [
                {
                    "id": "foo_2",
                    "key": "bar_2",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/invite/?foo=bar&cursor=1",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_invites(params={"foo": "bar"})
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "foo_1")
        self.assertEqual(result1["key"], "bar_1")
        self.assertEqual(result2["id"], "foo_2")
        self.assertEqual(result2["key"], "bar_2")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://example.org/api/v1/invite/?foo=bar")
        self.assertEqual(responses.calls[1].request.url,
                         "http://example.org/api/v1/invite/?foo=bar&cursor=1")

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
    def test_get_ratings_single_page(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "foo_1",
                    "key": "bar_1",
                },
                {
                    "id": "foo_2",
                    "key": "bar_2",
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
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "foo_1")
        self.assertEqual(result1["key"], "bar_1")
        self.assertEqual(result2["id"], "foo_2")
        self.assertEqual(result2["key"], "bar_2")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://example.org/api/v1/rating/?foo=bar")

    @responses.activate
    def test_get_ratings_multiple_pages(self):
        # setup
        search_response = {
            "next": "http://example.org/api/v1/rating/?foo=bar&cursor=1",
            "previous": None,
            "results": [
                {
                    "id": "foo_1",
                    "key": "bar_1",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/rating/?foo=bar",
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://example.org/api/v1/rating/?foo=bar&cursor=0",
            "results": [
                {
                    "id": "foo_2",
                    "key": "bar_2",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://example.org/api/v1/rating/?foo=bar&cursor=1",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_ratings(params={"foo": "bar"})
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "foo_1")
        self.assertEqual(result1["key"], "bar_1")
        self.assertEqual(result2["id"], "foo_2")
        self.assertEqual(result2["key"], "bar_2")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://example.org/api/v1/rating/?foo=bar")
        self.assertEqual(responses.calls[1].request.url,
                         "http://example.org/api/v1/rating/?foo=bar&cursor=1")

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
