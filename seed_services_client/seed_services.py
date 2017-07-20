from demands import JSONServiceClient
from requests.adapters import HTTPAdapter


class SeedServicesApiClient(object):
    """
    Base API client for seed services.

    :param str auth_token:
        An access token.

    :param str api_url:
        The full URL of the API.

    :param JSONServiceClient session:
        An instance of JSONServiceClient to use

    :param bool retry:
        Boolean indicating whether failed requests should be retried

    """

    def __init__(self, auth_token, api_url, session=None, retry=False):
        headers = {'Authorization': 'Token ' + auth_token}
        if session is None:
            session = JSONServiceClient(url=api_url,
                                        headers=headers)
        self.session = session

        if retry:
            http = HTTPAdapter(max_retries=5)
            https = HTTPAdapter(max_retries=5)
            self.session.mount('http://', http)
            self.session.mount('https://', https)
