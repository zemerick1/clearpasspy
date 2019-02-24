# Python class for Aruba's Clearpass Policy Manager
[https://www.emerickcc.com](https://www.emerickcc.com)

[Aruba Networks](https://arubanetworks.com)

## Examples
```python
import clearpasspy
# Client_ID: clearpassapi
# Grant Type: client_credentials OR password
# client Secret: <CLIENT SECRET FROM UI>
# Tackle first: client credentials
server = '<SERVER NAME>'
grant_type = 'client_credentials'
client_secret = 'SUPER SECRET'
client_id = 'clearpassapi'

data = {
    'server' : server,
    'grant_type' : grant_type,
    'secret' : client_secret,
    'client' : client_id
}

# When you create the object, it automatically authenticates you, and store the access token for subsequent calls.
CPPM = clearpasspy.ClearPass(data)
print(CPPM.access_token)
3ea61fd137df506515ae45f0887df1163c4080f9

# Takes MAC address with or without colons
print(CPPM.online_status('0000af23e980'))
True

# Takes 1 arg for limiting output. . max is 1000
print(CPPM.get_endpoints(10))
[{'id': 4814, 'mac_address': '0000e349473f', 'status': 'Unknown', 'attributes': {}, '_links': {'self': {'href': 'https://clearpass.server.com/api/endpoint/4814'}}}

# Print Endpoint by ID
print('Endpoint: {}'.format(CPPM.get_endpoint(4814)))
Endpoint {'id': 4814, 'mac_address': '0000e349473f', 'status': 'Unknown', 'attributes': {}, '_links': {'self': {'href': 'https://clearpass.server.com/api/endpoint/4814'}}}

```
