from unittest import TestCase
import responses

from seed_services_client.stage_based_messaging \
    import StageBasedMessagingApiClient


class TestStageBasedMessagingClient(TestCase):

    def setUp(self):
        self.api = StageBasedMessagingApiClient(
            "NO", "http://sbm.example.org/api/v1")

    @responses.activate
    def test_get_schedules(self):
        # Setup
        response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1, "minute": "0", "hour": "8", "day_of_week": "1",
                    "day_of_month": "*", "month_of_year": "*"
                },
                {
                    "id": 2, "minute": "0", "hour": "8", "day_of_week": "3",
                    "day_of_month": "*", "month_of_year": "*"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/schedule/",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_schedules()
        # Check
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["id"], 1)
        self.assertEqual(result["results"][0]["day_of_week"], "1")
        self.assertEqual(result["results"][1]["id"], 2)
        self.assertEqual(result["results"][1]["day_of_week"], "3")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/schedule/")

    @responses.activate
    def test_get_schedule(self):
        # Setup
        sid = 1
        response = {
            "id": sid, "minute": "0", "hour": "8", "day_of_week": "1",
            "day_of_month": "*", "month_of_year": "*"
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/schedule/%s/" % sid,
                      json=response, status=200)
        # Execute
        result = self.api.get_schedule(sid)
        # Check
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["day_of_week"], "1")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/schedule/1/")

    @responses.activate
    def test_get_messageset(self):
        # Setup
        mid = 11
        messageset = {
            'id': mid,
            'short_name': "short_name",
            'notes': None,
            'next_set': 10,
            'default_schedule': 1,
            'content_type': 'text',
            'created_at': "2016-06-22T06:13:29.693272Z",
            'updated_at': "2016-06-22T06:13:29.693272Z"
        }
        responses.add(
            responses.GET,
            "http://sbm.example.org/api/v1/messageset/%s/" % mid,
            json=messageset, status=200
        )
        # Execute
        result = self.api.get_messageset(mid)
        # Check
        self.assertEqual(result["id"], 11)
        self.assertEqual(result["short_name"], "short_name")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/messageset/11/")

    @responses.activate
    def test_get_subscriptions(self):
        # Setup
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id_1 = "subscription1-4bf1-8779-c47b428e89d0"
        subscription_id_2 = "subscription2-4bf1-8779-c47b428e89d0"
        response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": subscription_id_1,
                    "identity": registrant_id,
                    "active": True,
                    "completed": False,
                    "lang": "eng_ZA",
                    "url": "http://sbm/api/v1/subscriptions/%s" % (
                        subscription_id_1),
                    "messageset": 11,
                    "next_sequence_number": 11,
                    "schedule": 101,
                    "process_status": 0,
                    "version": 1,
                    "metadata": {},
                    "created_at": "2015-07-10T06:13:29.693272Z",
                    "updated_at": "2015-07-10T06:13:29.693272Z"
                },
                {
                    "id": subscription_id_2,
                    "identity": registrant_id,
                    "active": True,
                    "completed": False,
                    "lang": "eng_ZA",
                    "url": "http://sbm/api/v1/subscriptions/%s" % (
                        subscription_id_2),
                    "messageset": 21,
                    "next_sequence_number": 21,
                    "schedule": 121,
                    "process_status": 0,
                    "version": 1,
                    "metadata": {},
                    "created_at": "2015-07-10T06:13:29.693272Z",
                    "updated_at": "2015-07-10T06:13:29.693272Z"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/subscriptions/",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_subscriptions()
        # Check
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["id"], subscription_id_1)
        self.assertEqual(result["results"][0]["active"], True)
        self.assertEqual(result["results"][1]["id"], subscription_id_2)
        self.assertEqual(result["results"][1]["active"], True)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update_subscription(self):
        # Setup
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id = "subscription1-4bf1-8779-c47b428e89d0"
        response = {
            "id": subscription_id,
            "identity": registrant_id,
            "active": False,
            "completed": False,
            "lang": "eng_ZA",
            "url": "http://sbm/api/v1/subscriptions/%s" % subscription_id,
            "messageset": 11,
            "next_sequence_number": 11,
            "schedule": 101,
            "process_status": 0,
            "version": 1,
            "metadata": {},
            "created_at": "2015-07-10T06:13:29.693272Z",
            "updated_at": "2015-07-10T06:13:29.693272Z"
        }
        responses.add(responses.PATCH,
                      "http://sbm.example.org/api/v1/subscriptions/%s/" % subscription_id,  # noqa
                      json=response, status=200)
        data = {
            "active": False
        }
        # Execute
        result = self.api.update_subscription(subscription_id, data)
        # Check
        self.assertEqual(result["id"], subscription_id)
        self.assertEqual(result["active"], False)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/subscriptions/%s/" % subscription_id)  # noqa
