"""
Based on https://github.com/UCLComputerScience/comp0034_flask_login_complete
Adapted by 17075800
"""
from os.path import dirname, abspath, join


class Config(object):
    """Set Flask base configuration"""
    # CSRF_ENABLED = True
    # Secret key was randomly created using a Python console and enter 'import secrets' and then 'secrets.token_urlsafe(16)'
    SECRET_KEY = '7A0PSeGv1XcyeHEHIuO5Yw'

    # General Config
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = False

    # Forms config
    # Generated using the same method as the SECRET_KEY
    WTF_CSRF_SECRET_KEY = '2hrd55pCkFuyyIX5IoQ0Ag'

    # Database config
    CWD = dirname(abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(CWD, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    # The following are fictitious details for a MySQL server database! Included to illustrate the syntax.
    DB_SERVER = '192.168.19.32'
    SQLALCHEMY_DATABASE_URI = 'mysql://user@{}/foo'.format(DB_SERVER)
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevConfig(Config):
    DEBUG = True
