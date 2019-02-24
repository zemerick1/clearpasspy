import requests
import json

# ENDPOINT URL /api/insight/endpoint/mac/

class ClearPass():
    ''' Login when class is initiated. '''
    def __init__(self, data):
        self.get_access_token(data)
        self.server = data['server']
    def online_status(self, macaddress):
        is_online = False
        token = self.access_token
        macaddress = macaddress.replace(':', '')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "{} {}".format('Bearer', token)
        }
        url = 'https://' + self.server + '/api/insight/endpoint/mac/' + macaddress
        r = requests.get(url, headers=headers)
        print(r)
        json_r = json.loads(r.text)
        if json_r['is_online'] == True:
            is_online = True
        else:
            is_online = False
        return is_online
    def get_access_token(self, data):
        ''' https://github.com/aruba/clearpass-api-python-snippets '''
        """Get OAuth 2.0 access token with config from params.cfg"""
        clearpass_fqdn = data['server']
        oauth_grant_type = data['grant_type']
        oauth_client_id = data['client']
        oauth_client_secret = data['secret']
        url = "https://" + clearpass_fqdn + "/api/oauth"

        headers = {'Content-Type': 'application/json'}

        ''' grant_type: password '''
        if oauth_grant_type == "password":
            payload = {'grant_type': oauth_grant_type, 'username': oauth_username, 'password': oauth_password,
                       'client_id': oauth_client_id, 'client_secret': oauth_client_secret}
            try:
                r = requests.post(url, headers=headers, json=payload)
                r.raise_for_status()
            except Exception as e:
                print(e)
                exit(1)
            json_response = json.loads(r.text)
            return json_response
        ''' grant_type: password   public client '''
        if oauth_grant_type == "password" and not oauth_client_secret:
            payload = {'grant_type': oauth_grant_type, 'username': oauth_username, 'password': oauth_password,
                       'client_id': oauth_client_id}
            try:
                r = requests.post(url, headers=headers, json=payload)
                r.raise_for_status()
            except Exception as e:
                print(e)
                exit(1)
            json_response = json.loads(r.text)
            return json_response
        ''' grant_type: client_credentials '''
        if oauth_grant_type == "client_credentials":
            payload = {'grant_type': oauth_grant_type, 'client_id': oauth_client_id,
                       'client_secret': oauth_client_secret}
            try:
                r = requests.post(url, headers=headers, json=payload)
                r.raise_for_status()
            except Exception as e:
                print(e)
                exit(1)
            json_response = json.loads(r.text)
            self.access_token = json_response['access_token']
            return json_response

