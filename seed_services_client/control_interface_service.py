from demands import JSONServiceClient


class ControlInterfaceServiceApiClient(object):
    """
    Client for Control Interface Service.

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

    def get_definitions(self, params=None):
        return self.session.get('/definition/', params=params)

    def get_definition(self, definition):
        return self.session.get('/definition/%s/' % definition)

    def update_definition(self, definition, data=None):
        return self.session.patch('/definition/%s/' % definition, data=data)

    def create_definition(self, definition):
        return self.session.post('/definition/', data=definition)

    def delete_definition(self, definition):
        self.session.delete('/definition/%s/' % definition)
        return {"success": True}
