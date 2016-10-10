
"""
Client for Service Rating Store HTTP services APIs.

"""
import requests
import json


class ServiceRatingApiClient(object):

    """
    Client for ServiceRating API.

    :param str api_token:

        An API Token.

    :param str api_url:
        The full URL of the API. Defaults to
        ``http://seed-service-rating/api/v1``.

    """

    def __init__(self, api_token, api_url=None, session=None):
        if api_url is None:
            api_url = "http://seed-service-rating/api/v1"
        self.api_url = api_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token %s' % api_token
        }
        if session is None:
            session = requests.Session()
        session.headers.update(self.headers)
        self.session = session

    def call(self, endpoint, method, obj=None, params=None, data=None):
        if obj is None:
            url = '%s/%s/' % (self.api_url.rstrip('/'), endpoint)
        else:
            url = '%s/%s/%s/' % (self.api_url.rstrip('/'), endpoint, obj)
        result = {
            'get': self.session.get,
            'post': self.session.post,
            'patch': self.session.patch,
            'delete': self.session.delete,
        }.get(method, None)(url, params=params, data=json.dumps(data))
        result.raise_for_status()
        if method is "delete":  # DELETE returns blank body
            return {"success": True}
        else:
            return result.json()

    # Invites
    def get_invites(self, params=None):
        return self.call('invite', 'get', params=params)

    def get_invite(self, invite_id):
        return self.call('invite', 'get', obj=invite_id)

    def create_invite(self, invite):
        return self.call('invite', 'post', data=invite)

    def update_invite(self, invite_id, invite):
        return self.call('invite', 'patch', obj=invite_id,
                         data=invite)

    def delete_invite(self, invite_id):
        # Ratings should be deleted first for FK reasons
        return self.call('invite', 'delete', obj=invite_id)

    # Ratings
    def get_ratings(self, params=None):
        return self.call('rating', 'get', params=params)

    def get_rating(self, rating_id):
        return self.call('rating', 'get', obj=rating_id)

    def create_rating(self, rating):
        return self.call('rating', 'post', data=rating)

    def update_rating(self, rating_id, rating):
        return self.call('rating', 'patch', obj=rating_id,
                         data=rating)

    def delete_rating(self, rating_id):
        return self.call('rating', 'delete', obj=rating_id)
