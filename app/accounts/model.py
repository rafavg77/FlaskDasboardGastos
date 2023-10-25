from app import db
import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    transactions = db.relationship('Transaction', backref='user', lazy=True)