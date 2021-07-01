from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from  . import db
from .models import Orders, Products,Manufacturers,Users,Call_center_staff,Customer_service_staff,Marketing_staff,Stocking_clerks,Managers,Stores,Warehouses,Customers,Contract_customers,Credit_customers
from werkzeug.security import generate_password_hash
import random
views= Blueprint('views', __name__)
#CUSTOMER VIEWS
@views.route('/home',methods=['GET','POST'])
def home():
    # if request.method=='GET':
    #     result = request.args.get('search')
    #     return redirect(url_for('views.search'),result)
  
    
            

    return render_template('index.html',Products=Products.query.all())

@views.route('/description/<id>')
def description(id):
    product=Products.query.filter_by(id=id).first()
    return render_template('description.html',product=product)

@views.route('/addCart' ,methods=['POST'])
def addCart():
    if request.method=='POST':
        product_id=request.form.get('id')
        product=Products.query.filter_by(id=product_id).first()
        product_dict={product_id:{'name':product.name,'price':product.price}}
        if 'cart'in session:
            if product_id in session['cart']:
                flash('product exists')
            else:    
                session['cart']=dict(list(session['cart'].items())+list(product_dict.items()))
        else:
            session['cart']=product_dict    

    return redirect(request.referrer)
@views.route('/cart')
def cart():   
        
    return render_template('cart.html')
@views.route('/checkout')
def checkout():
    if 'cart' in session:
        order_id=random.randint(1,1000,1)
        for  product in session['cart'].items():
            order=Orders(id=order_id,product_id=product)
            db.session.add(order)
        db.session.commit()
        return redirect(url_for('views.my_orders'))
    else:
        flash('Cart is Empty')
    return render_template('checkout.html')

@views.route('/my_orders/<id>')
def my_orders():
    orders=Orders.query.filter_by(customer_id=id).all()
    return render_template('my_orders.html',orders=orders)
    
@views.route('/search',methods=['POST','GET'])
def search():
 
    
    return render_template('search.html')

 

@views.route('/profile')
def profile():
    return render_template('profile.html')


#ADMIN VIEWS
@views.route('/adminDash')
def admin_dash():
    return render_template('admindash.html')

#CREATE
@views.route('/createUser',methods=['GET','POST'])
def create_user():
    if request.method=='POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        type = request.form.get('department')
        password=request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            state=True
            #flash('Email already exists',category='error')
        else:
            new_user=Users(email=email,first_name=first_name, last_name=last_name,type=type,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
              
            if type=='call_center':
                user = Users.query.filter_by(email=email).first()
                user_id=user.id
                new_user=Call_center_staff(user_id=user_id)
            if type=='customer_service':
                user = Users.query.filter_by(email=email).first()
                user_id=user.id
                new_user=Customer_service_staff(user_id=user_id)
            if type=='warehouse':
                user = Users.query.filter_by(email=email).first()
                user_id=user.id
                new_user=Stocking_clerks(user_id=user_id)
            if type=='marketing':
                user = Users.query.filter_by(email=email).first()
                user_id=user.id
                new_user=Marketing_staff(user_id=user_id)
            if type=='manager':
                user = Users.query.filter_by(email=email).first()
                user_id=user.id
                new_user=Managers(user_id=user_id)
                                
            db.session.add(new_user)
            db.session.commit()   

    return render_template('createuser.html')

@views.route('/createStore',methods=['POST','GET'])
def create_store():
    if request.method=='POST':
        location = request.form.get('location')
        stock_id=request.form.get('stock_id')      
        store = Stores.query.filter_by(location=location).first()
        if store:
            pass
            #flash('Store already exists',category='error')
        else:          
            new_store=Stores(location=location,stock_id=stock_id)
            db.session.add(new_store)
            db.session.commit()   

        
    return render_template('createstore.html')

@views.route('/createWarehouse', methods=['POST','GET'])
def create_warehouse():
    if request.method=='POST':
        location = request.form.get('location')
        name=request.form.get('name')
        
        warehouse = Warehouses.query.filter_by(location=location).first()
        if warehouse:
            pass
            #flash('Warehouse already exists',category='error')
        else:          
            new_warehouse=Warehouses(location=location,name=name)
            db.session.add(new_warehouse)
            db.session.commit()   
    return render_template('createwarehouse.html')

@views.route('/createProduct',methods=['POST','GET'])   
def create_product():
    if request.method=='POST':
        name = request.form.get('name')
        price = request.form.get('price')
        type = request.form.get('type')
        manufacturer_name = request.form.get('manufacturer')
        description= request.form.get('description')
        
        manufacturer = Manufacturers.query.filter_by(name=manufacturer_name).first()
        if not manufacturer:
            new_manufacturer=Manufacturers(name=manufacturer_name)
            db.session.add(new_manufacturer)
            manufacturer=Manufacturers.query.filter_by(name=manufacturer_name).first()
        manufacturer_id=manufacturer.id   
        new_product=Products(name=name,price=price,type=type,description=description,manufacturer_id=manufacturer_id)        
        db.session.add(new_product) 
        db.session.commit()
    return render_template('createproduct.html')

#READ
@views.route('/customers')
def customers():
    return render_template('customers.html', Customers=Customers.query.all())

# @views.route('/customer/<id>',methods=['POST'])
# def customer(id):
#     customer=Customers.query.filter_by(id=id).first()

#     return render_template('customer.html', customer=customer)

@views.route('/staff')
def staff():
    return render_template('staff.html', Staff=Users.query.all())



@views.route('/orders')
def orders():
    return render_template('orders.html', Orders=Orders.query.all())


@views.route('/products')
def products():
    return render_template('products.html', Products=Products.query.all())


@views.route('/stores')
def stores():
    return render_template('stores.html', Stores=Stores.query.all())

@views.route('/stores/<id>')
def store(id):
    store=Stores.query.filter_by(id=id).first()
    stock=store.products
    return render_template('stock.html', )

@views.route('/warehouses')
def warehouses():
    return render_template('warehouses.html', Warehouses=Warehouses.query.all())    

@views.route('/warehouses/<id>')
def warehouse(id):
    warehouse=Warehouses.query.filter_by(id=id).first()
    Stock=warehouse.stock
    return render_template('stock.html',Stock=Stock )


#UPDATE
# @views.route('/customer/<id>',methods=['POST'])
# def customer(id):
#     customer=Customers.query.filter_by(id=id).first()

#     return render_template('customer.html', customer=customer)


@views.route('/staff/<id>')
def employee(id):
    employee=Users.query.filter_by(id=id).first()
    return render_template('employee.html', employee=employee)

@views.route('/product/<id>')
def product(id):
    product=Products.query.filter_by(id=id).first()
    return render_template('product.html', product=product)

@views.route('/orders/<id>')
def order(id):
    order=Orders.query.filter_by(id=id).all()
    return render_template('order.html', order=order)



#DELETE    
@views.route('/delete_customer/<id>')
def delete_customer(id):
    customer=Customers.query.filter_by(id=id).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()

    return render_template('customers.html', Customers=Customers.query.all())    

@views.route('/delete_product/<id>')
def delete_product(id):
    product=Products.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
    return render_template('products.html', Products=Products.query.all())

@views.route('/delete_warehouses/<id>')
def delete_warehouse(id):
    warehouse=Warehouses.query.filter_by(id=id).first()
    if warehouse:
        db.session.delete(warehouse)
        db.session.commit()
    return render_template('warehouses.html',Warehouses=Warehouses.query.all())

@views.route('/delete_staff/<id>')
def delete_staff(id):
    staff=Users.query.filter_by(id=id).first()
    if staff:
        db.session.delete(staff)
        db.session.commit()
    return render_template('staff.html', staff=Users.query.all())