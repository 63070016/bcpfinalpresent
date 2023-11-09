from flask import Blueprint, request, render_template, jsonify, session
import requests
import datetime
from create_rds import get_rds_backups, get_rds_instances, server_BCP_TEST



rds_bp = Blueprint('rds', __name__)

@rds_bp.route('/rds')
def rds():
    # Get the authentication token

    if 'auth_token' in session:
        token = session['auth_token']
    else:
        return render_template('error.html')
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    # Get RDS instances using the authentication token
    rds_instances = get_rds_instances(token, project_id)

    # Transform the RDS instances data to a format suitable for HTML rendering
    rds_list = [{"name": rds_instance['name'], "id": rds_instance['id']} for rds_instance in rds_instances.get('instances', [])]

    return render_template('rds.html', rds_list=rds_list)


@rds_bp.route('/get_rds_backups', methods=['POST'])
def get_rds_backups_route():
    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    rds_instance_id = request.form['rds_instance_id']

    try:
        rds_backups_data = get_rds_backups(token, rds_instance_id, project_id)
        rds_backups = rds_backups_data.get('backups', [])

        rds_backup_info = []
        for rds_backup in rds_backups:
            rds_backup_name = rds_backup['name']
            rds_backup_id = rds_backup['id']
            rds_begin_time_utc = datetime.datetime.strptime(rds_backup['begin_time'], "%Y-%m-%dT%H:%M:%S+%f")
            rds_begin_time_utc_gmt7 = rds_begin_time_utc + datetime.timedelta(hours=7)  # Convert to GMT+7
            rds_begin_time_formatted = rds_begin_time_utc_gmt7.strftime('%Y-%m-%d %H:%M:%S')
            rds_backup_info.append({"id": rds_backup_id, "name": f"{rds_backup_name} - {rds_begin_time_formatted}"})
        
        print(rds_backups)
        print(rds_backup_info)
        print(rds_backup_name)
        print(rds_backup_id)

        return jsonify({"rds_backups": rds_backup_info, "message": "Backups for the selected RDS instance loaded."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"rds_backups": [], "message": f"Error fetching RDS backups: {e}"})
    
@rds_bp.route('/create_rds_from_backup', methods=['POST'])
def create_rds_from_backup():

    rds_backup_id = request.form['rds_backup_id']
    rds_instance_id = request.form['rds_instance_id']
    rds_backup_name = request.form['rds_backup_name']
    rds_name = request.form['rds_name']
    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    try:
        # Get the selected backup_id from the POST request
        if 'HRMI_DB' in rds_name:
            rds_server_data = server_BCP_TEST(token, rds_instance_id, rds_backup_id, rds_name, project_id)
        elif 'POS-DB' in rds_name:
            rds_server_data = server_BCP_TEST(token, rds_instance_id, rds_backup_id, rds_name, project_id)
        else:
            rds_server_data = None
        
        print(rds_server_data)
        print(rds_name)

        # Add your logic here to create an RDS instance with the selected backup_id
        # Replace this with your actual code to create the RDS instance

        # For demonstration, you can return a success message
        return jsonify({"message": "RDS instance created successfully from backup."})

    except Exception as e:
        return jsonify({"error_message": str(e)})