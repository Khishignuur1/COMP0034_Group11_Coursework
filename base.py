"""
Written by 17075800
tests was not being recognized as package so I have decided to put this here.
"""
from flask_testing import TestCase

from run import app


#Setting the config to Testconfig for unit tests
class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app
