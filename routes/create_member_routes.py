from flask import Blueprint, request, render_template, jsonify, session
import requests

from create_member import get_pool_elb_lb_id, create_elb_backend_member, get_pool_elb, get_interfaces

elbmem_bp = Blueprint('elbmem', __name__)

@elbmem_bp.route('/addelb_member')
def elb_page():
    # Render the "elb.html" page

    if 'auth_token' in session:
        token = session['auth_token']
    else:
        return render_template('error.html')
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    

    # Get ECS instances using the authentication token
    pools = get_pool_elb(token, project_id)

    pool_info = []
    for pool in pools:
        pool_name = pool['name']
        pool_id = pool['id']
        pool_descrip = pool['description']
        pool_info.append({"id": pool_id, "name": f"{pool_name}"})

    return render_template('addelb_member.html', pools = pool_info)


@elbmem_bp.route('/pool_ecs', methods=['POST'])
def elb_get_instance():
    # Render the "elb.html" page
    pool_id = request.form['pool_id']

    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    #network_id = '6035b7e3-b07c-4435-85d7-7d701c435d60'
    # Get ECS instances using the authentication token
    try:
        instances = get_pool_elb_lb_id(token, pool_id, project_id)

        instance_info = []
        for ecs in instances:
            ecs_name = ecs['name']
            ecs_id = ecs['id']
            instance_info.append({"id": ecs_id, "name": ecs_name})
        

        return jsonify({"ecs": instance_info, "message": "Backups for selected instance loaded."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"ecs": [], "message": f"Error fetchin g backups: {e}"})
    
@elbmem_bp.route('/interfaces', methods=['POST'])
def get_interfaces_route():
    server_id = request.form['ecs_id']
    pool_id = request.form['pool_id']
    pool_name = request.form['pool_name']
    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    try:
        interfaces_data = get_interfaces(token, server_id, project_id)
        interface_attachments = interfaces_data.get("interfaceAttachments", [])
        interfaces_info = []
        for attachment in interface_attachments:
            fixed_ips = attachment.get("fixed_ips", [])
            for ip in fixed_ips:
                subnet_id = ip.get("subnet_id")
                ip_address = ip.get("ip_address")
                if subnet_id and ip_address:
                    interfaces_info.append({"subnet_id": subnet_id, "ip_address": ip_address})
        


        print(subnet_id)
        print("interface_data:", interfaces_info)

        member = create_elb_backend_member(token, pool_id, subnet_id, ip_address, pool_name, project_id)
        print(member)

        return jsonify({"backups": interfaces_info, "message": "Add Member Success."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"backups": [], "message": f"Error fetching backups: {e}"})