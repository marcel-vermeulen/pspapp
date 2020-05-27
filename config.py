import os
from os import environ
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # APP MODE
    DEBUG = True

    # Top secret of website
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(12)
    #SECRET_KEY = os.urandom(12)

    # Database configuration
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('DATABASE_USER'),
        environ.get('DATABASE_PASSWORD'),
        environ.get('DATABASE_HOST'),
        environ.get('DATABASE_PORT'),
        environ.get('DATABASE_NAME')
    )
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Bootstrap using local static files
    BOOTSTRAP_SERVE_LOCAL = True

    # Mail Configuration
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

    # ADMINS
    ADMINS = environ.get('ADMINS')

    # IPAM Configuration
    IPAM_HOST = environ.get('IPAM_HOST')
    IPAM_PORT = environ.get('IPAM_PORT')
    IPAM_MAXIPS = environ.get('IPAM_MAXIPS')

class TestConfig(Config):

    # Test Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
