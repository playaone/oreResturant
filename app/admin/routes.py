import json, logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from app import db, bcrypt
from app.models import Product, Category, User, Order
from app.admin.forms import AddProductForm, AddCategoryForm, AddUserForm, LoginUserForm, UpdateUserForm
from app.admin.utils import upload_image
from sqlalchemy import func

admin = Blueprint('admin', __name__)

# ======================================================================================================================

@admin.route('/')
@admin.route('/admin/')
@login_required
def home():
    orders_count = Order.query.count()
    all_orders = Order.query.with_entities(func.sum(Order.amount).label('sum_amounts')).first()
    avg_sales =  all_orders.sum_amounts / orders_count if orders_count > 0 and all_orders > 0 else 0
    return render_template('admin/index.html', orders_count=orders_count, avg_sales=f'{avg_sales: .2f}')


@admin.route('/admin/register/', methods=['POST', 'GET'])
def admin_register():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, firstname=form.firstname.data, lastname=form.lastname.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(message=f'User Added, password = {form.password.data}', category='success')
        login_user(user)
        return redirect(url_for('admin.home'))
        
    return render_template('admin/auth-signup.html', title='Add User', form=form)

@admin.route('/admin/login/', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))
    form = LoginUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.home'))
        else:
            flash('Invalid username/password', category='danger')
            return redirect(url_for('admin.admin_login'))
    return render_template('admin/auth-signin.html', title='Add User', form=form)



@admin.route('/admin/logout/')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.admin_login'))
    logout_user()
    return redirect(url_for('admin.admin_login'))

# ======================================================Users================================================================

@admin.route('/users')
def users():
    users = User.query.all()
    if not users:
        flash(message='No user found', category="danger")
        return redirect(url_for('admin.home'))
    return render_template('admin/users.html', title="Users", users=users)

# ======================================================Add User================================================================
@admin.route('/users/add', methods=['POST', 'GET'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, type=form.type.data, email=form.email.data, phone=form.phone.data, firstname=form.firstname.data, lastname=form.lastname.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(message=f'User Added, password = {form.password.data}', category='success')
        return redirect(url_for('admin.add_user'))
    return render_template('admin/add-user.html', title="Add User", form=form)


# ======================================================Add User================================================================
@admin.route('/users/edit/<int:user_id>', methods=['POST', 'GET'])
def edit_user(user_id):
    form = UpdateUserForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        
        if user.username != form.username.data:
            username_user = User.query.filter_by(username=form.username.data).first()
            if not username_user:
                user.username=form.username.data
            else:
                flash(message='Username already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
            
        if user.email != form.email.data:
            email_user = User.query.filter_by(email=form.email.data).first()
            if not email_user:
                user.email=form.email.data
            else:
                flash(message='Email address already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
            
        if user.phone != form.phone.data:
            phone_user = User.query.filter_by(phone=form.phone.data).first()
            if not phone_user:
                user.phone=form.phone.data
            else:
                flash(message='Phone number already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
        
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.type=form.type.data
        
        db.session.commit()
        flash(message=f'User details updated', category='success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit-user.html', title="Edit User", form=form, user=user)

# ======================================================Delete User================================================================

@admin.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(message=f"User ({user.email}) Deleted", category="success")
        return redirect(url_for('admin.users'))
    else:
        flash(message="User not found", category="warning")
    return redirect(url_for('admin.users'))
        





# ======================================================================================================================







# ======================================================================================================================

@admin.route('/admin/category/all', methods=['POST', 'GET'])
@login_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories-list.html', title='All Categories', categories=categories)

# ======================================================================================================================


@admin.route('/admin/category/delete/<int:cat_id>', methods=['POST', 'GET'])
@login_required
def delete_category(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        flash(message="Category deleted", category="success")
    else:
        flash(message="Category not found", category="danger")
    return redirect(url_for('admin.categories'))

# ======================================================================================================================

@admin.route('/admin/category/add', methods=['POST', 'GET'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():        
        category = Category(title=form.title.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added!', category='success')
        return redirect(url_for('admin.add_category'))
    categories = Category.query.all()
    return render_template('admin/categories-add.html', title='Add Product', form=form, categories=categories)

# =======================================================================================================================

@admin.route('/admin/product/add', methods=['POST', 'GET'])
@login_required
def add_product():
    form = AddProductForm()
    form.category.query = Category.query.all()
    if form.validate_on_submit():
        image = upload_image(form.image_file.data)
        product = Product(title=form.name.data,
                          description=form.description.data,
                          tags=form.tags.data,
                          price=form.price.data,
                          image=image,
                          category=form.category.data,
                          category_id=form.category.data.id,
                          user_id=current_user.id,
                          author = current_user
                          )
        db.session.add(product)
        db.session.commit()
        flash('Product added!', category='success')
        return redirect(url_for('admin.add_product'))
    return render_template('admin/product_add.html', title='Add Product', form=form)

# ==================================================================================================================================

@admin.route('/admin/product/<int:product_id>/view/')
@login_required
def view_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash(message="Product not found!", category="warning")
        return redirect(url_for('admin.home'))
    return render_template('admin/product-detail.html', title='Add Product', product=product)

# =================================================================================================================================

@admin.route('/admin/products/all/')
@login_required
def all_products():
    products = Product.query.all()
    categories = Category.query.all()
    if not products:
        flash(message="No product in the inventory!", category="warning")
        return redirect(url_for('admin.home'))
    return render_template('admin/product_list.html', title='Add Product', products=products, categories=categories)

# =================================================================================================================================

@admin.route('/admin/product/delete/<product_id>')
@login_required
def delete_product(product_id):
    return redirect(url_for('admin.home'))

# ====================================================================================================================================

@admin.route('/admin/product/<product_id>/update/')
@login_required
def update_product():
    return render_template('admin/product-edit.html', title='Add Product')


# ================================================================ All Orders ====================================================================

@admin.route("/admin/orders")
@login_required
def all_orders():
    orders = Order.query.order_by(Order.id.asc()).all()
    return render_template('admin/orders.html', title="All Orders", orders=orders)

# ================================================================ All Orders ====================================================================

@admin.route("/admin/orders/pending")
@login_required
def pending_orders():
    orders = Order.query.filter_by(status='pending').order_by(Order.id.asc()).all()
    return render_template('admin/orders.html', title="All Orders", orders=orders)


# ================================================================ All Orders ====================================================================

@admin.route("/admin/orders/failed")
@login_required
def failed_orders():
    orders = Order.query.filter_by(status='failed').order_by(Order.id.asc()).all()
    return render_template('admin/orders.html', title="All Orders", orders=orders)


# ================================================================ All Orders ====================================================================

@admin.route("/admin/orders/success")
@login_required
def successful_orders():
    orders = Order.query.filter_by(status='success').order_by(Order.id.asc()).all()
    return render_template('admin/orders.html', title="All Orders", orders=orders)


# ================================================================ All Orders ====================================================================

@admin.route("/admin/order/delete/<string:order_id>")
@login_required
def delete_order(order_id):
    order = Order.query.filter_by(transaction_id=order_id).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        flash(message=f"Order {order.transaction_id} deleted", category="success")
    return redirect(request.referrer)


# ================================================================ View Order ====================================================================

@admin.route("/admin/order/view/<string:order_id>")
@login_required
def view_order(order_id):
    order = Order.query.filter_by(transaction_id=order_id).first()
    if order:
        products_json = json.loads(order.products)
        products = []
        for p in products_json:
            product = Product.query.get(p['productId'])
            product.purchase_quantity = p['quantity']
            product.cost = p['quantity'] * p['price']
            products.append(product)
        return render_template('admin/order-details.html', title="All Orders", order=order, products=products)
    else:
        return redirect(request.referrer)