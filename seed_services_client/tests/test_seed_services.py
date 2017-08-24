from mock import patch
from unittest import TestCase

from seed_services_client.seed_services import (
    SeedHTTPAdapter,
    SeedServicesApiClient,
)


class TestSeedHTTPAdapter(TestCase):

    @patch("requests.adapters.HTTPAdapter.send")
    def test_calls_parent_class_send_with_timeout(self, patch_adapter_send):
        adapter = SeedHTTPAdapter(timeout=10)
        adapter.send()
        patch_adapter_send.assert_called_with(timeout=10)


class TestSeedServicesApiClient(TestCase):

    @patch("seed_services_client.seed_services.SeedHTTPAdapter")
    def test_timeout_default_if_unset(self, patch_adapter):
        self.api = SeedServicesApiClient("token", "http://api/")
        patch_adapter.assert_called_with(timeout=65)

    @patch("seed_services_client.seed_services.SeedHTTPAdapter")
    def test_timeout_passed_if_set(self, patch_adapter):
        self.api = SeedServicesApiClient("token", "http://api/", timeout=5)
        patch_adapter.assert_called_with(timeout=5)

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
