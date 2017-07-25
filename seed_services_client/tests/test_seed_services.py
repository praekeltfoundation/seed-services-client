from unittest import TestCase

from seed_services_client.seed_services import SeedServicesApiClient


class TestSeedServicesApiClient(TestCase):

    def test_number_of_retries_default(self):
        self.api = SeedServicesApiClient("token", "http://api/")

        self.assertEqual(
            self.api.session.adapters['https://'].max_retries.total, 0)
        self.assertEqual(
            self.api.session.adapters['http://'].max_retries.total, 0)

    def test_number_of_retries_can_be_configured(self):
        self.api = SeedServicesApiClient("token", "http://api/", retries=5)

        self.assertEqual(
            self.api.session.adapters['https://'].max_retries.total, 5)
        self.assertEqual(
            self.api.session.adapters['http://'].max_retries.total, 5)
