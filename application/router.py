from flask import Flask, redirect, url_for, request, make_response, render_template, render_template_string
from forms import LoginForm, AppointmentForm, RegistrationForm, OrderForm
from setup import query

app = Flask(__name__,
            template_folder="../templates/",
            static_folder="../static/"
            )
app.config['DATABASE_URI'] = 'mysql://root:@localhost/puncys_store_1' # Database connection, don't touch this
app.config['SECRET_KEY'] = '18078bdd7193ed2a57674fd5e65c446e2ba9664e7008fe54ad02a58c9a622e53'
app.debug = True # Outputs statements to terminal, makes it easier to see what's going on

@app.route("/", methods = ['POST', 'GET']) # Login page. POST returns the form, POST attempts to login the
                                           # user with the information provided 
# templates\Login_v1\login.html <-- Relative path
def login():
    form = LoginForm()
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        #headers = {'Content-Type': "application/json"}
        return make_response(render_template("login.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return make_response(render_template("register.html", form = form), 200)
    else:
        return make_response("Invalid Request Method.", 400)

@app.route("/home", methods = ['GET'])
# templates\home_page\html\home.html <-- Relative path
def home():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/order", methods = ['POST', 'GET'])
def order():
    """ job_types = query("SELECT type from job_presets;")
    user_measurements = query("SELECT * from measurements where user_id = {};".format(1)) """
    form = OrderForm(data = {'session_id': 1})
    
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        make_response(render_template("order.html", form = form, session_id = 1, query = query), 200)
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/bills", methods = ['POST', 'GET'])
def bill():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/appointments", methods = ['POST', 'GET'])
def appointment():
    form = AppointmentForm()
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass

@app.route("/sales_report", methods = ['POST', 'GET'])
def sales_report():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return make_response("Invalid Request Method.", 400)
    pass