
from .__init__ import app
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, create_engine, Boolean, MetaData, Unicode

try:   
    engine = create_engine("mysql://root:@localhost/")
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database puncys_store_1;")
    conn.close()
except Exception as e:
    print("An error occurred, error details:\n---------------------\n{}\n---------------------\n".format(e))

try:
    engine = create_engine(app.config['DATABASE_URI'], echo = False)
except Exception as e:
    print("An error occurred, error details:\n---------------------\n{}\n---------------------\n".format(e))
    exit(1)
meta = MetaData()


def query(sql):
    print("Query: '{}'".format(sql))
    results = "An error occurred.\n"
    with engine.connect() as connection:
        try:
            results = connection.execute(sql)
        except Exception as e:
            
            print("An error occurred, error details:\n---------------------\n{}\n---------------------\n".format(e))
    return results

appointments = Table(
    'appointments', meta,
    Column('user_id', Unicode(5)),
    Column('app_date', String(10)),
    Column('app_time', String(5)),
    Column('app_status', String(1)),
    Column('app_id', Integer, primary_key = True),
)

bills = Table(
    'bills', meta,
    Column('bill_id', Integer, primary_key = True),
    Column('user_id', Unicode(5)),
    Column('order_id', Integer),
    Column('job_type', String(12)),
    Column('fabric_cost', Float),
    Column('labour_cost', Float),
    Column('date_completed', String(10)), # Probably gonna want to make this not-null at some point...
)

job_presets = Table(
    'job_presets', meta,
    Column('preset_id', Integer, primary_key = True),
    Column('type', String(12)),
    Column('garment_price', Float),
    #Column('media_address', String),
)

logins = Table(
    'logins', meta,
    Column('user_id', Unicode(5), primary_key = True),
    Column('email', String(40)),
    Column('password_hash', String(95)),
    Column('salt', Integer),
    Column('is_active', Boolean)
)

measurements = Table(
    'measurements', meta,
    Column('measurement_id', Integer, primary_key = True),
    Column('user_id', Unicode(5)),
    Column('job_type', String(12)),
    Column('name', String(12)),
    Column('length', Integer),
    Column('hip', Integer),
    Column('waist', Integer),
    Column('ankle', Integer),
    Column('round_leg', Integer),
    Column('round_ankle', Integer),
    Column('bust', Integer),
    Column('sleeve', Integer),
    Column('bicep', Integer),
    Column('armhole', Integer),
    Column('neck', Integer),
    Column('shoulder', Integer),
    Column('across_back', Integer),
    Column('bust_point', Integer),
    Column('round_knee', Integer),
)

orders = Table(
    'orders', meta,
    Column('order_id', Integer, primary_key = True),
    Column('user_id', Unicode(5)),
    Column('first_name', String(10)),
    Column('last_name', String(10)),
    Column('state', String(1)),
    Column('contact_num', String(14)),
    Column('delivery_address', String(40)),
    Column('type', String(12)),
    Column('measurement_id', Integer),
    Column('date_placed', String(10)),
    Column('due_date', String(10)),
    Column('media_address', String(30)),
    Column('est_cost', Float),
    Column('providing_fabric', Boolean),
)

users = Table(
    'users', meta,
    Column('user_id', Unicode(5), primary_key = True),
    Column('first_name', String(12)),
    Column('last_name', String(12)),
    Column('tele_num', String(14)),
    Column('home_address', String(40)),
    Column('email', String(40)),
    Column('dob', String(10)),
    Column('profile_pic_address', String(30)),
    Column('clearance', Integer),
)

meta.create_all(engine)
print()