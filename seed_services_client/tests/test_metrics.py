from unittest import TestCase
import json
import responses
from base64 import b64decode

from seed_services_client.metrics import MetricsApiClient


class TestMetricsApiClient(TestCase):
    @responses.activate
    def test_get_metrics(self):
        """
        The get_metrics function creates a GET request with the correct query
        parameters as specified in the function parameters.
        """
        client = MetricsApiClient(
            'http://metrics.example.org', auth=('user', 'pass'))

        responses.add(
            responses.GET,
            'http://metrics.example.org/metrics/'
            '?m=metric1&m=metric2&from=-1h&until=-0s&nulls=zeroize&'
            'interval=1hour&align_to_from=False',
            match_querystring=True, status=200, json={})

        client.get_metrics(
            m=['metric1', 'metric2'], from_='-1h', until='-0s',
            nulls='zeroize', interval='1hour', align_to_from=False)

        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        _, auth = request.headers['Authorization'].split()
        user, pass_ = b64decode(auth).split(':')
        self.assertEqual(user, 'user')
        self.assertEqual(pass_, 'pass')

    @responses.activate
    def test_fire_metrics(self):
        """
        The fire_metrics function should create a POST request with the correct
        JSON body as specified by the function parameters.
        """
        client = MetricsApiClient(
            'http://metrics.example.org', auth=('user', 'pass'))

        responses.add(
            responses.POST,
            'http://metrics.example.org/metrics/',
            status=201, json={})

        client.fire_metrics(metric1='foo', metric2='bar')

        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        self.assertEqual(json.loads(request.body), {
            'metric1': 'foo',
            'metric2': 'bar',
        })
        request = responses.calls[0].request
        _, auth = request.headers['Authorization'].split()
        user, pass_ = b64decode(auth).split(':')
        self.assertEqual(user, 'user')
        self.assertEqual(pass_, 'pass')
