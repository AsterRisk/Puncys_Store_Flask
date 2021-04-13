import os
import sys

class Config():
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '18078bdd7193ed2a57674fd5e65c446e2ba9664e7008fe54ad02a58c9a622e53'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'root'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or ''
    DEBUG = True
    PORT = 5000
    TEMPLATE_FOLDER = '../templates/'
    STATIC_FOLDER = '/static/'
    IMAGE_FOLDER = "/images/"
    SERVER_ADDRESS = 'localhost' #os.environ.get('IP_ADDRESS') or 'localhost'
    DATABASE_URI = "mysql://{}:{}@{}/puncys_store_1".format(ADMIN_USERNAME, ADMIN_PASSWORD, SERVER_ADDRESS)
    MAIL_SERVER ='smtp.mailtrap.io'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 2525
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'f58511aba1b433'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '9dcc85a8d8ecd9'
    DEFAULT_SENDER = "puncysstore@gmail.com"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class DevConfig(Config):
    DEBUG = False
    DEVELOPMENT = True

class ProdConfig(Config):
    DEBUG = False