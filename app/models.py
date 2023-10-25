from flask_login import UserMixin
from app import db
import datetime
from .accounts.model import Account
from .transactions.transaction_model import Transaction

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    accounts = db.relationship('Account', backref='user', lazy=True)
    #transactions = db.relationship('Transaction', backref='user', lazy=True)