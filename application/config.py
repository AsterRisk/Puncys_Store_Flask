import os
import sys

class Config():
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '18078bdd7193ed2a57674fd5e65c446e2ba9664e7008fe54ad02a58c9a622e53'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'root'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or ''
    TEMPLATE_FOLDER = '/templates/'
    STATIC_FOLDER = '/static/'
    SERVER_ADDRESS = 'localhost' #os.environ.get('IP_ADDRESS') or 'localhost'
    DATABASE_URI = "mysql://{}:{}@{}/puncys_store_1".format(ADMIN_USERNAME, ADMIN_PASSWORD, SERVER_ADDRESS)

class DevConfig(Config):
    DEBUG = False
    DEVELOPMENT = True

class ProdConfig(Config):
    DEBUG = False