
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TimeField, SubmitField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from .setup import query

from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('email', validators = [DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField('password', validators = [DataRequired()], render_kw={"placeholder":"Password"})
    submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
    first_name = StringField('fname', validators = [DataRequired()], render_kw={"placeholder":"First Name"})
    last_name = StringField('lname', validators = [DataRequired()], render_kw={"placeholder":"Last Name"})
    email = StringField('email', validators = [DataRequired(), Email()], render_kw={"placeholder":"Email"})
    addr = StringField('addr', validators = [DataRequired()], render_kw={"placeholder":"Home Address"})
    telephone = StringField('tele', validators = [DataRequired()], render_kw={"placeholder":"Telephone Number"})
    dob = DateField('dob', validators = [DataRequired()], render_kw={"placeholder":"DOB"})
    password = PasswordField('password_1', validators = [DataRequired()], render_kw={"placeholder":"Password"})
    conf_password = PasswordField('password_2', validators = [DataRequired()], render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField('submit')

class AppointmentForm(FlaskForm):
    date = DateField('date', validators = [DataRequired()], render_kw={"placeholder":"Date"})
    time = TimeField('time', validators = [DataRequired()], render_kw={"placeholder":"Time"})
    submit = SubmitField('submit')

class OrderForm(FlaskForm):
    job_types = query("select type from job_presets;")
    """ def __init__(self):
    #    
    #    try:
    #        user_measurements = query("select * from measurements where user_id = {}".format(self.data['session_id']))
    #        print("----------------------------------\n")
    #        print(user_measurements)
    #        print("----------------------------------\n")
    #    except Exception as e:
    #        print("HELLLOOOO")
    #        print(e) """

    # || User Data
    fname      = StringField('fname', validators = [DataRequired()], render_kw={})
    lname      = StringField('lname', validators = [DataRequired()], render_kw={})
    tele       = StringField('tele', validators = [DataRequired()], render_kw={})
    addr       = StringField('addr', validators = [DataRequired()], render_kw={})
    due_date   = DateField('due-date', validators = [], render_kw={})

    # || Order Measurements
    length      = StringField('length', validators = [DataRequired()], render_kw={"value":0})
    hip         = StringField('hip', validators = [DataRequired()], render_kw={"value":0})
    waist       = StringField('waist', validators = [DataRequired()], render_kw={"value":0})
    across_back = StringField('across_back', validators = [DataRequired()], render_kw={"value":0})
    round_leg   = StringField('round_leg', validators = [DataRequired()], render_kw={"value":0})
    round_knee  = StringField('round_knee', validators = [DataRequired()], render_kw={"value":0})
    bust        = StringField('bust', validators = [DataRequired()], render_kw={"value":0})
    ankle       = StringField('ankle', validators = [DataRequired()], render_kw={"value":0})
    neck        = StringField('neck', validators = [DataRequired()], render_kw={"value":0})
    shoulder    = StringField('shoulder', validators = [DataRequired()], render_kw={"value":0})
    sleeve      = StringField('sleeve', validators = [DataRequired()], render_kw={"value":0})
    bicep       = StringField('bicep', validators = [DataRequired()], render_kw={"value":0})
    bust_point  = StringField('bust_point', validators = [DataRequired()], render_kw={"value":0})
    armhole     = StringField('armhole', validators = [DataRequired()], render_kw={"value":0})
    round_ankle = StringField('round_ankle', validators = [DataRequired()], render_kw={"value":0})

    # || Important Booleans
    need_appt     = BooleanField('need_appt', validators = [], render_kw={"selected-value":1, "default":"checked"})
    providing_fab = BooleanField('need_appt', validators = [], render_kw={"selected-value":1, "default":"checked"})
    new_meas      = BooleanField('new_meas', validators = [], render_kw={})

    # || Miscellaneous
    meas_name     = StringField('meas_name', validators = [], render_kw={})
    meas_select   = SelectField('meas_select', validators = [], render_kw={}, choices= [])
    job_type      = SelectField('job_type', validators = [DataRequired()], render_kw ={}, choices = (["Select a job type..."] + [job.type for job in job_types]))
    job_type_text = StringField('job_type_text', validators = [], render_kw = {})

    # || Submit
    submit = SubmitField('Submit')

    
    