import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
# mail = Mail()
loginManager = LoginManager()


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
    
    from app.public.routes import public
    from app.admin.routes import admin
    from app.errors.handlers import errors
    
    app.register_blueprint(public)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    
    
    with app.app_context():
        db.create_all()
        
    return app
    
    