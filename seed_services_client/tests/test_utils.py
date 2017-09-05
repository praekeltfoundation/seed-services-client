import responses
from unittest import TestCase
from seed_services_client.seed_services import SeedServicesApiClient
from seed_services_client.utils import get_paginated_response


class TestApiClient(SeedServicesApiClient):
    pass


class TestUtils(TestCase):
    def setUp(self):
        self.api = TestApiClient(
            "NO", "http://test.example.org/api/v1")

    @responses.activate
    def test_get_paginated_response_single_page(self):
        """
        The get_paginated_response function should return the content for the
        single page.
        """

        responses.add(
            responses.GET,
            "http://test.example.org/api/v1/tests/",
            json={
                "next": None,
                "previous": None,
                "results": [{"id": 1, "content": "content_for_1"},
                            {"id": 2, "content": "content_for_2"}]
            },
            status=200, content_type='application/json',
            match_querystring=True
        )

        res = get_paginated_response(self.api.session, "/tests/")
        self.assertEqual(list(res), [
            {"id": 1, "content": "content_for_1"},
            {"id": 2, "content": "content_for_2"}
        ])

    @responses.activate
    def test_get_paginated_response_multiple_pages(self):
        """
        The get_paginated_response function should return the content for all
        the pages.
        """

        # First page
        responses.add(
            responses.GET,
            "http://test.example.org/api/v1/tests/",
            json={
                "next": "http://test.example.org/api/v1/tests/?cursor=1",
                "previous": None,
                "results": [{"id": 1, "content": "content_for_1"},
                            {"id": 2, "content": "content_for_2"}]
            },
            status=200, content_type='application/json',
            match_querystring=True
        )
        # Second page
        responses.add(
            responses.GET,
            "http://test.example.org/api/v1/tests/?cursor=1",
            json={
                "next": "http://test.example.org/api/v1/tests/?cursor=2",
                "previous": None,
                "results": [{"id": 3, "content": "content_for_3"},
                            {"id": 4, "content": "content_for_4"}]
            },
            status=200, content_type='application/json',
            match_querystring=True
        )
        # Thrid page
        responses.add(
            responses.GET,
            "http://test.example.org/api/v1/tests/?cursor=2",
            json={
                "next": None,
                "previous": None,
                "results": [
                    {"id": 5, "content": "content_for_5"},
                ]
            },
            status=200, content_type='application/json',
            match_querystring=True
        )

        res = get_paginated_response(self.api.session, "/tests/")
        self.assertEqual(list(res), [
            {"id": 1, "content": "content_for_1"},
            {"id": 2, "content": "content_for_2"},
            {"id": 3, "content": "content_for_3"},
            {"id": 4, "content": "content_for_4"},
            {"id": 5, "content": "content_for_5"},
        ])
