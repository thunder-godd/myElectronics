from flask import Blueprint,render_template,request, flash, redirect,url_for,session
from .models import Users,Customers,Contract_customers,Credit_customers
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
@auth.route('/customer_login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        customer = Customers.query.filter_by(email=email).first()
        if customer:
            if check_password_hash(customer.password, password):
                flash('Logged in successfully', category='success')
                login_user(customer,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('customer_login.html',customer=current_user)

@auth.route('/Admin',methods=['GET','POST'])
def Admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.adminDash'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('Staff_login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        customer_type = request.form.get('type')
        card_number= request.form.get('card_number')
        customer = Customers.query.filter_by(email=email).first()
        if customer:
            flash('Email already exists',category='error')
        elif  len(email) < 4:
            flash('email is too short', category='error')
        elif  len(first_name) < 1:
            flash('first Name is too short', category='error')
        elif  len(last_name) < 1:
            flash('last name is too short', category='error')
        elif  len(password1) < 8:
            flash('password too short', category='error')
        elif password2 != password1:
            flash('passwords do not match', category='error')
        elif  len(card_number) < 8:
            flash('Enter A valid Card Number', category='error')    
        else:
            new_customer=Customers(email=email,first_name=first_name, last_name=last_name,type=customer_type,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_customer)
           
            if customer_type=='Contract':
                customer = Customers.query.filter_by(email=email).first()
                contract_customer=Contract_customers(customer_id=customer.id,billing_number=card_number)
                db.session.add(contract_customer)
            elif customer_type=='Credit':
                customer = Customers.query.filter_by(email=email).first()
                credit_customer=Credit_customers(customer_id=customer.id,card_number=card_number)
                db.session.add(credit_customer)                   
            db.session.commit()
            login_user(customer,remember=True)
            flash('account created', category='success')
            return redirect(url_for('views.home'))
                   
    return render_template('sign_up.html',user=current_user)
