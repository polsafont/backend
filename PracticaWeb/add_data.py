from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.artist import ArtistModel
from models.event import EventModel
from models.account import AccountsModel
from models.order import OrdersModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


def init_db():
    db.drop_all()
    db.create_all()
    new_artist1 = ArtistModel(name="Bad Gyal", country="Spain", genre="TRAP")
    db.session.add(new_artist1)
    new_artist2 = ArtistModel(name="Txarango", country="Spain", genre="REGGAE")
    db.session.add(new_artist2)
    new_artist3 = ArtistModel(name="Estopa", country="Spain", genre="ROCK")
    db.session.add(new_artist3)
    new_artist4 = ArtistModel(name="Dvicio", country="Spain", genre="REGGAE")
    db.session.add(new_artist4)
    new_artist5 = ArtistModel(name="Iron Maiden", country="Spain", genre="ROCK")
    db.session.add(new_artist5)
    db.session.commit()

    new_event1 = EventModel("Canet Rock 2020", "Canet de Mar Beach", "Barcelona", "2020-07-05", 24, 100)
    new_event1.artists.append(new_artist2)
    new_event1.artists.append(new_artist4)
    db.session.add(new_event1)

    new_event2 = EventModel("Festival Cruilla 2020", "Parc del Forum", "Barcelona", "2020-07-07", 100, 100)
    new_event2.artists.append(new_artist1)
    new_event2.artists.append(new_artist2)
    new_event2.artists.append(new_artist3)
    db.session.add(new_event2)

    new_event3 = EventModel("Iron Maiden Tour", "Sant Jordi", "Barcelona", "2020-07-06", 70, 200)
    new_event3.artists.append(new_artist5)
    db.session.add(new_event3)
    db.session.commit()

    new_user1 = AccountsModel('tester', 500, 0)
    new_user1.hash_password('1234')  # 'username:'tester', password:'1234'
    db.session.add(new_user1)
    db.session.commit()

    new_user1 = AccountsModel('admin', 400, 1)
    new_user1.hash_password('admin')  # 'username:'admin', password:'admin'
    db.session.add(new_user1)
    db.session.commit()
