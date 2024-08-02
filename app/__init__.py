import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
loginManager = LoginManager()
jwt = JWTManager()


loginManager.login_view = 'admin.admin_login'
loginManager.login_message = 'Please Login'
loginManager.login_message_category = 'danger'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    
    from app.admin.routes import admin
    from app.errors.handlers import errors
    
    from flask_restful import Api
    
    api = Api(app)
    
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    
    
    from app.api.resource import Login, Registration, FetchAll, FetchOne, Discounted, FetchDrinks, Profile
    
    api.add_resource(Registration, '/register')
    api.add_resource(Login, "/login")
    api.add_resource(FetchAll, "/menus")
    api.add_resource(FetchOne, "/menus/<int:id>")
    api.add_resource(FetchDrinks, "/menus/drinks")
    api.add_resource(Discounted, "/menus/discounted")
    api.add_resource(Profile, "/profile")
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return "Invalid login token", 401
    
    @jwt.expired_token_loader
    def expired_token_callback(header, data):
        return "Token expired", 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return "Unauthorized!", 401
    
    
    with app.app_context():
        db.create_all()
        
    return app
    
    