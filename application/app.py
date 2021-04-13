from flask import Flask, redirect, url_for, request, make_response, render_template, render_template_string, session, flash, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from flask_mail import Message
from .models import Login, User, Order, Appointment, Measurement
from .forms import LoginForm, AppointmentForm, RegistrationForm, OrderForm, ChangeStateForm, FlaskForm
from .setup import query
from random import randint
import datetime
from .__init__ import app, login_manager, csrf, mail
from werkzeug.security import check_password_hash, generate_password_hash

import os

session = {}

def loginUser(user): # Developed by: 620122579
    print(user)
    user = query("select * from users where user_id = {};".format(user.user_id)).fetchone()
    session['user_id'] = user.user_id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['home_address'] = user.home_address
    session['email'] = user.email
    session['tele_num'] = user.tele_num
    session['DOB'] = user.dob
    session['clearance'] = user.clearance

def logoutUser(): # Developed by: 620122579
    session['user_id'] = None
    session['first_name'] = None
    session['last_name'] = None
    session['home_address'] = None
    session['tele_num'] = None
    session['email'] = None
    session['DOB'] = None
    session['clearance'] = None

def compare_dates(date1: str, date2: str): # Developed by: 620122579 #Expected input: Two dates in the format YYYY-MM-DD 
    # Returns -1 if date2 happens before date1, 0 if both dates are the same and 1 if date1 happens before date2
    # compare_dates("March 3rd 2021", "March 12th 2021") ==> 1
    # compare_dates("July 3rd 2021", "March 12th 2021") ==> -1 
    # compare_dates("March 12th 2021", "March 12th 2021") ==> 0 
    date1 = list(map(int, date1.split("-")))
    date2 = list(map(int, date2.split("-")))
    if (date1[0] < date2[0]):
        # If the year in date 1 is less than the year in date 2
        return 1
    elif (date1[0] > date2[0]):
        # If the year in date 2 is less than the year in date 1
        return -1
    # Both years are equal, so check months
    elif (date1[1] < date2[1]):
        # If the month in date 1 is less than the month in date 2
        return 1
    elif (date1[1] > date2[1]):
        # If the month in date 2 is less than the month in date 1
        return -1
    # Both months are equal, so check days
    elif (date1[2] < date2[2]):
        # If the day in date 1 is less than the day in date 2
        return 1
    elif (date1[2] > date2[2]):
        # If the day in date 2 is less than the day in date 1
        return -1
    # Both dates are equal, return 0
    else: 
        return 0

@app.route("/images/<filename>")
def get_file(filename: str):
    return send_from_directory(os.path.join(os.getcwd(), app.config['IMAGE_FOLDER']), filename)

def meas_dict(length, waist, hip, sleeve, bicep, armhole, neck, shoulder, \
            across_back, bust, bust_point, ankle, round_leg, round_knee, round_ankle):
    meas = {}
    # (measurement.length, measurement.waist, measurement.hip, measurement.sleeve, 
    # measurement.bicep, measurement.armhole, measurement.neck, measurement.shoulder, 
    # measurement.across_back, measurement.bust, measurement.bust_point, measurement.ankle, 
    # measurement.round_leg, measurement.round_knee, measurement.round_ankle)
    meas['length'] = length
    meas['waist'] = waist
    meas['hip'] = hip
    meas['sleeve'] = sleeve
    meas['bicep'] = bicep
    meas['armhole'] = armhole
    meas['neck'] = neck
    meas['shoulder'] = shoulder
    meas['across_back'] = across_back
    meas['bust'] = bust
    meas['bust_point'] = bust_point
    meas['ankle'] = ankle
    meas['round_leg'] = round_leg
    meas['round_knee'] = round_knee
    meas['round_ankle'] = round_ankle
    return meas

@app.route("/", methods = ['POST', 'GET']) # Login page. GET returns the form, POST attempts to login the
                                           # user with the information provided 
# Developed by: 620122579
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data:
                email = form.email.data
                user = query("Select * from logins where email = '{}';".format(email)).first()
                
                if(user == None):
                    flash("Login failed. No user with that email found.", "danger")
                    return redirect(url_for('login'))
                temp = (form.password.data + str(user.salt))
                
                if (user and check_password_hash(user.password_hash, temp)):
                    loginUser(user)
                    flash("Login successful!", "success")
                    return redirect(url_for('home'))
                else:
                    
                    flash("Login failed. Please check your credentials.", "danger")
                    return redirect(url_for('login'))
                    
        pass
    elif request.method == 'GET':
        #headers = {'Content-Type': "application/json"}
        return make_response(render_template("login.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/save_changes", methods = ["POST"])
# Developed by: 620122579
def save_changes():
    form = ChangeStateForm()
    if request.method == "POST":
        try:
            instructions = form.queries.data.split(";")
        except:
            flash("An error occurred. Please contact the system administrator.", "danger")
            return redirect(url_for('home'))
        table = instructions[0]
        if (table == "orders"):
            id_name = "order_id"
            obj = "order"
        if (table == "appointments"):
            id_name = "app_id"
            obj = "appointment"
        instructions = [ins for ins in instructions[1:] if (ins)]
        for instr in instructions:
            state_iD = instr.split("|")
            state = state_iD[0]
            iD = state_iD[1]
            order = query("select * from orders where order_id = {}".format(iD)).first()
            old_state = order['state']
            if(not(old_state == state)): # if a change was actually made
                query("UPDATE {0} SET state = '{1}' WHERE {2} = {3};".format(table, state, id_name, iD))
                msg = Message()
                msg.subject = "There's been an update to your order at Puncy's Store"
                msg.sender = app.config['DEFAULT_SENDER']
                order = query("select * from orders where order_id = {}".format(iD)).first()
                print("ORDER:\n")
                print(order, end = "\n\n")
                msg.html = render_template("update_mail.html", first_name = query("select first_name from users where user_id = {}".format(order['user_id'])).first()[0], obj = obj, new_state = state, params = order)
                cust_email = query("select email from users where user_id = {}".format(order['user_id'])).first()
                print(cust_email)
                msg.recipients = ["puncysstore@gmail.com", cust_email[0]]
                print(msg.recipients)
                mail.send(msg)
        flash("Changes made successfully!", "success")

        return redirect(url_for('home'))
    else:
        flash("Bad request method, redirecting...", "danger")
        return redirect(url_for('home'))

@app.route("/view_orders")
# Developed by: 620122579
def view_orders():
    """if (session['clearance'] == 0):
            pass
    else:
        flash("You do not have authority to view this page.", "danger")
        return redirect(url_for('home'))"""
    form = ChangeStateForm()
    form.queries.render_kw={"value":"orders;"}
    orders = query("select * from orders where state != 'C';").fetchall()
    measurements = {}
    for order in orders:
        measurement = query("SELECT * FROM measurements WHERE measurement_id = {}".format(order.measurement_id)).first()
        measurements[order.measurement_id] = meas_dict(measurement.length, measurement.waist, measurement.hip, measurement.sleeve, measurement.bicep, measurement.armhole, measurement.neck, measurement.shoulder, measurement.across_back, measurement.bust, measurement.bust_point, measurement.ankle, measurement.round_leg, measurement.round_knee, measurement.round_ankle)
    #measurements = [query("select * from measurements where measurement_id = {};".format(order.measurement_id)).first() for order in orders]
    print(measurements)
    return render_template("view_orders.html", orders = orders, measurements = measurements, form = form)

@app.route("/view_orders/<user_id>")
# Developed by: 620122579
def view_my_orders(user_id):
    # This is the view for a customer viewing their specific orders
    if not((session['user_id'] == user_id)):
        if session['clearance'] == 0:
            pass
        else:
            flash("You do not have authority to view this page.", "danger")
            return redirect(url_for('home'))

    
    orders = query("select * from orders where user_id = {};".format(user_id)).fetchall()
    measurements = [query("select * from measurements where measurement_id = {};".format(order.measurement_id)).fetchall() for order in orders]
    return render_template("view_orders.html", orders = orders, measurements = measurements)

@app.route("/logout")
# Developed by: 620122579
def logout():
    logoutUser()
    flash("You have been logged out", "danger")
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    
    return User.query.get(int(id))

@app.route("/register", methods = ['GET', 'POST'])
# Developed by: 620122579
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
            flash("Registration successful!", "success")
            
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful registration, please try again.", "danger")
            return make_response(render_template("register.html", form = form), 200)
    elif request.method == 'GET':
        return make_response(render_template("register.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)

@app.route("/home", methods = ['GET'])
#@login_required
# Developed by: 620122579
# templates\home_page\html\home.html <-- Relative path
def home():
    if request.method == 'GET':
        return make_response(render_template("home.html"), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/order", methods = ['POST', 'GET'])
#@login_required
# Developed by: 620122579
def order():
    """try:
        if(session['user_id'] == None):
            flash("You must log in to view this page. Please log in below.")
            return redirect(url_for('login'))
    except:
        flash("You must log in to view this page. Please log in below.")
        return redirect(url_for('login'))"""
    
    job_types = query("SELECT type from job_presets;")
    user_measurements = query("SELECT * from measurements where user_id = {};".format(1)).fetchall()
    measurements = [(measurement.measurement_id, (str((measurement.name, measurement.job_type)))) for measurement in user_measurements] 
    form = OrderForm()
    form.meas_select.choices= measurements
    try:
        user_id = session['user_id']
        if (user_id == None):
            flash("You must log in to view this page.", "danger")
            return redirect(url_for("login"))
    except:
        flash("You must log in to view this page.", "danger")
        return redirect(url_for("login"))
    if request.method == 'POST':
        
        first_name = form.fname.data
        last_name = form.lname.data
        contact_num = form.tele.data
        addr = form.addr.data
        typ = form.job_type.data
        
        date_placed = datetime.date.today().strftime("%Y-%m-%d")
        est_cost = int(query("select garment_price from job_presets where type = '{}'".format(typ)).first()[0])
        
        due_date = form.due_date.data.split("/")
        due_date = "{}-{}-{}".format(due_date[2], due_date[0],due_date[1])
        providing_fab = form.providing_fab.data
        if form.new_meas.data:
            new_measurement = Measurement(user_id = user_id, job_type = typ, name = form.meas_name.data, length = form.length.data, waist= form.waist.data,\
                hip = form.hip.data, ankle = form.ankle.data, round_leg= form.round_leg.data, round_ankle= form.round_ankle.data, bust = form.bust.data,\
                    sleeve = form.sleeve.data, bicep = form.bicep.data, armhole = form.armhole.data, neck = form.neck.data, shoulder = form.shoulder.data,\
                         across_back = form.across_back.data, bust_point= form.bust_point.data, round_knee = form.round_knee.data)
            measurement_id = query("select max(measurement_id) from measurements;").first()['max(measurement_id)']
        else:
            measurement_id = form.meas_select.data
        new_order = Order(user_id = user_id, first_name = first_name, last_name = last_name, contact_num = contact_num, delivery_address=addr, \
                            typ = typ, measurement_id=measurement_id, est_cost = est_cost, date_placed = date_placed, \
                            providing_fabric=form.providing_fab.data, due_date=due_date)
        msg = Message()
        job_typ = typ.split("-")
        size = job_typ[1]
        job_typ = job_typ[0]
        order_id = query("select max(order_id) from orders;").first()
        est_cost = query("SELECT est_cost from ORDERS WHERE order_id = {};".format(order_id[0])).first()
        msg.html = render_template("base_mail.html", first_name = session['first_name'], due_date = due_date, order_size = size, order_type= job_typ, est_cost = "{:.2f}".format((float(est_cost[0]))))
        msg.recipients = [session['email'], "puncysstore@gmail.com"]
        msg.sender = app.config['DEFAULT_SENDER']
        msg.subject = "Your clothing order has been received!"
        mail.send(msg)
        if(form.need_appt.data):
            flash("Order successful!", "success")
            return redirect(url_for('appointment'))
        else:
            flash("Order successful!", "success")
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return make_response(render_template("order.html", form = form, session_id = user_id, query = query), 200)
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
	try:
		user_id = session['user_id']
		if (user_id == None):
			flash("You must log in to view this page.", "danger")
			return redirect(url_for("login"))
	except:
		flash("You must log in to view this page.", "danger")
		return redirect(url_for("login"))
	form = AppointmentForm()
	if request.method == 'POST':
		appoint = Appointment(user_id,request.form['date'], request.form['time'])
		flash('Appointment was successfully made!', "success")
		return redirect('/home')
	elif request.method == 'GET':
		return make_response(render_template("appointment.html", form = form))
	else:
		return make_response("Invalid Request Method.", 400)

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