from flask import Flask, redirect, url_for, request, make_response, render_template, render_template_string, session, flash
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from .models import Login, User, Order, Appointment, Measurement
from .forms import LoginForm, AppointmentForm, RegistrationForm, OrderForm
from .setup import query
from random import randint
import datetime
from .__init__ import app, login_manager, csrf
from werkzeug.security import check_password_hash, generate_password_hash

session = {}

def loginUser(user):
    print(user)
    user = query("select * from users where user_id = {};".format(user.user_id)).fetchone()
    session['user_id'] = user.user_id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['home_address'] = user.home_address

    session['tele_num'] = user.tele_num
    session['DOB'] = user.dob
    session['clearance'] = user.clearance

def logoutUser():
    session['user_id'] = None
    session['first_name'] = None
    session['last_name'] = None
    session['home_address'] = None
    session['tele_num'] = None
    session['DOB'] = None
    session['clearance'] = None


@app.route("/", methods = ['POST', 'GET']) # Login page. POST returns the form, POST attempts to login the
                                           # user with the information provided 
# templates\Login_v1\login.html <-- Relative path
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data:
                email = form.email.data
                user = query("Select * from logins where email = '{}';".format(email)).first()
                print(user)
                temp = (form.password.data + str(user.salt))
                print(temp)
                if (user and check_password_hash(user.password_hash, temp)):
                    loginUser(user)
                    flash("Login successful!")
                    return redirect(url_for('home'))
                else:
                    
                    print(check_password_hash(user.password_hash, temp))
                    flash("Login failed. Please check your credentials.", "danger")
                    print("Login failed. Please check your credentials.")
                    return redirect(url_for('login'))
                    
        pass
    elif request.method == 'GET':
        #headers = {'Content-Type': "application/json"}
        return make_response(render_template("login.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/logout")
def logout():
    logoutUser()
    flash("You have been logged out", "danger")
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print("POST REQUEST")
        #if form.validate_on_submit():
        #print("hey " + form.email.data)
        #print("hey " + form.first_name.data)
        #print("hey " + form.last_name.data)
        #print("hey " + form.addr.data)
        #print("hey " + form.password.data)
        #print("hey " + form.conf_password.data)
        if (form.password.data == form.conf_password.data):
            passw = form.password.data
            email = form.email.data
            tel = form.telephone.data
            addr = form.addr.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            dob = form.dob.data
            salt = randint(0, 9999)
            ID = query("SELECT count(user_id) from Users;").first()[0] +1
            new_user = User(email = email, first_name = first_name, last_name=last_name, home_address=addr, dob=dob, tele_num=tel, clearance=2, ppa= None, id = str(ID))
            
            
            print("ID: {}".format(ID))
            new_login = Login(email = email, password = form.password.data, salt = salt, user_id = ID)
            tables = query("show tables;")
            print(tables.fetchall())
            user = query("SELECT * from logins where email = '{}';".format(email)).fetchone()
            #user = Login.query.filter_by(email = email).first()
            print(user)
            
            loginUser(user)
            flash("Registration successful!")
            
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful registration, please try again.")
            return make_response(render_template("register.html", form = form), 200)
    elif request.method == 'GET':
        return make_response(render_template("register.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)

@app.route("/home", methods = ['GET'])
#@login_required
# templates\home_page\html\home.html <-- Relative path
def home():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return make_response(render_template("home.html"), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/order", methods = ['POST', 'GET'])
#@login_required
def order():
    """ job_types = query("SELECT type from job_presets;")
    user_measurements = query("SELECT * from measurements where user_id = {};".format(1)) """
    form = OrderForm()
    try:
        if(session['user_id'] == None):
            flash("You must log in to view this page. Please log in below.")
            return redirect(url_for('login'))
    except:
        flash("You must log in to view this page. Please log in below.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        first_name = form.fname.data
        last_name = form.lname.data
        contact_num = form.tele.data
        addr = form.addr.data
        typ = form.job_type.data
        measurement_id = 1
        date_placed = datetime.date.today().strftime("%Y-%m-%d")
        est_cost = 5000
        providing_fab = form.providing_fab.data
        if form.new_meas.data:
            new_measurement = Measurement(user_id = user_id, job_type = typ, name = form.meas_name.data, length = form.length.data, waist= form.waist.data,\
                hip = form.hip.data, ankle = form.ankle.data, round_leg= form.round_leg.data, round_ankle= form.round_ankle.data, bust = form.bust.data,\
                    sleeve = form.sleeve.data, bicep = form.bicep.data, armhole = form.armhole.data, neck = form.neck.data, shoulder = form.shoulder.data,\
                         across_back = form.across_back.data, bust_point= form.bust_point.data, round_knee = form.round_knee.data)
        new_order = Order(user_id = user_id, first_name = first_name, last_name = last_name, contact_num = contact_num, delivery_address=addr, \
                            typ = typ, measurement_id=measurement_id, est_cost = est_cost, date_placed = date_placed, \
                            providing_fabric=form.providing_fab.data)
        if(form.need_appt.data):
            return redirect(url_for('appointment'))
        else:
            flash("Order successful!")
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return make_response(render_template("order.html", form = form, session_id = 1, query = query), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/bills", methods = ['POST', 'GET'])
#@login_required
def bill():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/appointments", methods = ['POST', 'GET'])
#@login_required
def appointment():
    form = AppointmentForm()
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return "<h1>APPOINTMENT FORM</h1>"
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/sales_report", methods = ['POST', 'GET'])
#@login_required
def sales_report():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass