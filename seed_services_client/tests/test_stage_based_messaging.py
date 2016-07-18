from unittest import TestCase
import responses

from seed_services_client.stage_based_messaging \
    import StageBasedMessagingApiClient


class TestIdentityStoreClient(TestCase):

    def setUp(self):
        self.api = StageBasedMessagingApiClient(
            "NO", "http://sbm.example.org/api/v1")

    @responses.activate
    def test_get_schedules(self):
        # setup
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

    
