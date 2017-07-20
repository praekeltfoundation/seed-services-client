from unittest import TestCase

from seed_services_client.seed_services import SeedServicesApiClient


class TestSeedServicesApiClient(TestCase):

    def test_retry_requests(self):
        self.api = SeedServicesApiClient("token", "http://api/", retry=True)

        self.assertEqual(
            self.api.session.adapters['https://'].max_retries.total, 5)
        self.assertEqual(
            self.api.session.adapters['http://'].max_retries.total, 5)
