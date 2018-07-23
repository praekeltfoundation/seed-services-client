from unittest import TestCase
import responses

from seed_services_client.hub import HubApiClient


class TestHubClient(TestCase):

    def setUp(self):
        self.api = HubApiClient("NO",
                                "http://hub.example.org/api/v1")

    @responses.activate
    def test_get_registrations_one_page(self):
        # setup
        search_response = {
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
        result1 = next(result["results"])
        self.assertEqual(result1["stage"], "prebirth")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/registrations/?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582")  # noqa

    @responses.activate
    def test_get_registrations_multiple_pages(self):
        # setup
        qs = "?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582"
        search_response = {
            "next": "http://hub.example.org/api/v1/registrations/%s&cursor=1"
                    % qs,
            "previous": None,
            "results": [
                {
                    "id": "reg-1-cf-abe8-4302-bd91-fd617e1c592e",
                    "stage": "prebirth",
                    "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
                    "validated": True,
                    "data": {
                        "last_period_date": "20160202",
                    },
                    "source": 1,
                    "created_at": "2016-08-03T19:39:26.464102Z",
                    "updated_at": "2016-08-03T19:39:26.464152Z",
                    "created_by": 1,
                    "updated_by": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/registrations/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://hub.example.org/api/v1/registrations/%s"
                        "&cursor=0" % qs,
            "results": [
                {
                    "id": "reg-2-cf-abe8-4302-bd91-fd617e1c592e",
                    "stage": "prebirth",
                    "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
                    "validated": True,
                    "data": {
                        "last_period_date": "20170202",
                    },
                    "source": 1,
                    "created_at": "2016-08-03T19:39:26.464102Z",
                    "updated_at": "2016-08-03T19:39:26.464152Z",
                    "created_by": 1,
                    "updated_by": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/registrations/%s&cursor=1"
                      % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_registrations(params={
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582"})
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "reg-1-cf-abe8-4302-bd91-fd617e1c592e")
        self.assertEqual(result2["id"], "reg-2-cf-abe8-4302-bd91-fd617e1c592e")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/registrations/?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://hub.example.org/api/v1/registrations/?mother_id=5cc97b85-c73c-46e3-8a14-df065727b582&cursor=1")  # noqa

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

    @responses.activate
    def test_update_registration(self):
        # setup
        uid = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        response = {
            "id": uid,
            "stage": "prebirth",
            "mother_id": "5cc97b85-c73c-46e3-8a14-df065727b582",
            "validated": True,
            "data": {
                "surname": "the builder",
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
        responses.add(responses.PATCH,
                      "http://hub.example.org/api/v1/registration/%s/" % uid,
                      json=response, status=200)
        # Execute
        registration = {
            "data": {
                "surname": "the builder",
            }
        }
        result = self.api.update_registration(uid, registration)
        # Check
        self.assertEqual(result["data"]['surname'], "the builder")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://hub.example.org/api/v1/registration/%s/" % uid)

    @responses.activate
    def test_get_changes_one_page(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
                    "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
                    "action": "change_messaging",
                    "data": {
                        "msg_type": "audio",
                        "voice_days": "tue_thu",
                        "voice_times": "9_11"
                    },
                    "source": 1
                }
            ]
        }
        qs = "?mother_id=846877e6-afaa-43de-acb1-09f61ad4de99"
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/changes/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_changes(params={
            "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99"})
        # Check
        result1 = next(result["results"])
        self.assertEqual(result1["action"], "change_messaging")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/changes/?mother_id=846877e6-afaa-43de-acb1-09f61ad4de99")  # noqa

    @responses.activate
    def test_get_changes_multiple_pages(self):
        # setup
        qs = "?mother_id=846877e6-afaa-43de-acb1-09f61ad4de99"
        search_response = {
            "next": "http://hub.example.org/api/v1/changes/%s&cursor=1" % qs,
            "previous": None,
            "results": [
                {
                    "id": "change-1-abe8-4302-bd91-fd617e1c592e",
                    "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
                    "action": "change_messaging",
                    "data": {
                        "msg_type": "audio",
                        "voice_days": "tue_thu",
                        "voice_times": "9_11"
                    },
                    "source": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/changes/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://hub.example.org/api/v1/changes/%s&cursor=0"
                        % qs,
            "results": [
                {
                    "id": "change-2-abe8-4302-bd91-fd617e1c592e",
                    "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
                    "action": "change_msisdn",
                    "data": {
                        "new_msisdn": "+23456789"
                    },
                    "source": 1
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/changes/%s&cursor=1" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_changes(params={
            "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99"})
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["action"], "change_messaging")
        self.assertEqual(result2["action"], "change_msisdn")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/changes/?mother_id=846877e6-afaa-43de-acb1-09f61ad4de99")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://hub.example.org/api/v1/changes/?mother_id=846877e6-afaa-43de-acb1-09f61ad4de99&cursor=1")  # noqa

    @responses.activate
    def test_get_change(self):
        # setup
        change_response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
            "action": "change_messaging",
            "data": {
                "msg_type": "audio",
                "voice_days": "tue_thu",
                "voice_times": "9_11"
            },
            "source": 1,
            "created_at": "2016-08-03T19:39:26.464102Z",
            "updated_at": "2016-08-03T19:39:26.464152Z",
            "created_by": 1,
            "updated_by": 1
        }
        reg = "7bfffecf-abe8-4302-bd91-fd617e1c592e"
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/changes/%s/" % reg,
                      json=change_response, status=200)
        # Execute
        result = self.api.get_change(
            "7bfffecf-abe8-4302-bd91-fd617e1c592e")
        # Check
        self.assertEqual(result["action"], "change_messaging")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://hub.example.org/api/v1/changes/7bfffecf-abe8-4302-bd91-fd617e1c592e/")  # noqa

    @responses.activate
    def test_create_change(self):
        # setup
        post_response = {
            "id": "7bfffecf-abe8-4302-bd91-fd617e1c592e",
            "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
            "action": "change_messaging",
            "data": {
                "msg_type": "audio",
                "voice_days": "tue_thu",
                "voice_times": "9_11"
            },
            "source": 1,
            "created_at": "2016-08-03T19:39:26.464102Z",
            "updated_at": "2016-08-03T19:39:26.464152Z",
            "created_by": 1,
            "updated_by": 1
        }
        responses.add(responses.POST,
                      "http://hub.example.org/api/v1/change/",
                      json=post_response, status=201)
        # Execute
        change = {
            "mother_id": "846877e6-afaa-43de-acb1-09f61ad4de99",
            "action": "change_messaging",
            "data": {
                "msg_type": "audio",
                "voice_days": "tue_thu",
                "voice_times": "9_11"
            }
        }
        result = self.api.create_change(change)
        # Check
        self.assertEqual(result["action"], "change_messaging")
        self.assertEqual(result["source"], 1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/change/")

    @responses.activate
    def test_trigger_report_generation(self):
        # setup
        post_response = {"report_generation_requested": True}
        responses.add(responses.POST,
                      "http://hub.example.org/api/v1/reports/",
                      json=post_response, status=202)
        # Execute
        data = {
            'output_file': "tempfile.name",
            'start_date': '2016:01:01',
            'end_date': '2016:02:01',
            'email_to': ['foo@example.com'],
            'email_subject': 'The Email Subject'
        }
        result = self.api.trigger_report_generation(data)
        # Check
        self.assertEqual(result, {"report_generation_requested": True})
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/reports/")

    @responses.activate
    def test_trigger_optout_admin(self):
        # Setup
        post_response = {"identity": "identity-1234"}
        responses.add(responses.POST,
                      "http://hub.example.org/api/v1/optout_admin/",
                      json=post_response, status=200)

        # Execute
        data = {
            "identity": "identity-1234"
        }

        result = self.api.create_optout_admin(data)

        # Check
        self.assertEqual(result, post_response)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/optout_admin/")

    @responses.activate
    def test_trigger_change_admin(self):
        # Setup
        post_response = {"identity": "identity-1234"}
        responses.add(responses.POST,
                      "http://hub.example.org/api/v1/change_admin/",
                      json=post_response, status=200)

        # Execute
        data = {
            "identity": "identity-1234",
            "subscription": "subscription-1234",
            "language": "eng_ZA"
        }

        result = self.api.create_change_admin(data)

        # Check
        self.assertEqual(result, post_response)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/change_admin/")

    @responses.activate
    def test_get_report_tasks_one_page(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    'status': 'Pending',
                    'end_date': '2016-02-01 00:00:00+00:00',
                    'created_at': '2017-08-16T09:35:15.940212Z',
                    'file_size': None,
                    'updated_at': '2017-08-16T09:35:15.940227Z',
                    'error': None,
                    'email_subject': 'The Email Subject',
                    'start_date': '2016-01-01 00:00:00+00:00'
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/reporttasks/",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_report_tasks()

        # Check
        result1 = next(result["results"])
        self.assertEqual(result1["status"], "Pending")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/reporttasks/")

    @responses.activate
    def test_get_report_tasks_multiple_pages(self):
        # setup
        search_response = {
            "next": "http://hub.example.org/api/v1/reporttasks/?cursor=1",
            "previous": None,
            "results": [
                {
                    'status': 'Pending',
                    'end_date': '2016-02-01 00:00:00+00:00',
                    'created_at': '2017-08-16T09:35:15.940212Z',
                    'file_size': None,
                    'updated_at': '2017-08-16T09:35:15.940227Z',
                    'error': None,
                    'email_subject': 'The Email Subject',
                    'start_date': '2016-01-01 00:00:00+00:00'
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/reporttasks/",
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://hub.example.org/api/v1/reporttasks/?cursor=0",
            "results": [
                {
                    'status': 'Completed',
                    'end_date': '2016-02-01 00:00:00+00:00',
                    'created_at': '2017-08-16T09:35:15.940212Z',
                    'file_size': None,
                    'updated_at': '2017-08-16T09:35:15.940227Z',
                    'error': None,
                    'email_subject': 'The Email Subject',
                    'start_date': '2016-01-01 00:00:00+00:00'
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/reporttasks/?cursor=1",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_report_tasks()

        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["status"], "Pending")
        self.assertEqual(result2["status"], "Completed")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                         "http://hub.example.org/api/v1/reporttasks/")
        self.assertEqual(responses.calls[1].request.url,
                         "http://hub.example.org/api/v1/reporttasks/?cursor=1")

    @responses.activate
    def test_get_user_details(self):
        # setup
        search_response = {
            "has_next": False,
            "has_previous": False,
            "results": [
                {
                    "identity_id": "316e8bf5-091e-430f-a8af-665ba5bc9692",
                    "msisdn": "+234123123123",
                    "receiver_role": "mother",
                    "validated": "true",
                    "created_at": "20/07/18 08:14",
                    "updated_at": "20/07/18 08:14",
                    "state": "Ebonyi",
                    "facility_name": "Chidera Health Clinic and Maternity",
                    "linked_to_id": "1c79b593-78bf-4dd3-bc99-cc4e179c880f",
                    "linked_to_msisdn": "+2347068430547",
                    "linked_to_receiver_role": "father",
                }
            ]
        }
        responses.add(responses.GET,
                      "http://hub.example.org/api/v1/user_details/",
                      json=search_response, status=200,
                      match_querystring=True)

        # Execute
        result = self.api.get_user_details()

        # Check
        self.assertEqual(result, search_response
        )
