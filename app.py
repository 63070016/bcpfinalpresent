from flask import Flask

from routes import create_ecs_routes, create_ims_routes, create_rds_routes, create_elb_routes, create_member_routes, create_home_routes


app = Flask(__name__, static_url_path='/static', template_folder="templates")


app.secret_key = 'P@ssword' #your secret key

# Register blueprints
app.register_blueprint(create_home_routes.home_bp, url_prefix='/')
app.register_blueprint(create_ims_routes.ims_bp, url_prefix='/')
app.register_blueprint(create_ecs_routes.ecs_bp, url_prefix='/')
app.register_blueprint(create_rds_routes.rds_bp, url_prefix='/')
app.register_blueprint(create_elb_routes.elb_bp, url_prefix='/')
app.register_blueprint(create_member_routes.elbmem_bp, url_prefix='/')



if __name__ == '__main__':
    app.run(debug=True)