from mock import patch
from unittest import TestCase
import responses

from seed_services_client.identity_store import IdentityStoreApiClient
from seed_services_client.seed_services import SeedServicesApiClient


class TestIdentityStoreClient(TestCase):

    def setUp(self):
        self.api = IdentityStoreApiClient("NO", "http://id.example.org/api/v1")

    @patch("seed_services_client.seed_services.SeedServicesApiClient.__init__")
    def test_inherited_from_base_api_class(self, mock_parent_init):
        self.assertTrue(
            issubclass(IdentityStoreApiClient, SeedServicesApiClient))

        IdentityStoreApiClient(
            'token', 'http://api/', session='session', argument=True)
        mock_parent_init.assert_called_with(
            'token', 'http://api/', session='session', argument=True)

    @responses.activate
    def test_identity_search_one_page(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "0c03d360-1180-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        qs = "?details__addresses__msisdn=%2B27001"
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity_by_address(address_type="msisdn",
                                                  address_value="+27001")
        # Check
        result1 = next(result["results"])
        self.assertEqual(result1["id"], "0c03d360-1180-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__addresses__msisdn=%2B27001")  # noqa

    @responses.activate
    def test_identity_search_multiple_pages(self):
        # setup
        qs = "?details__addresses__msisdn=%2B27001"
        search_response = {
            "next": "http://id.example.org/api/v1/identities/search/%s&"
                    "cursor=1" % qs,
            "previous": None,
            "results": [
                {
                    "id": "identity-1-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://id.example.org/api/v1/identities/search/%s&"
                        "cursor=0" % qs,
            "results": [
                {
                    "id": "identity-2-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s&"
                      "cursor=1" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity_by_address(address_type="msisdn",
                                                  address_value="+27001")
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "identity-1-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(result2["id"], "identity-2-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__addresses__msisdn=%2B27001")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__addresses__msisdn=%2B27001&cursor=1")  # noqa

    @responses.activate
    def test_details_search(self):
        # setup
        qs = "?details__preferred_language=eng_ZA"
        search_response = {
            "next": "http://id.example.org/api/v1/identities/search/%s&"
                    "cursor=1" % qs,
            "previous": None,
            "results": [
                {
                    "id": "identity-1-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "preferred_language": "eng_ZA",
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://id.example.org/api/v1/identities/search/%s&"
                        "cursor=0" % qs,
            "results": [
                {
                    "id": "identity-2-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "preferred_language": "eng_ZA",
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s&"
                      "cursor=1" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.search_identities("details__preferred_language",
                                            "eng_ZA")
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "identity-1-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(result2["id"], "identity-2-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__preferred_language=eng_ZA")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__preferred_language=eng_ZA&cursor=1")  # noqa

    @responses.activate
    def test_identity_search_no_results(self):
        # setup
        search_response = {
            "next": None,
            "previous": None,
            "results": []
        }
        qs = "?details__addresses__msisdn=%2B27002"
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/search/%s" % qs,
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity_by_address(address_type="msisdn",
                                                  address_value="+27002")
        # Check
        self.assertEqual(len(list(result["results"])), 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                        "http://id.example.org/api/v1/identities/search/?details__addresses__msisdn=%2B27002")  # noqa

    @responses.activate
    def test_get_identity_none(self):
        # setup
        four_oh_four = {
            "detail": "Not found."
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/uuid/",
                      json=four_oh_four, status=404,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity(identity="uuid")
        # Check
        self.assertEqual(result, None)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://id.example.org/api/v1/identities/uuid/")

    @responses.activate
    def test_get_identity_found(self):
        # setup
        identity = {
            "id": "4275a063-3129-45ac-853b-0d64aaefd8c5",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+26773000000": {}
                    }
                }
            },
            "communicate_through": None,
            "operator": None,
            "created_at": "2016-04-21T09:11:05.725680Z",
            "created_by": 2,
            "updated_at": "2016-06-15T15:09:05.333526Z",
            "updated_by": 2
        }
        uid = identity["id"]
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/%s/" % uid,
                      json=identity, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity(identity=uid)
        # Check
        self.assertEqual(result["id"], uid)
        self.assertEqual(result["version"], 1)
        self.assertEqual(result["details"]["default_addr_type"], "msisdn")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://id.example.org/api/v1/identities/%s/" % uid)

    @responses.activate
    def test_get_identity_address(self):
        # Setup
        uid = 'uid'
        url = ('http://id.example.org/api/v1/identities/{0}'
               '/addresses/msisdn?default=True').format(uid)
        addresses_msisdn_response = {'results': [
            {'address': '+27000000000'},
            {'address': '+27000000001'},
        ]}
        responses.add(responses.GET, url,
                      json=addresses_msisdn_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity_address(identity_id=uid)
        # Check
        self.assertEqual(result, '+27000000000')

    @responses.activate
    def test_get_identity_address_no_results(self):
        # Setup
        uid = 'uid'
        url = ('http://id.example.org/api/v1/identities/{0}'
               '/addresses/msisdn?default=True').format(uid)
        addresses_msisdn_response = {'results': []}
        responses.add(responses.GET, url,
                      json=addresses_msisdn_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identity_address(identity_id=uid)
        # Check
        self.assertEqual(result, None)

    @responses.activate
    def test_get_identity_address_custom_params(self):
        # Setup
        uid = 'uid'
        url = ('http://id.example.org/api/v1/identities/{0}'
               '/addresses/msisdn?param_one=set').format(uid)
        addresses_msisdn_response = {'results': []}
        responses.add(responses.GET, url,
                      json=addresses_msisdn_response, status=200,
                      match_querystring=True)
        # Execute
        self.api.get_identity_address(identity_id=uid,
                                      params={'param_one': 'set'})
        # This test doesn't assert anything, but responses will raise a
        # ConnectionError if the params don't match

    @responses.activate
    def test_identity_list_no_results(self):
        # setup
        response = {
            "next": None,
            "previous": None,
            "results": []
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identities()
        # Check
        self.assertEqual(len(list(result["results"])), 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://id.example.org/api/v1/identities/")

    @responses.activate
    def test_identity_list_one_results(self):
        # setup
        response = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "4275a063-3129-45ac-853b-0d64aaefd8c5",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                            "msisdn": {
                                "+26773000000": {}
                            }
                        }
                    },
                    "communicate_through": None,
                    "operator": None,
                    "created_at": "2016-04-21T09:11:05.725680Z",
                    "created_by": 2,
                    "updated_at": "2016-06-15T15:09:05.333526Z",
                    "updated_by": 2
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/",
                      json=response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identities()
        # Check
        result1 = next(result["results"])
        self.assertEqual(result1["version"], 1)
        self.assertEqual(result1["details"]["default_addr_type"], "msisdn")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://id.example.org/api/v1/identities/")

    @responses.activate
    def test_identity_list_multiple_pages(self):
        # setup
        search_response = {
            "next": "http://id.example.org/api/v1/identities/?cursor=1",
            "previous": None,
            "results": [
                {
                    "id": "identity-1-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/",
                      json=search_response, status=200,
                      match_querystring=True)
        search_response = {
            "next": None,
            "previous": "http://id.example.org/api/v1/identities/?cursor=0",
            "results": [
                {
                    "id": "identity-2-80-4fb4-9eed-ecd2cff8fa05",
                    "version": 1,
                    "details": {
                        "default_addr_type": "msisdn",
                        "addresses": {
                          "msisdn": {
                              "+27123": {}
                          }
                        }
                    }
                }
            ]
        }
        responses.add(responses.GET,
                      "http://id.example.org/api/v1/identities/?cursor=1",
                      json=search_response, status=200,
                      match_querystring=True)
        # Execute
        result = self.api.get_identities()
        # Check
        result1 = next(result["results"])
        result2 = next(result["results"])
        self.assertEqual(result1["id"], "identity-1-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(result2["id"], "identity-2-80-4fb4-9eed-ecd2cff8fa05")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url,
                        "http://id.example.org/api/v1/identities/")  # noqa
        self.assertEqual(responses.calls[1].request.url,
                        "http://id.example.org/api/v1/identities/?cursor=1")  # noqa

    @responses.activate
    def test_update_identity_details(self):
        # Setup
        uid = "4275a063-3129-45ac-853b-0d64aaefd8c5"
        response = {
            "id": uid,
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+26773000000": {}
                    }
                },
                "risk": "high"
            },
            "communicate_through": None,
            "operator": None,
            "created_at": "2016-04-21T09:11:05.725680Z",
            "created_by": 2,
            "updated_at": "2016-06-15T15:09:05.333526Z",
            "updated_by": 2
        }
        responses.add(responses.PATCH,
                      "http://id.example.org/api/v1/identities/%s/" % uid,
                      json=response, status=200)
        data = {
            "details": {
                "risk": "high"
            }
        }
        # Execute
        result = self.api.update_identity(uid, data)
        # Check
        self.assertEqual(result["id"], uid)
        self.assertEqual(result["version"], 1)
        self.assertEqual(result["details"]["default_addr_type"], "msisdn")
        self.assertEqual(result["details"]["risk"], "high")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         "http://id.example.org/api/v1/identities/%s/" % uid)

    @responses.activate
    def test_create_identity(self):
        # Setup
        identity = {
            "id": "4275a063-3129-45ac-853b-0d64aaefd8c5",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+26773000000": {}
                    }
                },
                "risk": "high"
            },
            "communicate_through": None,
            "operator": None,
            "created_at": "2016-04-21T09:11:05.725680Z",
            "created_by": 2,
            "updated_at": "2016-06-15T15:09:05.333526Z",
            "updated_by": 2
        }
        responses.add(responses.POST,
                      "http://id.example.org/api/v1/identities/",
                      json=identity, status=201)

        # Execute
        self.api.create_identity(identity)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://id.example.org/api/v1/identities/")

    @responses.activate
    def test_get_optouts_one_page(self):
        optouts = {
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "e5210c99-8d8a-40f1-8e7f-8a66c4de9e29",
                    "optout_type": "stop",
                    "identity": "8311c23d-f3c4-4cab-9e20-5208d77dcd1b",
                    "address_type": "msisdn",
                    "address": "+1234",
                    "request_source": "testsource",
                    "requestor_source_id": "1",
                    "reason": "Test reason",
                    "created_at": "2017-01-27T10:00:06.354178Z"
                },
            ]
        }
        responses.add(
            responses.GET,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop",
            json=optouts, match_querystring=True)

        res = self.api.get_optouts(params={'optout_type': 'stop'})
        result1 = next(res["results"])
        self.assertEqual(result1['id'], "e5210c99-8d8a-40f1-8e7f-8a66c4de9e29")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop"
        )

    @responses.activate
    def test_get_optouts_multiple_pages(self):
        optouts = {
            "next": "http://id.example.org/api/v1/optouts/search/?"
                    "optout_type=stop&cursor=1",
            "previous": None,
            "results": [
                {
                    "id": "optout-1-8d8a-40f1-8e7f-8a66c4de9e29",
                    "optout_type": "stop",
                    "identity": "identity-1-c4-4cab-9e20-5208d77dcd1b",
                    "address_type": "msisdn",
                    "address": "+1234",
                    "request_source": "testsource",
                    "requestor_source_id": "1",
                    "reason": "Test reason",
                    "created_at": "2017-01-27T10:00:06.354178Z"
                },
            ]
        }
        responses.add(
            responses.GET,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop",
            json=optouts, match_querystring=True)
        optouts = {
            "next": None,
            "previous": "http://id.example.org/api/v1/optouts/search/?"
                        "optout_type=stop&cursor=0",
            "results": [
                {
                    "id": "optout-2-8d8a-40f1-8e7f-8a66c4de9e29",
                    "optout_type": "stop",
                    "identity": "identity-2-c4-4cab-9e20-5208d77dcd1b",
                    "address_type": "msisdn",
                    "address": "+1234",
                    "request_source": "testsource",
                    "requestor_source_id": "1",
                    "reason": "Test reason",
                    "created_at": "2017-01-27T10:00:06.354178Z"
                },
            ]
        }
        responses.add(
            responses.GET,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop&"
            "cursor=1",
            json=optouts, match_querystring=True)

        res = self.api.get_optouts(params={'optout_type': 'stop'})
        result1 = next(res["results"])
        result2 = next(res["results"])
        self.assertEqual(result1['id'], "optout-1-8d8a-40f1-8e7f-8a66c4de9e29")
        self.assertEqual(result2['id'], "optout-2-8d8a-40f1-8e7f-8a66c4de9e29")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop"
        )
        self.assertEqual(
            responses.calls[1].request.url,
            "http://id.example.org/api/v1/optouts/search/?optout_type=stop&"
            "cursor=1"
        )

    @responses.activate
    def test_create_optout(self):
        optout = {
            "id": "e5210c99-8d8a-40f1-8e7f-8a66c4de9e29",
            "optout_type": "stop",
            "identity": "8311c23d-f3c4-4cab-9e20-5208d77dcd1b",
            "address_type": "msisdn",
            "address": "+1234",
            "request_source": "testsource",
            "requestor_source_id": "1",
            "reason": "Test reason",
            "created_at": "2017-01-27T10:00:06.354178Z"
        }
        responses.add(
            responses.POST,
            'http://id.example.org/api/v1/optout/',
            json=optout, status=201)

        self.api.create_optout(optout)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://id.example.org/api/v1/optout/"
        )

    @responses.activate
    def test_create_optin(self):
        optin = {
            "id": "ba27bb4e-49a3-49cd-81a4-9f6af7380cbf",
            "identity": "46f61a96-d54f-4eda-8250-e5bb86be2580",
            "address_type": "msisdn",
            "address": "+1234",
            "request_source": "Test source",
            "requestor_source_id": "1",
            "created_at": "2017-01-27T10:41:38.924319Z"
        }
        responses.add(
            responses.POST,
            'http://id.example.org/api/v1/optin/',
            json=optin, status=201)

        self.api.create_optin(optin)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.url,
            'http://id.example.org/api/v1/optin/'
        )
