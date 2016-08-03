from demands import JSONServiceClient


class IdentityStoreApiClient(object):
    """
    Client for Identity Store Service.

    :param str auth_token:

        An access token.

    :param str api_url:
        The full URL of the API.

    """

    def __init__(self, auth_token, api_url, session=None):
        headers = {'Authorization': 'Token ' + auth_token}
        if session is None:
            session = JSONServiceClient(url=api_url,
                                        headers=headers)
        self.session = session

    def get_identities(self, params=None):
        return self.session.get('/identities/', params=params)

    def get_identity(self, identity):
        # return None on 404 becuase that means an identity not found
        self.session.is_acceptable = \
            lambda response, request_params: response.status_code in [404, 200]
        result = self.session.get('/identities/%s/' % identity)
        if "detail" in result and result["detail"] == "Not found.":
            return None
        return result

    def get_identity_by_address(self, address_type, address_value):
        params = {"details__addresses__%s" % address_type: address_value}
        return self.session.get('/identities/search/', params=params)
