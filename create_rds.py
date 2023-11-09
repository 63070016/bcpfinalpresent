
import requests


### Get RDS instance ###
def get_rds_instances(token, project_id):
    rds_url = f'https://rds.ap-southeast-2.myhuaweicloud.com/v3/{project_id}/instances'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(rds_url, headers=headers)
        response.raise_for_status()

        rds_instances = response.json()
        return rds_instances

    except requests.exceptions.RequestException as e:
        print('Error:', e)

### GET RDS BACKUP From rds_id ###
def get_rds_backups(token, rds_instance_id, project_id):
    rds_url = f'https://rds.ap-southeast-2.myhuaweicloud.com/v3/{project_id}/backups?instance_id={rds_instance_id}'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(rds_url, headers=headers)
        response.raise_for_status()

        rds_backups = response.json()
        return rds_backups

    except requests.exceptions.RequestException as e:
        print('Error:', e)



##### RDS ########


##### RDS MY SQL########
def server_BCP_TEST(token, rds_instance_id, rds_backup_id, rds_name, project_id):
    create_server_url = f'https://rds.ap-southeast-2.myhuaweicloud.com/v3/{project_id}/instances'
    
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data =  {
        "name": f"BCP_{rds_name}",
        "datastore": {
            "type": "MySQL",
            "version": "5.7"
        },
        "flavor_ref": "rds.mysql.n1.large.2",
        "volume": {
            "type": "CLOUDSSD",
            "size": 250
        },
        "region": "ap-southeast-2",
        "availability_zone": "ap-southeast-2b",
        "vpc_id": "69ea958c-0add-99983c3a3", 
        "subnet_id": "31dfd50e-dba5-4e8593a630",
        "port": "3306",
        "data_vip": "172.16",
        "security_group_id": "81b3e612-f698-4c2b-621b98",
        "restore_point": {
            "instance_id": rds_instance_id,
            "type": "backup",
            "backup_id": rds_backup_id
        },
        "disk_encryption_id": "ab5b4b65-be91-4936d18ac6",
        "tags": [
            {
            "key": "Project",
            "value": "BCP-Plan"
            }
        ]
    }

    try:
        response = requests.post(create_server_url, headers=headers, json=data)
        response.raise_for_status()
        server_data = response.json()
        server_text = response.text()

        return {"server_data": server_data, "server_text": server_text}

    except requests.exceptions.HTTPError as e:
        print(f"Error creating RDS server: {e}")
        return {"error_message": str(e)}
