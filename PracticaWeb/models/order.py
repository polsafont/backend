from db import db


class OrdersModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), foreign_key='accounts.username', nullable=False)
    id_event = db.Column(db.Integer, nullable=False)
    tickets_bought = db.Column(db.Integer, nullable=False)

    def __init__(self, id_event, tickets_bought):
        self.id_event = id_event
        self.tickets_bought = tickets_bought

    def json(self):
        data = {
            'username': self.username,
            'is_admin': self.is_admin,
            'avaible_money': self.available_money
        }
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




