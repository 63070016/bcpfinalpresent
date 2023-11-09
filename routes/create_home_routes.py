from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from auth import get_auth_token

home_bp = Blueprint('home', __name__)

### Home ###
@home_bp.route('/')
def homepage():
    return render_template('home.html')


@home_bp.route('/authen', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_id = request.form['clientId']
        client_secret = request.form['clientSecret']
        domain_name = request.form['domainName']
        project_name = request.form['projectName']
        project_id = request.form['projectId']  # Get project_id from the form data

        # Set project_id in the session
        session['project_id'] = project_id
        
    else:
        client_id = None
        client_secret = None
        domain_name = None
        project_name = None

    token = get_auth_token(client_id, client_secret, domain_name, project_name)

    # Get ECS instances using the authentication token
    session['auth_token'] = token

    if 'auth_token' in session:
        # Get the token from the session
        token = session['auth_token']

        session['logged_in'] = True
        # Check if project_id is in the session
        if 'project_id' in session:
            project_id = session['project_id']


            # Get ECS instances using the authentication token and project_id
            if token:
                return jsonify({"success": True, "token": token, "project_id": project_id})
            else:
                # Credentials are invalid
                return jsonify({"success": False, "error": "Invalid credentials"})
        else:
            return jsonify({"success": False, "error": "Project ID not found in session"})




@home_bp.route('/logout')
def logouthtml():

    return render_template('logout.html')

@home_bp.route('/clearsession')
def logout():
    # Clear the user's session data
    session.clear()
    # Redirect to the home page or any other page you prefer
    return redirect(url_for('home.homepage'))


