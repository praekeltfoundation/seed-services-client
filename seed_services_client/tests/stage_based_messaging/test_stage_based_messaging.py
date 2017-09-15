from unittest import TestCase
import responses

from seed_services_client.stage_based_messaging \
    import StageBasedMessagingApiClient


class TestStageBasedMessagingClient(TestCase):

    def setUp(self):
        self.api = StageBasedMessagingApiClient(
            "NO", "http://sbm.example.org/api/v1")

    @responses.activate
    def test_get_schedules_one_page(self):
        # Setup
        response = {
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
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result1["day_of_week"], "1")
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result2["day_of_week"], "3")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/schedule/")

    @responses.activate
    def test_get_schedules_multiple_pages(self):
        # Setup
        response = {
            "next": "http://sbm.example.org/api/v1/schedule/?cursor=1",
            "previous": None,
            "results": [
                {
                    "id": 1, "minute": "0", "hour": "8", "day_of_week": "1",
                    "day_of_month": "*", "month_of_year": "*"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/schedule/",
                      json=response, status=200,
                      match_querystring=True)
        response = {
            "next": None,
            "previous": "http://sbm.example.org/api/v1/schedule/?cursor=0",
            "results": [
                {
                    "id": 2, "minute": "0", "hour": "8", "day_of_week": "3",
                    "day_of_month": "*", "month_of_year": "*"
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/schedule/?cursor=1",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_schedules()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result1["day_of_week"], "1")
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result2["day_of_week"], "3")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/schedule/")
        self.assertEqual(responses.calls[1].request.url,
                         "http://sbm.example.org/api/v1/schedule/?cursor=1")

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
    def test_list_messagesets_one_page(self):
        # Setup
        response = {
            "previous": None,
            "next": None,
            "results": [{
                'id': 1,
                'short_name': "short_name_1",
                'notes': None,
                'next_set': 10,
                'default_schedule': 1,
                'content_type': 'text',
                'created_at': "2016-06-22T06:13:29.693272Z",
                'updated_at': "2016-06-22T06:13:29.693272Z"
            }, {
                'id': 2,
                'short_name': "short_name_2",
                'notes': None,
                'next_set': 10,
                'default_schedule': 1,
                'content_type': 'text',
                'created_at': "2016-06-22T06:13:29.693272Z",
                'updated_at': "2016-06-22T06:13:29.693272Z"
            }]
        }
        responses.add(
            responses.GET,
            "http://sbm.example.org/api/v1/messageset/",
            json=response, status=200, match_querystring=True
        )
        # Execute
        result = self.api.get_messagesets()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result1["short_name"], "short_name_1")
        self.assertEqual(result2["short_name"], "short_name_2")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/messageset/")

    @responses.activate
    def test_list_messagesets_multiple_pages(self):
        # Setup
        response = {
            "previous": None,
            "next": "http://sbm.example.org/api/v1/messageset/?cursor=1",
            "results": [{
                'id': 1,
                'short_name': "short_name_1",
                'notes': None,
                'next_set': 10,
                'default_schedule': 1,
                'content_type': 'text',
                'created_at': "2016-06-22T06:13:29.693272Z",
                'updated_at': "2016-06-22T06:13:29.693272Z"
            }]
        }
        responses.add(
            responses.GET,
            "http://sbm.example.org/api/v1/messageset/",
            json=response, status=200, match_querystring=True
        )
        response = {
            "previous": "http://sbm.example.org/api/v1/messageset/cursor=0",
            "next": None,
            "results": [{
                'id': 2,
                'short_name': "short_name_2",
                'notes': None,
                'next_set': 10,
                'default_schedule': 1,
                'content_type': 'text',
                'created_at': "2016-06-22T06:13:29.693272Z",
                'updated_at': "2016-06-22T06:13:29.693272Z"
            }]
        }
        responses.add(
            responses.GET,
            "http://sbm.example.org/api/v1/messageset/?cursor=1",
            json=response, status=200, match_querystring=True
        )
        # Execute
        result = self.api.get_messagesets()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], 1)
        self.assertEqual(result2["id"], 2)
        self.assertEqual(result1["short_name"], "short_name_1")
        self.assertEqual(result2["short_name"], "short_name_2")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/messageset/")
        self.assertEqual(responses.calls[1].request.url,
                         "http://sbm.example.org/api/v1/messageset/?cursor=1")

    @responses.activate
    def test_messageset_languages(self):
        # Setup
        data = {
            "1": ["afr", "eng"],
            "2": ["afr", "eng", "zul"]
        }

        responses.add(
            responses.GET,
            "http://sbm.example.org/api/v1/messageset_languages/",
            json=data,
            status=200
        )

        # Execute
        result = self.api.get_messageset_languages()

        # Check
        self.assertEqual(result, data)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/messageset_languages/")

    @responses.activate
    def test_get_subscriptions_one_page(self):
        # Setup
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id_1 = "subscription1-4bf1-8779-c47b428e89d0"
        subscription_id_2 = "subscription2-4bf1-8779-c47b428e89d0"
        response = {
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
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], subscription_id_1)
        self.assertEqual(result1["active"], True)
        self.assertEqual(result2["id"], subscription_id_2)
        self.assertEqual(result2["active"], True)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_subscriptions_multiple_pages(self):
        # Setup
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id_1 = "subscription1-4bf1-8779-c47b428e89d0"
        subscription_id_2 = "subscription2-4bf1-8779-c47b428e89d0"
        response = {
            "next": "http://sbm.example.org/api/v1/subscriptions/?cursor=1",
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
                }
            ]
        }
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/subscriptions/",
                      json=response, status=200,
                      match_querystring=True)
        response = {
            "next": None,
            "previous": "http://sbm.example.org/api/v1/subscriptions/?"
                        "cursor=0",
            "results": [
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
                      "http://sbm.example.org/api/v1/subscriptions/?cursor=1",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_subscriptions()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], subscription_id_1)
        self.assertEqual(result1["active"], True)
        self.assertEqual(result2["id"], subscription_id_2)
        self.assertEqual(result2["active"], True)
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_get_subscription(self):
        # Setup
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id = "subscription1-4bf1-8779-c47b428e89d0"
        response = {
            "id": subscription_id,
            "identity": registrant_id,
            "active": True,
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
        responses.add(responses.GET,
                      "http://sbm.example.org/api/v1/subscriptions/%s/" % subscription_id,  # noqa
                      json=response, status=200)

        # Execute
        result = self.api.get_subscription(subscription_id)
        # Check
        self.assertEqual(result["id"], subscription_id)
        self.assertEqual(result["active"], True)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/subscriptions/%s/" % subscription_id)  # noqa

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

    @responses.activate
    def test_create_subscription(self):
        registrant_id = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        subscription_id = "subscription1-4bf1-8779-c47b428e89d0"
        response = {
            "id": subscription_id,
            "identity": registrant_id,
            "active": False,
            "completed": False,
            "lang": "eng_ZA",
            "url": "http://sbm/api/v1/subscriptions/%s" % subscription_id,
            "messageset": 1,
            "next_sequence_number": 1,
            "schedule": 101,
            "process_status": 0,
            "version": 1,
            "metadata": {},
            "created_at": "2015-07-10T06:13:29.693272Z",
            "updated_at": "2015-07-10T06:13:29.693272Z"
        }

        responses.add(responses.POST,
                      "http://sbm.example.org/api/v1/subscriptions/",
                      json=response, status=200)

        data = {
            "active": True,
            "identity": registrant_id,
            "completed": False,
            "lang": "eng_ZA",
            "messageset": 1,
            "next_sequence_number": 1,
            "schedule": 101,
            "process_status": 0,
        }
        # Execute
        result = self.api.create_subscription(data)
        # Check
        self.assertEqual(result["active"], False)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://sbm.example.org/api/v1/subscriptions/")
