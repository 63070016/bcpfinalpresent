import requests


def get_pool_elb(token, project_id):
    pool_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/pools'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(pool_url, headers=headers)
        response.raise_for_status()

        pools_info = response.json()
        return pools_info.get('pools', [])

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_pool_elb_lb_id(token, pool_id, project_id):
    pool_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/pools?id={pool_id}'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(pool_url, headers=headers)
        response.raise_for_status()

        pools_info = response.json()

        loadbalancer_id = pools_info.get('pools', [])[0].get('loadbalancers', [])[0].get('id') if pools_info.get('pools') else None

        loadbalances = get_loadbalance_id(token, loadbalancer_id, project_id)
        return loadbalances

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_loadbalance_id(token, loadbalancer_id, project_id):
    lb_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/loadbalancers?id={loadbalancer_id}'
    

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(lb_url, headers=headers)
        response.raise_for_status()

        lb_info = response.json()
        vip_subnet_id = lb_info.get('loadbalancers', [])[0].get('vip_subnet_id')
        nt_subnet = get_vip_network_id(token, vip_subnet_id, project_id)
        return nt_subnet

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_vip_network_id(token, vip_subnet_id, project_id):
    vip_subnet_url = f'https://vpc.ap-southeast-2.myhuaweicloud.com/v2.0/subnets?id={vip_subnet_id}'
    

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(vip_subnet_url, headers=headers)
        response.raise_for_status()

        vip_subnet_info = response.json() 
        vip_network = vip_subnet_info.get('subnets', [])

        for network in vip_network:
            network_id = network.get('network_id')
        
        vpc = get_vpc_id(token, network_id, project_id)

        print (network_id)
        return vpc

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_vpc_id(token, network_id, project_id):
    vpc_subnet_url = f'https://vpc.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/subnets/{network_id}'
    

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(vpc_subnet_url, headers=headers)
        response.raise_for_status()

        vpc_subnet_info = response.json() 

        subnet = vpc_subnet_info.get('subnet', {})
        vpc_id = subnet.get('vpc_id')

        vpc_map_ecs = vpc_ecs(token, vpc_id, project_id)
        
        return vpc_map_ecs

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def vpc_ecs(token, vpc_id, project_id):
    vpc_subnet_url = f'https://ecs.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/cloudservers/detail'
    

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(vpc_subnet_url, headers=headers)
        response.raise_for_status()

        ecs_info = response.json() 

        servers = ecs_info.get('servers', [])
        matching_servers = [] 

        for server in servers:
            server_name = server.get('name', '')
            metadata = server.get('metadata', {})
            server_vpc_id = metadata.get('vpc_id', '')
            
            if server_vpc_id == vpc_id:
                print(f"Server {server_name} is in the specified VPC ({vpc_id})")
                matching_servers.append(server)
        
        return matching_servers

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def get_interfaces(token, server_id, project_id):
    interface_url = f'https://ecs.ap-southeast-2.myhuaweicloud.com/v1/{project_id}/cloudservers/{server_id}/os-interface'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    try:
        response = requests.get(interface_url, headers=headers)
        response.raise_for_status()
        interfaces = response.json()

        print(interfaces)
        return interfaces

    except requests.exceptions.RequestException as e:
        print('Error:', e)


def create_elb_backend_member(token, pool_id, subnet_id, ip_address, pool_name, project_id):
    create_backend_server_url = f'https://elb.ap-southeast-2.myhuaweicloud.com/v2/{project_id}/elb/pools/{pool_id}/members'

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    if "BCP_server_group-backend-service" in pool_name:
        data = {
        "member": {
            "subnet_id": subnet_id,
            "protocol_port": 28080,
            "address": ip_address
        }
    }
    elif "BCP_server_group-eordering" in pool_name:

        data = {
        "member": {
            "subnet_id": subnet_id,
            "protocol_port": 18080,
            "address": ip_address
        }
    }
    elif "BCP_server_group-srifabakery" in pool_name:
        data = {
        "member": {
            "subnet_id": subnet_id,
            "protocol_port": 8080,
            "address": ip_address
        }
    }
    else:
        None


    try:
        # Print the backup_id for debugging purposes
        print(f"Creating Member: {pool_id} - {pool_name}")

        response = requests.post(create_backend_server_url, headers=headers, json=data)
        response.raise_for_status()
        backend_server_member = response.json()

        return {"pool_id": pool_id, "backend_server_member": backend_server_member, "subnet_id" : subnet_id}

    except requests.exceptions.HTTPError as e:
        print(f"Error creating Member: {e}")
        return {"pool_id": pool_id, "error_message": str(e)}
    

