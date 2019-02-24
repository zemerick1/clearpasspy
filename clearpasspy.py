import requests
import json

# ENDPOINT URL /api/insight/endpoint/mac/

class ClearPass():
    ''' Login when class is initiated. '''
    def __init__(self, data):
        self.get_access_token(data)
        self.server = data['server']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': "{} {}".format('Bearer', self.access_token)
        }
    def online_status(self, macaddress):
        ''' Returns true/false if endpoint is online '''
        is_online = False
        token = self.access_token
        macaddress = macaddress.replace(':', '')
        url = 'https://' + self.server + '/api/insight/endpoint/mac/' + macaddress
        r = requests.get(url, headers=self.headers)
        json_r = json.loads(r.text)
        if json_r['is_online'] == True:
            is_online = True
        else:
            is_online = False
        return is_online
    def get_endpoints(self, limit):
        ''' Returns first 'limit' endpoints '''
        ''' Need this to be more dynamic for limiting results. '''
        url = 'https://' + self.server + '/api/endpoint?filter=%7B%7D&sort=%2Bid&offset=0&limit=' + str(limit) + '&calculate_count=false'
        r = requests.get(url, headers=self.headers)
        json_r = json.loads(r.text)
        return json_r['_embedded']['items']

    def get_endpoint(self, id):
        ''' Returns endpoint based on ID'''
        url = 'https://' + self.server + '/api/endpoint/' + str(id)
        r = requests.get(url, headers=self.headers)
        json_r = json.loads(r.text)
        if r.status_code == 200:
            return json_r
        elif r.status_code == 404:
            return 'Invalid ID'
        else:
            return r.status_code
    def get_access_token(self, data):
        ''' https://github.com/aruba/clearpass-api-python-snippets '''
        """Get OAuth 2.0 access token"""
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

