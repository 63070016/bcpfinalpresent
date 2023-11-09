import requests
import json

## AUTHEN ##
def get_auth_token(client_id, client_secret, domain_name, project_name):
    auth_url = 'https://iam.myhuaweicloud.com/v3/auth/tokens'

    headers = {
        'Content-Type': 'application/json'
    }
 
    payload = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': client_id,
                        'password': client_secret,
                        'domain': {
                            'name': domain_name
                        }
                    }
                }
            },
            'scope': {
                'project': {
                    'name': project_name 
                }
            }
        }
    }

    response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    token = response.headers['X-Subject-Token']

    print(token)

    return token