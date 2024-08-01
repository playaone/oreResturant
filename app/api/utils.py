import os
import datetime
import requests
from app import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask import request

from app.models import User, Product, Category



# ==============================================Login app version 2===============================================

def admin():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user and user.type != 'customer':
        return True
    
    return False



def userDetails(user, access=None, refresh=None):
    user_details = {
        'access_token': access,
        'refresh_token': refresh,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'phone_number': user.phone,
        'type': user.type
    }
    return user_details

def menu(product):
    return {
        'title': product.title,
        'image': product.image_file,
        'description': product.description,
        'tags': product.tags,
        'price': product.price,
        'category': product.category.title
    }
    

def login():
    
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    if login != '' and password != '':
        user = User.query.filter(db.or_(User.username==login, User.phone==login)).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if user.expiry_date is None:
                user.expiry_date = datetime.datetime.now()
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            
            return userDetails(user, access_token, refresh_token), 200

        return 'Invalid credentials', 401
    return 'Input credentials', 401



# =================================================================== Refresh Token ===============================================================

def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, fresh=False)
    return access_token, 200
    

# =================================================================== register app ===============================================================
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    
    if not username or username == '':
        return 'Enter username', 401

    phone = request.form.get('phone')    
    if not phone:
        return 'Enter phone number', 401
    elif phone == '':
        return 'Phone is empty', 401

    password = request.form.get('password')
    if not password or password == '':
        return 'Enter password', 401
    
    if User.query.filter_by(username=username).first():
        return "Username already in use", 401
    
    if User.query.filter_by(email=email).first():
        return "Email already in use", 401


    if User.query.filter_by(phone=phone).first():
        return "Phone number already in use", 401

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(phone=phone, username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    
    return userDetails(user, access_token, refresh_token), 200


# ============================================================================== Update account ===========================================================

def fetch_all_menu():
    products = Product.query.all()
    all = []
    
    for product in products:
        all.append(
            menu(product)
        )
    return all, 200


def fetch_menu():
    product_id = request.args.get(id)
    
    if product_id == '':
        return "Invalid id", 401
    
    product = Product.query.get(product_id)
    
    return menu(product), 200


def fetch_all_users():
    if not admin():
        return "Unauthorized!", 400
    
    all = []
    users = User.query.all()
    
    if users:    
        for user in users:
            all.append(userDetails(user=user))
        
        return all, 200
    
    return 'No user found', 404


def fetch_user():
    if not admin():
        return "Unauthorized!", 400
    
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    
    if user:       
        return userDetails(user=user), 200
    
    return 'User not found', 404


def profile():    
    username = get_jwt_identity
    user = User.query.filter(username=username)
    
    if user:       
        return userDetails(user=user), 200
    
    return 'User not found', 404


def fetch_drinks():
    category = Category.query.filter_by(title='drinks')
    if category:
        all = []
        products = category.products
        for product in products:
            all.append(menu(product=product))
        
        return all, 200
    return 'Category not available', 404


def fetch_discounted():
    products = Product.query.filter(Product.discount != None).all()
    if products:
        all = []
        for product in products:
            all.append(menu(product))
        
        return all, 200
    return 'No dicounted product found', 404
        