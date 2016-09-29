import os

import requests
import requests.exceptions


class Client(object):

    def __init__(self, host, token=None, username=None, password=None):
        self.host = host
        self.token = token or os.environ.get('VIDEOFRONT_TOKEN')
        if not self.token:
            if not username or not password:
                raise ValueError(
                    "You need to either define an authentication token "
                    "or a pair username/password. Both can be obtained by "
                    "running the 'createuser' management command.\n"
                    "The token can also be set as the VIDEOFRONT_TOKEN environment variable."
                )
            self.token = self._get_token(username, password)

    def endpoint(self, name):
        return self.host + '/api/v1/' + name

    def _get_token(self, username, password):
        response = requests.post(
            self.endpoint('auth-token/'),
            data={
                'username': username,
                'password': password,
            }
        )
        response_data = response.json()
        return response_data['token']

    def get(self, endpoint, params=None):
        return self._request('get', endpoint, params=params)

    def post(self, endpoint, data=None, files=None):
        return self._request('post', endpoint, data=data, files=files)

    def delete(self, endpoint, data=None):
        return self._request('delete', endpoint, data=data)

    def _request(self, method, endpoint, **kwargs):
        func = getattr(requests, method)
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = 'Token ' + self.token
        response = func(self.endpoint(endpoint), **kwargs)
        if response.status_code >= 400:
            raise HttpError(response.status_code, response.content)
        return response


class HttpError(Exception):

    def __init__(self, status_code, content):
        super(HttpError, self).__init__("HTTP error {}: {}".format(status_code, content))
