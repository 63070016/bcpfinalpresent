from flask import Blueprint, request, render_template, jsonify, session



from create_ecs import get_ims_resources,server_BCP_test_server


ecs_bp = Blueprint('ecs', __name__)

### Get ims ###
@ecs_bp.route('/create_ecs')
def ims():
    # Get the authentication token
    if 'auth_token' in session:
        token = session['auth_token']
    else:
        return render_template('error.html')
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)

    # Get IMS resources using the authentication token
    ims_resources = get_ims_resources(token)

    # Extract IMS names and IDs from the IMS resources
    ims_list = [{"name": ims['name'], "id": ims['id'], "description": ims['description']} for ims in ims_resources]

    return render_template('create_ecs.html', ims_list=ims_list)

@ecs_bp.route('/create_ecs_with_ims', methods=['POST'])
def create_ecs_with_ims():
    ims_image_id = request.form['ims_image_id']
    ims_name = request.form['ims_image_name']
    ims_description = request.form['ims_image_description']

    if 'auth_token' in session:
        token = session['auth_token']
    if 'project_id' in session:
        project_id = session['project_id']
        print("Project ID:", project_id)
    try:
        
        
        # Authenticate and get the IMS image details based on ims_image_id
        

        if 'DC' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        # Create the ECS server using the extracted details
        elif 'BOR' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ########
        elif 'AP-Terminal' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)          
        ######## 
        elif 'SAP-DB' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'SAP-App' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'HRMI' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif '3M' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'FileShare' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'WS01' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'WS02' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        elif 'FTP' in ims_description:
            ecs_creation_result = server_BCP_test_server(token, ims_image_id, ims_description, project_id)
        ######## 
        else:
            ecs_creation_result = None
        return jsonify({"message": ecs_creation_result})

    except Exception as e:
        return jsonify({"error_message": str(e)})