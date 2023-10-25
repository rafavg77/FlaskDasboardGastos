from app import db
import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    description = db.Column(db.String(255))
    ingress = db.Column(db.Float(precision=2))
    engress = db.Column(db.Float(precision=2))
    comment = db.Column(db.String(255))
    status = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())