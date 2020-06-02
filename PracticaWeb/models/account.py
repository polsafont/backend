from db import db


class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    username = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = db.Column(db.Integer, nullable=False)
    available_money = db.Column(db.Integer)
    orders = db.relationship('OrdersModel', backref='orders', lazy=True)

    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin
        self.password = 'test'

    def json(self):
        data = {
            'username' : self.username,
            'is_admin' : self.is_admin
        }
        return data
