"""
Based on https://github.com/UCLComputerScience/comp0034_flask_login_complete and
https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
Adapted by 17075800
"""
from datetime import datetime as dt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# Handles the specific details of the User
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    user_type = db.Column(db.String(10), nullable=False)
    items = db.relationship('Item', backref='author', lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def __repr__(self):
        return "User email %s" % self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    
# Handles the specific details of the Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.now)
    content = db.Column(db.Text, nullable=False)
    color = db.Column(db.Text)
    size = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "item"}

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
