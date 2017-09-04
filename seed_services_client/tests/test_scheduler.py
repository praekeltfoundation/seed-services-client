from unittest import TestCase
import responses

from seed_services_client.scheduler import SchedulerApiClient


class TestSchedulerApiClient(TestCase):

    def setUp(self):
        self.api = SchedulerApiClient("NO", "http://example.org/api/v1")

    @responses.activate
    def test_get_schedules(self):
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
                      "http://example.org/api/v1/schedule/?foo=bar",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_schedules(params={"foo": "bar"})
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["id"], "foo")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_schedule(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar"
        }
        schedule_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        responses.add(
            responses.GET,
            "http://example.org/api/v1/schedule/%s/" % (schedule_id,),
            json=response, status=200)

        # Execute
        result = self.api.get_schedule(
            "7bfffecf-abe8-4302-bd91-fd617e1c592e")
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_schedule(self):
        # setup
        response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "foo": "bar",
        }
        responses.add(responses.POST,
                      "http://example.org/api/v1/schedule/",
                      json=response, status=201)
        # Execute
        result = self.api.create_schedule({})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update_schedule(self):
        # setup
        schedule_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": schedule_id,
            "foo": "bar",
        }
        responses.add(
            responses.PATCH,
            "http://example.org/api/v1/schedule/%s/" % (
                schedule_id,),
            json=response, status=201)
        # Execute
        result = self.api.update_schedule(schedule_id, {})
        # Check
        self.assertEqual(result["foo"], "bar")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete_schedule(self):
        schedule_id = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {}
        responses.add(
            responses.DELETE,
            "http://example.org/api/v1/schedule/%s/" % (
                schedule_id,),
            json=response, status=204)
        # Execute
        result = self.api.delete_schedule(schedule_id)
        # Check
        self.assertEqual(result, {})
        self.assertEqual(len(responses.calls), 1)
