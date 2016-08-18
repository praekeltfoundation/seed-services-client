from unittest import TestCase
import responses

from seed_services_client.hub import HubApiClient


class TestHubClient(TestCase):

    def setUp(self):
        self.api = HubApiClient("NO",
                                "http://hub.example.org/api/v1")

    @responses.activate
    def test_get_registrations(self):
        # setup
        search_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
                    "stage": "prebirth",
                    "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
                    "validated": True,
                    "data": {
                        "hoh_surname": "the builder",
                        "last_period_date": "20160202",
                        "operator_id": "hcw00001-63e2-4acc-9b94-26663b9bc267",
                        "mama_name": "sue",
                        "mama_id_no": "12345",
                        "hoh_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                        "msg_type": "text",
                        "mama_surname": "zin",
                        "msg_receiver": "head_of_household",
                        "hoh_name": "bob",
                        "language": "eng_UG",
                        "mama_id_type": "ugandan_id",
                        "receiver_id": "hoh00001-63e2-4acc-9b94-26663b9bc267"
                    },
                    "source": 1,
                    "created_at": "2016-08-03T19:39:26.464102Z",
                    "updated_at": "2016-08-03T19:39:26.464152Z",
                    "created_by": 1,
                    "updated_by": 1
                }
            ]
        }
        qs = "?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582"
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/registrations/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_registrations(params={
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582"})
        # Check
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["stage"], "prebirth")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/registrations/?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582")  # noqa

    @responses.activate
    def test_get_registration(self):
        # setup
        reg_response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "stage": "prebirth",
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
            "validated": True,
            "data": {
                "hoh_surname": "the builder",
                "last_period_date": "20160202",
                "operator_id": "hcw00001-63e2-4acc-9b94-26663b9bc267",
                "mama_name": "sue",
                "mama_id_no": "12345",
                "hoh_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                "msg_type": "text",
                "mama_surname": "zin",
                "msg_receiver": "head_of_household",
                "hoh_name": "bob",
                "language": "eng_UG",
                "mama_id_type": "ugandan_id",
                "receiver_id": "hoh00001-63e2-4acc-9b94-26663b9bc267"
            },
            "source": 1,
            "created_at": "2016-08-03T19:39:26.464102Z",
            "updated_at": "2016-08-03T19:39:26.464152Z",
            "created_by": 1,
            "updated_by": 1
        }
        reg = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/registrations/%s/" % reg,
                      json=reg_response, status=200)
        # Execute
        result = self.api.get_registration(
            "7bfffecf-abe8-4302-bd91-fd617e1c592e")
        # Check
        self.assertEqual(result["stage"], "prebirth")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/registrations/7bfffecf-abe8-4302-bd91-fd617e1c592e/")  # noqa

    @responses.activate
    def test_create_registration(self):
        # setup
        post_response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "stage": "prebirth",
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
            "validated": True,
            "data": {
                "hoh_surname": "the builder",
                "last_period_date": "20160202",
                "operator_id": "hcw00001-63e2-4acc-9b94-26663b9bc267",
                "mama_name": "sue",
                "mama_id_no": "12345",
                "hoh_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                "msg_type": "text",
                "mama_surname": "zin",
                "msg_receiver": "head_of_household",
                "hoh_name": "bob",
                "language": "eng_UG",
                "mama_id_type": "ugandan_id",
                "receiver_id": "hoh00001-63e2-4acc-9b94-26663b9bc267"
            },
            "source": 1,
            "created_at": "2016-08-03T19:39:26.464102Z",
            "updated_at": "2016-08-03T19:39:26.464152Z",
            "created_by": 1,
            "updated_by": 1
        }
        responses.add(responses.POST,
                      "http://hub.example.org/api/v1/registration/",
                      json=post_response, status=201)
        # Execute
        registration = {
            "stage": "prebirth",
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
            "data": {
                "hoh_surname": "the builder",
                "last_period_date": "20160202",
                "operator_id": "hcw00001-63e2-4acc-9b94-26663b9bc267",
                "mama_name": "sue",
                "mama_id_no": "12345",
                "hoh_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                "msg_type": "text",
                "mama_surname": "zin",
                "msg_receiver": "head_of_household",
                "hoh_name": "bob",
                "language": "eng_UG",
                "mama_id_type": "ugandan_id",
                "receiver_id": "hoh00001-63e2-4acc-9b94-26663b9bc267"
            }
        }
        result = self.api.create_registration(registration)
        # Check
        self.assertEqual(result["stage"], "prebirth")
        self.assertEqual(result["source"], 1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/registration/")
