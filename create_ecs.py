import requests
import json


### Get list image ###
def get_ims_resources(token):
    ims_url = f'https://ims.ap-southeast-2.myhuaweicloud.com/v2/cloudimages'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(ims_url, headers=headers)
        response.raise_for_status()

        ims_resources = response.json().get('images', [])  # Extract the 'images' data from the response

        # Create a list to store IMS names and IDs
        ims_list = []

        for ims in ims_resources:
            ims_id = ims.get('id', '')
            ims_name = ims.get('name', '')
            ims_description = ims.get('__description', '')

            if ims_id and ims_name:
                ims_list.append({"id": ims_id, "name": ims_name, "description" : ims_description})
        

        return ims_list  # Return a list of dictionaries containing IMS names and IDs

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return []  # Return an empty list in case of an error

    
########  
def server_BCP_test_server(token, ims_image_id, ims_description, project_id):
    create_server_url = f'https://ecs.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/cloudservers'
    
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data = {
        "server": {
            "availability_zone": "ap-southeast-2b",
            "name": f"BCP_{ims_description}",
            "imageRef": ims_image_id,
            "root_volume": {
                "volumetype": "SAS",
                "metadata": {
                "__system__encrypted": "1",
                "__system__cmkid": "bd9a9ca8-0749-4959-"
                }
            },
            "data_volumes": [
                {
                    "volumetype": "SAS",
                    "size": 100,
                    "metadata": {
                        "__system__encrypted": "1",
                        "__system__cmkid": "bd9a9ca59-8fd"
                    },
                    "extendparam": {
                        "snapshotId": "b51d7b-4e7"
                    }
                },
                {
                    "volumetype": "SAS",
                    "size": 200,
                    "metadata": {
                        "__system__encrypted": "1",
                        "__system__cmkid": "bd9a9ca5"
                    },
                    "extendparam": {
                        "snapshotId": "4663d759-0e962"
                    }
                }
            ],
            "flavorRef": "s6.xlarge.4",
            "vpcid": "b13b260b-5995-4b73a",  
            "security_groups": [
                {
                    "id": "4e98b5c0-b6c2-4122-87d" 
                },
                {
                    "id": "c3bb21fb-7ecb035338408" 
                },
                {
                    "id": "9623a3a6-c33dd36b8e5"
                },
                {
                    "id": "fd2be391-d4621e3882563"
                }, 
                {
                    "id": "948c34dc-55a4-ef516c585f"
                },
                {
                    "id": "0b09fec6-f221-4253becfad7e2"
                }
            ],
            "nics": [
                {
                    "subnet_id": "14a73f93-b4bf-48c13ae2",
                    "ip_address": "10.0."
                }
            ],
            "publicip": {
                "eip": {
                    "iptype": "5_bgp",
                    "ip_version": 4,
                    "bandwidth": {
                        "size": 100,
                        "sharetype": "PER",
                        "chargemode": "traffic",
                        "name": "BCP_SAP_TEST",
                    }
                }
            },
            "server_tags": [
                {
                    "key": "Project",
                    "value": "BCP-Plan"
                }
            ],
            "adminPass": "P@ssw0rd@!", # Password?
            "count": 1

        }
    }

    try:
        response = requests.post(create_server_url, headers=headers, json=data)
        response.raise_for_status()
        server_data = response.json()

        return {"server_data": server_data}

    except requests.exceptions.HTTPError as e:
        print(f"Error creating ECS server: {e}")
        return {"error_message": str(e)}
