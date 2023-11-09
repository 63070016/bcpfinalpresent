from flask import Blueprint, request, render_template, jsonify, session
import requests
import datetime
from create_ims import get_instances, get_backups, create_ims_image




ims_bp = Blueprint('ims', __name__)


@ims_bp.route('/create_ims')
def index():
    # Get the authentication token
    if 'auth_token' in session:
        token = session['auth_token']
    else:
        return render_template('error.html')
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    # Get ECS instances using the authentication token
    instances = get_instances(token, project_id)

    return render_template('create_ims.html', instances=instances)



@ims_bp.route('/get_backups', methods=['POST'])
def get_backups_route():

    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    instance_id = request.form['instance_id']

    try:
        backups_data = get_backups(token, instance_id, project_id)
        backups = backups_data.get('backups', [])



        backup_info = []
        for backup in backups:
            backup_name = backup['name']
            backup_created_at_utc = datetime.datetime.strptime(backup['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
            backup_created_at_gmt7 = backup_created_at_utc + datetime.timedelta(hours=7)  # Convert to GMT+7
            backup_created_at_formatted = backup_created_at_gmt7.strftime('%Y-%m-%d %H:%M:%S')
            backup_info.append({"id": backup['id'], "name": f"{backup_name} - {backup_created_at_formatted}"})

        return jsonify({"backups": backup_info, "message": "Backups for selected instance loaded."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"backups": [], "message": f"Error fetching backups: {e}"})
    
@ims_bp.route('/create_ims_image', methods=['POST'])
def create_ims_image_endpoint():
    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    instance_name = request.form['instance_name']
    backup_id = request.form['backup_id']

    try:
        image_data = create_ims_image(token, instance_name, backup_id, project_id)
        return jsonify({"message": "IMS image created.", "image_data": image_data})
    except requests.exceptions.HTTPError as e:
        return jsonify({"message": f"Error creating IMS image: {e}"})

