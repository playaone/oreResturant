from os import environ
import logging
import requests
import json
from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from app import db
from app.models import Product, Category, Order
from app.public.forms import ShippingDetailsForm
import json

public = Blueprint('public', __name__)

@public.route('/')
def index():
    products = Product.query.all()
    return render_template('public/index.html', title='Welcome', products=products)

@public.route('/about')
def about():
    return render_template('public/about.html', title='Welcome')

@public.route('/contact')
def contact():
    return render_template('public/contact.html', title='Welcome')

@public.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get(id)
    if product:
        products = Product.query.filter_by(category_id = product.category_id).order_by(Product.id.desc()).limit(8).all()
        return render_template('public/product-detail.html', title='Welcome', product=product, products=products)
    flash(message="sorry! that product does not exist or may have been deleted", category="warning")
    return redirect(url_for('public.shop'))


@public.route('/shop/')
def shop():
    products = Product.query.paginate(page=1, per_page=30)
    filter = "All Products"
    return render_template("public/shop.html", title='Shop', products=products, filter=filter)


@public.route('/shop/<string:filter>')
def shop_filtered(filter):
    category = Category.query.filter_by(title=filter).first()
    title = "Shop"
    if category:
        title = category.title
        products = Product.query.filter_by(category_id=category.id).paginate(page=1, per_page=30)
    else:
        products = Product.query.paginate(page=1, per_page=30)
    
    return render_template("public/shop.html", title=title, products=products, filter=filter)



@public.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        session['totalCost'] = 0
        cart = request.get_data(cache=False, as_text=True)
        cart = json.loads(cart)
        
        session['orders'] = []
        
        for item in cart:
            productId = item['productId']
            quantity = item['quantity']
            
            print(quantity)
            product = Product.query.get(productId)
            
            if product:
                price = product.price_new
                session['totalCost'] += price * quantity
                orders = {
                    'productId': productId,
                    'quantity': quantity,
                    'price': price
                }                
                session['orders'].append(orders)
                session.modified = True
            else:
                return f"product with ID: {productId} not found", 404
                
                
        return "ok", 200
    return render_template('public/cart.html', title='Cart')

@public.route('/profile')
def profile():
    return render_template('public/profile.html', title='Cart')



@public.route('/invoice/<string:reference>')
def invoice(reference):
    
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    order = Order.query.filter_by(transaction_id=reference).first()
    
    if not order:
        flash(message="Error getting order details", category="danger")
        return redirect(url_for("public.checkout"))
    if request.args.get('url') or request.args.get('refresh') :       
        
        header = {
            "Authorization": f"Bearer {environ['PAYSTACK_KEY']}",
        }
        
        response = requests.get(url=url, headers=header)

        if response:
            result = response.json()
            order.status = result['data']['status']
            db.session.commit()
            # return redirect(url_for('public.invoice', reference=reference))
    
    match order.status:
        case 'pending', 'processing':
            status = 'warning'
        case 'success':
            status = "success"
        case default:
            status = "danger"
        
    return render_template('public/invoice.html', title='Invoice', order=order, status=status, reference=reference)



@public.route('/checkout', methods=['POST', 'GET'])
def checkout():
    form = ShippingDetailsForm()
    if form.validate_on_submit():
        amount = session['totalCost']
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        description = form.description.data
        
        data = {
            "email": email,
            "amount": amount * 100,
            "currency": "NGN",
        }
        
        header = {
            "Authorization": f"Bearer {environ['PAYSTACK_KEY']}",
            'Content-Type': 'application/json'
        }
        
        response = ''
        
        try:
            response = requests.post(url="https://api.paystack.co/transaction/initialize", json=data, headers=header)
        except:
            logging.warning(response)
            response = False
        
        
        if response != False:
        
            status_code = response.status_code
            
            
            response = response.json()
            
            message = response['message']
            authorization_url = response['data']['authorization_url']
            access_code = response['data']['access_code']
            transaction_id = response['data']['reference']
            
            print(transaction_id)
            
            orders = json.dumps(session['orders'])
        
        else:
            status_code = 500
        
        if status_code == 200:
            order = Order(amount=amount, email=email, firstname=form.firstname.data, lastname=form.lastname.data, phone=phone, products=orders, address=address, city=city, state=state, description=description, transaction_id=transaction_id, authorization_url=authorization_url, status_code=status_code, message=message, access_code=access_code)
            
            db.session.add(order)
            db.session.commit()
            
            session['totalCost'] = 0
            session['orders'] = []
            
            return redirect(url_for("public.invoice", reference=transaction_id))  
        else:
            logging.warning(status_code)
            flash(message="Error generating invoice, please try again later or send us a messaage", category="warning")
        
        return redirect(url_for("public.checkout"))
        
    return render_template('public/checkout.html', title='Checkout', form=form, total=session['totalCost'], orders=session['orders'])