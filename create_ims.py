import requests
import json


### GET ECS ###
def get_instances(token, project_id):
    instances_url = f'https://ecs.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/cloudservers/detail'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    response = requests.get(instances_url, headers=headers)
    response.raise_for_status()

    instances_data = response.json()
    return instances_data.get('servers', [])

### GET BACKUP ###
def get_backups(token, instance_id, project_id):
    backups_url = f'https://cbr.ap-southeast-2.myhuaweicloud.com/v3/{project_id}/backups?resource_id={instance_id}'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    response = requests.get(backups_url, headers=headers)
    response.raise_for_status()

    backups = response.json()
    return backups


### Create Image from Backup ###
def create_ims_image(token, instance_name, backup_id, project_id):
    create_image_url = 'https://ims.ap-southeast-2.myhuaweicloud.com/v1/cloudimages/wholeimages/action'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data = {
        'name': f'BCP_{instance_name}',
        'description': f'{instance_name}',
        'backup_id': backup_id,
        'whole_image_type': 'CBR'
        
    }

    try:
        # Print the backup_id for debugging purposes
        print(f"Creating IMS image with backup_id: {backup_id}")

        response = requests.post(create_image_url, headers=headers, json=data)
        response.raise_for_status()
        image_data = response.json()
        print(image_data)
        return {"backup_id": backup_id, "image_data": image_data}

    except requests.exceptions.HTTPError as e:
        print(f"Error creating IMS image: {e}")
        return {"backup_id": backup_id, "error_message": str(e)}