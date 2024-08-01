from app import db, loginManager
from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import serializer
import datetime

# decorted function
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(30), unique=True, nullable=False)
    email= db.Column(db.String(130), unique=True, nullable=False)
    phone= db.Column(db.String(15))
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(12), nullable=True, default='customer')
    posts = db.relationship('Product', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"Username=> {self.user}, email=> {self.email}"
  

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True, cascade="all, delete")
    
    def __str__(self):
        return self.title
     
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    discount = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(20), nullable=False)
    products = db.Column(db.Text(), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    status_code = db.Column(db.String(50), nullable=False)
    authorization_url = db.Column(db.String(50), nullable=False)
    access_code = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now())