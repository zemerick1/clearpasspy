import requests
import json
import logging

_LOGGER = logging.getLogger(__name__)


class ClearPass:
    """Login when class is initiated."""
    def __init__(self, data):
        self.get_access_token(data)
        self.server = data['server']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': "{} {}".format('Bearer', self.access_token)
        }

    def api_get(self, service):
        """Call specified API service endpoint with GET method."""
        url = 'https://' + self.server + '/api' + service
        try:
            r = requests.get(url, headers=self.headers)
            json_r = json.loads(r.text)
        except Exception as e:
            print(e)
        return json_r

    def api_post(self, service, payload):
        """Call specified API service endpoint with POST method."""
        url = 'https://' + self.server + '/api' + service
        try:
            r = requests.post(url, headers=self.headers, data=json.dumps(payload))
            json_r = json.loads(r.text)
        except Exception as e:
            print(e)
        return json_r

    def api_patch(self, service, payload):
        """Call specified API service endpoint with PATCH method."""
        url = 'https://' + self.server + '/api' + service
        try:
            r = requests.patch(url, headers=self.headers, data=json.dumps(payload))
            json_r = json.loads(r.text)
        except Exception as e:
            print(e)
        return json_r

    def online_status(self, mac_address):
        """Return true/false if endpoint is online."""

        mac_address = mac_address.replace(':', '')
        service = '/insight/endpoint/mac/' + mac_address
        endpoint = self.api_get(service)
        if endpoint['is_online']:
            is_online = True
        else:
            is_online = False
        return is_online

    def get_endpoints(self, limit):
        """Return first 'limit' endpoints."""
        service = '/endpoint?filter=%7B%7D&sort=%2Bid&offset=0&limit=' + str(limit) + '&calculate_count=false'
        endpoint = self.api_get(service)
        return endpoint

    def get_endpoint(self, endpoint_id):
        """Return endpoint based on ID."""
        service = '/endpoint/' + str(endpoint_id)
        endpoint = self.api_get(service)
        return endpoint

    def get_access_token(self, data):
        """Get OAuth 2.0 access token."""
        clearpass_fqdn = data['server']
        oauth_grant_type = data['grant_type']
        oauth_client_id = data['client']
        oauth_client_secret = data['secret']
        url = "https://" + clearpass_fqdn + "/api/oauth"

        headers = {'Content-Type': 'application/json'}

        if oauth_grant_type == "password":
            payload = {'grant_type': oauth_grant_type, 'username': oauth_username, 'password': oauth_password,
                       'client_id': oauth_client_id, 'client_secret': oauth_client_secret}
            _LOGGER.debug("PAYLOAD: {}".format(payload))
            r = requests.post(url, headers=headers, json=payload)
            json_response = json.loads(r.text)
            if r.status_code == 200:
                self.access_token = json_response['access_token']
            else:
                self.access_token = r.status_code
            return self.access_token

        if oauth_grant_type == "password" and not oauth_client_secret:
            payload = {'grant_type': oauth_grant_type, 'username': oauth_username, 'password': oauth_password,
                       'client_id': oauth_client_id}
            _LOGGER.debug("PAYLOAD: {}".format(payload))
            r = requests.post(url, headers=headers, json=payload)
            json_response = json.loads(r.text)
            if r.status_code == 200:
                self.access_token = json_response['access_token']
            else:
                self.access_token = r.status_code
            return self.access_token

        if oauth_grant_type == "client_credentials":
            payload = {'grant_type': oauth_grant_type, 'client_id': oauth_client_id,
                       'client_secret': oauth_client_secret}
            _LOGGER.debug("PAYLOAD: {}".format(payload))
            r = requests.post(url, headers=headers, json=payload)
            json_response = json.loads(r.text)
            _LOGGER.debug("RESPONSE (CC): {}".format(json_response))
            if r.status_code == 200:
                self.access_token = json_response['access_token']
            else:
                self.access_token = r.status_code
            return self.access_token

