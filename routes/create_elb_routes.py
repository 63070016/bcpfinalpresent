
from flask import Blueprint, request, render_template, jsonify, session
import requests

from create_elb import get_subnets, get_vpc, create_elb_subnet

elb_bp = Blueprint('elb', __name__)

@elb_bp.route('/create_elb')
def elb_create():
    # Render the "elb.html" page
    # Get the authentication token
    # Get the authentication token
    if 'auth_token' in session:
        token = session['auth_token']
    else:
        return render_template('error.html')
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    vpcs = get_vpc(token, project_id)

    # Get ECS instances using the authenticatio
    return render_template('create_elb.html', vpcs=vpcs)

@elb_bp.route('/get_subnets', methods=['POST'])
def get_instance_subnets():
    vpc_id = request.form['vpc_id']

    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    try:
        subnets_data = get_subnets(token, vpc_id, project_id)
        subnets = subnets_data.get('subnets', [])

        subnet_info = []
        for subnet in subnets:
            subnet_name = subnet['name']
            neutron_subnet_id = subnet['neutron_subnet_id']
            subnet_info.append({"id": neutron_subnet_id, "name": subnet_name})
        
        print("subnet_data:", subnet_info)

        return jsonify({"backups": subnet_info, "message": "Backups for selected instance loaded."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"backups": [], "message": f"Error fetching backups: {e}"})

@elb_bp.route('/create_elb', methods=['POST'])
def create_elb_route():
    neutron_subnet_id = request.form['subnet_id']
    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    try:
        elb_data = create_elb_subnet(token, neutron_subnet_id, project_id)
        
        print("elb_data:", elb_data)

        return {"message": "ELB Create Success"}
    except requests.exceptions.HTTPError as e:
        return {"backups": [], "message": f"Error fetching backups: {e}"}