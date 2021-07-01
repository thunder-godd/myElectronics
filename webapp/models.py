from sqlalchemy.orm import backref
from . import db 
from datetime import datetime

class Products(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000))
    price=db.Column(db.Integer)
    type=db.Column(db.String(1000))
    description=db.Column(db.Text)
    quantity=db.Column(db.Integer,default=0)
    in_stock=db.Column(db.Boolean,default=False)
    image=db.Column(db.String(150), nullable=False, default='img.jpg')
    date_created=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    manufacturer_id=db.Column(db.Integer,db.ForeignKey('manufacturers.id'))
    manufacturer=db.relationship('Manufacturers')
    store_id=db.Column(db.Integer,db.ForeignKey('stores.id'))
    store=db.relationship('Stores')
    warehouse_id=db.Column(db.Integer,db.ForeignKey('warehouses.id'))
    warehouse=db.relationship('Warehouses')

    def update_stock(self):
        if self.quantity > 0:
            self.in_stock=True
        else:
             self.in_stock=False   

class Customers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name =db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    type= db.Column(db.String(150))
    contract=db.relationship('Contract_customers', backref='customers')
    credit=db.relationship('Credit_customers', backref='customers')
    orders=db.relationship('Orders', backref='customers')

class Contract_customers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'))
    customer=db.relationship('Customers')
    billing_number=db.Column(db.String(150),nullable=False,unique=True)

class Credit_customers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),primary_key=True)
    customer=db.relationship('Customers')
    card_number=db.Column(db.String(150),nullable=False,unique=True)

class Orders(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.String(1000), db.ForeignKey('customers.id'))
    customer=db.relationship('Customers')
    product_id=db.Column(db.String(1000), db.ForeignKey('products.id'))
    product=db.relationship('Products')
    date_ordered=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    delivered=db.Column(db.Boolean,default=False)
    delivery=db.relationship('Deliveries', backref='orders')
    
    

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name =db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    type=db.Column(db.String(150))
    managers=db.relationship('Managers',backref='users')
    customer_service_staff=db.relationship('Customer_service_staff',backref='users')
    call_center_staff=db.relationship('Call_center_staff',backref='users')
    stocking_clerks=db.relationship('Stocking_clerks',backref='users')
    admin=db.relationship('Admin',backref='users')
    marketing_staff=db.relationship('Marketing_staff',backref='users')

class Warehouses(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000),unique=True)
    location=db.Column(db.String(1000))
    capacity=db.Column(db.String(1000))
    manager_id=db.Column(db.Integer,db.ForeignKey('managers.id'))
    manager=db.relationship('Managers')
    products=db.relationship('Products', backref='warehouses')
    


class Sales(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey('products.id'))
    product=db.relationship('Products')
    location=db.Column(db.String(100))


class Deliveries(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'))
    order=db.relationship('Orders')
    tracking_number=db.Column(db.String(100),nullable=False,unique=True)
    company=db.Column(db.String(150))
    date_delivered=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users')

class Managers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users')
    store=db.relationship('Stores' ,backref='Managers')
    warehouse=db.relationship('Warehouses', backref='managers')

class Call_center_staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users') 

class Customer_service_staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users')    

class Stocking_clerks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users')

class Marketing_staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user=db.relationship('Users')       

class Manufacturers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    product=db.relationship('Products',backref='manufacturers')
 
class Stores(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String(1000))
    location=db.Column(db.String(1000))
    manager_id=db.Column(db.Integer,db.ForeignKey('managers.id'))
    manager=db.relationship('Managers')
    products=db.relationship('Products', backref='stores')
    
