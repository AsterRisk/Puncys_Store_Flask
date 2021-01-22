from flask_sqlalchemy import SQLAlchemy
from setup import query, appointments, bills, job_presets, logins, measurements, users, orders
from router import app

db = SQLAlchemy(app)

# --DATABASE MODELS--
#  
# Fancy word for tables, represent the actual SQL tables on the database
# USAGE of these models [appointments table referenced as example]:
# || INSERT :: ins = appointments.insert().values(user_id = <id>, app_date = <date>, ...) 
# || Calling str() on ins will return the actual SQL statement but it won't show the parameters
# || ins.compile().params <-- this will return a dictionary that shows the column names and the values being edited
# || DELETE, UPDATE, SELECT also have similar methods. 
# || Note: It is possible to call insert with multiple dictionaries to insert many records at once:
#        ins = appointments.insert().values([
#           {'user_id': 1, 'app_time':'9:00', 'app_date': '10/01/2021', 'status':"Pending", 'app_id': 2}
#           {'user_id': 2, 'app_time':'9:00', 'app_date': '10/02/2021', 'status':"Pending", 'app_id': 3}
#           {'user_id': 3, 'app_time':'9:00', 'app_date': '10/03/2021', 'status':"Pending", 'app_id': 4}
#           {'user_id': 4, 'app_time':'9:00', 'app_date': '10/04/2021', 'status':"Pending", 'app_id': 5}
# ||     ])

# || SELECT :: sql = appointments.select().where(<conditions>)
# || Equivalent to "SELECT * from appointments where <conditions>;" 

# || UPDATE :: sql = appointments.update().where(<conditions>)
# || Equivalent to "UPDATE appointments <update> where <conditions>;"

# || DELETE :: sql = appointments.delete().where(<conditions>)
# || Equivalent to "DELETE from appointments where <conditions>;"

# || After each of these, to execute the query, call query(sql). 
# || Pro tip, naming the variable sql some variant of what the statement is doing will make it easier to
# || remember what it's for further down the line

# || results.fetchone()  <-- returns the next row in the resultant table
# || for row in results: <-- goes through each row in the resultant table, each row is a dictionary with keys === column names in the result

class Appointment(db.Model):

    user_id = db.Column('user_id', db.Integer)
    app_date = db.Column('app_date', db.String(10))
    app_time = db.Column('app_time', db.String(5))
    app_status = db.Column('app_status', db.String(12))
    app_id = db.Column('app_id', db.Integer, primary_key = True)

    def __init__(self, user_id, date, time):
        self.user_id = user_id
        self.app_time = time
        self.app_date = date
        self.app_status = "P"
        
        ins = appointments.insert().values(user_id = self.user_id, app_time = self.app_time, app_date = self.app_date, app_id = self.app_id, app_status = self.app_status)
        query(ins)

class Bill(db.Model):
    user_id = db.Column('user_id', db.Integer)
    bill_id = db.Column('bill_id', db.Integer, primary_key = True)
    order_id = db.Column('order_id', db.Integer)
    job_type = db.Column('job_type', db.String)
    fabric_cost = db.Column('fabric_cost', db.Float)
    labour_cost = db.Column('labour_cost', db.Float)
    date_completed = db.Column('date_completed', db.String(10))

    def __init__(self, user_id, bill_id, order_id, job_type, fabric_cost, labour_cost, date_completed):
        self.user_id = user_id
        self.order_id = order_id
        self.job_type = job_type
        self.fabric_cost = fabric_cost
        self.labour_cost = labour_cost
        self.date_completed = date_completed

        ins = bills.insert().values(user_id = self.user_id, order_id = self.order_id, job_type = self.job_type, fabric_cost = self.fabric_cost, labour_cost = self.labour_cost, date_completed = self.date_completed)
        query(ins)

class JobPreset(db.Model):
    preset_id = db.Column('preset_id', db.Integer, primary_key = True)
    job_type = db.Column('type', db.String)
    garment_price = db.Column('garment_price', db.Float)

    def __init__(self, preset_id, job_type, garment_price):
        self.preset_id = preset_id
        self.job_type = job_type
        self.garment_price = garment_price

        ins = job_presets.insert().values(preset_id = self.preset_id, job_type = self.job_type, garment_price=self.garment_price)
        query(ins)

class Login(db.Model):
    email = db.Column('email', db.String)
    user_id = db.Column('user_id', db.Integer, primary_key = True)
    password_hash = db.Column('password_hash', db.String)
    salt = db.Column('salt', db.Integer)

    def __init__(self, email, user_id, password_hash, salt):
        self.email = email
        self.user_id = user_id
        self.password_hash = password_hash
        self.salt = salt

        ins = logins.insert().values(email = self.email, user_id = self.user_id, password_hash = self.password_hash, salt = self.salt)
        query(ins)

class Measurement(db.Model):
    measurement_id = db.Column('measurement_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer)
    job_type = db.Column('job_type', db.String)
    name = db.Column('name', db.String)
    
    length = db.Column('length', db.String)
    hip = db.Column('hip', db.String)
    waist = db.Column('waist', db.String)
    ankle = db.Column('ankle', db.String)
    round_leg = db.Column('round_leg', db.String)
    round_ankle = db.Column('round_ankle', db.String)
    bust = db.Column('bust', db.String)
    sleeve = db.Column('sleeve', db.String)
    bicep = db.Column('bicep', db.String)
    armhole = db.Column('armhole', db.String)
    neck = db.Column('neck', db.String)
    shoulder = db.Column('shoulder', db.String)
    across_back = db.Column('across_back', db.String)
    bust_point = db.Column('bust_point', db.String)
    round_knee = db.Column('round_knee', db.String)

    def __init__(self, user_id, job_type, name, length = None, waist = None, hip = None, ankle = None, round_leg = None, round_ankle = None, bust = None, sleeve = None, bicep = None, armhole = None, neck = None, shoulder = None, across_back = None, bust_point = None, round_knee = None):
        self.user_id = user_id
        self.job_type = job_type
        self.name = name
        self.length = length
        self.hip = hip
        self.waist = waist
        self.ankle = ankle
        self.round_leg = round_leg
        self.round_ankle = round_ankle
        self.bust = bust
        self.sleeve = sleeve
        self.bicep = bicep
        self.armhole = armhole
        self.neck = neck
        self.shoulder = shoulder
        self.across_back = across_back
        self.bust_point = bust_point
        self.round_knee = round_knee

        ins = measurements.insert().values(user_id = self.user_id, job_type = self.job_type, name = self.name, length = self.length, hip = self.hip,\
                                           waist = self.waist, ankle = self.ankle, round_leg = self.round_leg, \
                                           round_ankle = self.round_ankle, bust = self.bust, bicep = self.bicep, armhole = self.armhole, \
                                           neck = self.neck, shoulder = self.shoulder, sleeve = self.sleeve,\
                                           across_back = self.across_back, bust_point = self.bust_point, round_knee = self.round_knee)
        query(ins)

class Order(db.Model):
    order_id = db.Column('order_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    state = db.Column('state', db.String)
    contact_num = db.Column('contact_num', db.String)
    delivery_address = db.Column('deliver_address', db.String)
    job_type = db.Column('type', db.String)
    measurement_id = db.Column('measurement_id', db.Integer)
    date_placed = db.Column('date_placed', db.String)
    due_date = db.Column('due_date', db.String)
    media_address = db.Column('media_address', db.String)
    est_cost = db.Column('est_cost', db.Float)
    providing_fabric = db.Column('providing_fabric', db.Boolean)

    def __init__(self, user_id, first_name, last_name, contact_num, delivery_address, job_type, measurement_id, date_placed, due_date, media_address, est_cost, providing_fabric):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.state = "P"
        self.contact_num = contact_num
        self.delivery_address = delivery_address
        self.job_type = job_type
        self.measurement_id = measurement_id
        self.date_placed = date_placed
        self.due_date = due_date
        self.media_address = media_address
        self.est_cost = est_cost
        self.providing_fabric = providing_fabric

        ins = orders.insert().values(user_id = self.user_id, first_name = self.first_name, last_name = self.last_name, state = self.state, \
                                            contact_num = self.contact_num, delivery_address = self.delivery_address, job_type = self.job_type, \
                                            measurement_id = self.measurement_id, date_placed = self.date_placed, due_date = self.due_date, \
                                            media_address = self.media_address, est_cost = self.est_cost, providing_fabric = self.providing_fabric)
        query(ins)

class User(db.Model):
    user_id = db.Column('user_id', db.Integer, primary_key = True)
    email = db.Column('email', db.String)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    tele_num = db.Column('tele_num', db.String)
    home_addr = db.Column('home_address', db.String)
    dob = db.Column('dob', db.String)
    profile_pic_address = db.Column('profile_pic_address', db.String)
    clearance = db.Column('clearance', db.Integer)

    def __init__(self, email, first_name, last_name, tele_num, home_addr, dob, ppa, clearance):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.tele_num = tele_num
        self.home_addr = home_addr
        self.dob = dob
        self.profile_pic_address = ppa
        self.clearance = clearance

        ins = users.insert().values(email = self.email, first_name = self.first_name, last_name = self.last_name, home_addr = self.home_addr, \
                                    tele_num = self.tele_num, dob = self.dob, profile_pic_address = self.profile_pic_address, \
                                    clearance = self.clearance)
        query(ins)
    