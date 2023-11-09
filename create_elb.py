import requests
from flask import jsonify

def get_vpc(token, project_id):
    vpc_url = f'https://vpc.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/vpcs'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(vpc_url, headers=headers)
        response.raise_for_status()

        vpc_info = response.json()
        return vpc_info.get('vpcs', [])

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_subnets(token, vpc_id, project_id):
    subnet_url = f'https://vpc.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/subnets?vpc_id={vpc_id}'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(subnet_url, headers=headers)
        response.raise_for_status()

        subnets_info = response.json()
        print(vpc_id + "5555555555555")
        return subnets_info

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def create_elb_subnet(token, subnet_id, project_id):
    create_elb_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/loadbalancers'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data = {
        "loadbalancer": {
            "name": "BCP-loadbalance",
            "description": "Bcp-loadbalance",
            "vip_subnet_id": subnet_id,
        }
    }

    try: 
        # Print the backup_id for debugging purposes
        print(f"Creating ELB with subnet_id: {subnet_id}")

        response = requests.post(create_elb_url, headers=headers, json=data)
        response.raise_for_status()
        elb_data = response.json()
        loadbalancer_id = elb_data['loadbalancer']['id']
        loadbalancer_name = elb_data['loadbalancer']['name']
        listener = create_elb_listener(token, subnet_id, loadbalancer_id, loadbalancer_name, project_id)

        return jsonify({"backups": listener, "message": "Create Success."})

    except requests.exceptions.HTTPError as e:
        print(f"Error creating ELB: {e}")
        return {"subnet_id": subnet_id, "error_message": str(e)}
    
def create_elb_listener(token, subnet_id, loadbalancer_id, loadbalancer_name, project_id):
    create_elb_listener_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/listeners'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data = {
        "listener": { 
            "protocol_port": 80,
            "protocol": "HTTP", 
            "loadbalancer_id": f"{loadbalancer_id}", 
            "name" : "listener-test-bcp"
        } 
    }

    try:
        # Print the backup_id for debugging purposes
        print(f"Creating listener with lbid: {loadbalancer_id}")

        response = requests.post(create_elb_listener_url, headers=headers, json=data)
        response.raise_for_status()
        listener_data = response.json()
        listener_id = listener_data['listener']['id']
        listener_name = listener_data['listener']['name']
        listener_protocol = listener_data['listener']['protocol']
        listener_port = str(listener_data['listener']['protocol_port'])
        listener_port_protocol = listener_protocol + " " + listener_port

        backend_server_group = create_backend_server(token, listener_id, loadbalancer_name, listener_name, listener_port_protocol, project_id)
        return {"listener_id": listener_id, "listener_data": listener_data}

    except requests.exceptions.HTTPError as e:
        print(f"Error creating listener: {e}")
        return {"lb_id": loadbalancer_id, "error_message": str(e)}

def create_backend_server(token, listener_id, loadbalancer_name, listener_name, listener_protocol, project_id):
    create_backend_server_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/pools'
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    data = {
        "pool": {
            "lb_algorithm": "ROUND_ROBIN",
            "listener_id": listener_id,  # Use the provided loadbalancer_id
            "protocol": "HTTP",
            "name" : "BCP_test-backend-member-group",
            "description" : loadbalancer_name + " | " + listener_name + " | " + listener_protocol
        }
    }

    try:
        # Print the loadbalancer_id for debugging purposes
        print(f"Creating backend with listener_id: {listener_id}")

        response = requests.post(create_backend_server_url, headers=headers, json=data)
        response.raise_for_status()
        backend_server_data = response.json()
        pool_id = backend_server_data.get("pool", {}).get("id")

        return {"pool_id": pool_id}
    except requests.exceptions.HTTPError as e:
        print(f"Error creating backend server: {e}")
        return {"listener_id": listener_id, "error_message": str(e)}