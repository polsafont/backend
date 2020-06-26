from models.artist import ArtistModel
from models.event import EventModel
from models.account import AccountsModel, auth, verify_password
from models.order import OrdersModel

from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from flask_cors import CORS
from flask import render_template

from db import db, secret_key

app = Flask(__name__,
            static_folder="../../vuefrontend/dist/static",
            template_folder="../../vuefrontend/dist")

app.config.from_object(__name__)

api = Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = secret_key

migrate = Migrate(app, db)
db.init_app(app)


# from add_data import init_db
# init_db()

@app.route('/')
def render_vue():
    return render_template('index.html')


class Artist(Resource):
    def get(self, id):
        try:
            artist = ArtistModel.find_by_id(id)
            return {'artist': artist.json()}, 200
        except:
            return {"message": "Error Get Artist"}, 500

    @auth.login_required(role='admin')
    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('genre', type=str, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            artist = ArtistModel(data['name'], data['country'], data['genre'])
            ArtistModel.save_to_db(artist)
            return {"message": "Artist anadido correctamente"}, 200
        except:
            return {"message": "Error Post Artist"}, 500

    @auth.login_required(role='admin')
    def delete(self, id):
        try:
            artist = ArtistModel.find_by_id(id)
            ArtistModel.delete_from_db(artist)
            return {"message": "Artist eliminado correctamente"}, 200
        except:
            return {"message": "Error Delete Artist"}, 500

    @auth.login_required(role='admin')
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('genre', type=str, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            artist = ArtistModel.find_by_id(id)
            artist.set_artist(data['name'], data['country'], data['genre'])
            ArtistModel.save_to_db(artist)
            return {"message": "Artist modificado correctamente"}, 200
        except:
            return {"message": "Error Put Artist"}, 500


class Event(Resource):
    def get(self, id):
        try:
            event = EventModel.find_by_id(id)
            return event.json(), 200
        except:
            return {"message": "Error Get Event"}, 500

    @auth.login_required(role='admin')
    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('place', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('date', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('price', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('total_available_tickets', type=int, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            event = EventModel(data['name'], data['place'], data['city'], data['date'], data['price'],
                               data['total_available_tickets'])
            EventModel.save_to_db(event)
            return {"message": "Event anadido correctamente"}, 200
        except:
            return {"message": "Error Post Event"}, 500

    @auth.login_required(role='admin')
    def delete(self, id):
        try:
            event = EventModel.find_by_id(id)
            EventModel.delete_from_db(event)
            return {"message": "Event eliminado correctamente"}, 200
        except:
            return {"message": "Error Delete Event"}, 500

    @auth.login_required(role='admin')
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('place', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('date', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('price', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('total_available_tickets', type=int, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            event = EventModel.find_by_id(id)
            event.set_event(data['name'], data['place'], data['city'], data['date'], data['price'],
                            data['total_available_tickets'])
            EventModel.save_to_db(event)
            return {"message": "Event modificado correctamente"}, 200
        except:
            return {"message": "Error Put Event"}, 500


class ArtistList(Resource):
    def get(self):
        data = {'artists': []}
        artists = ArtistModel.get_all()
        for a in artists:
            data['artists'].append(a.json())

        return data


class EventList(Resource):
    def get(self):
        data = {'events': []}
        events = EventModel.get_all()
        for a in events:
            data['events'].append(a.json())

        return data


class EventArtistsList(Resource):
    def get(self, id):
        event = EventModel.find_by_id(id)
        artists = EventModel.get_artists(event)
        data = {'artists': []}
        for a in artists:
            data['artists'].append(a.json())

        return data


class EventArtist(Resource):
    def get(self, id_event, id_artist):
        event = EventModel.find_by_id(id_event)
        artists = EventModel.get_artists(event)
        for a in artists:
            if a.id == int(id_artist):
                return {'event': event.json(), 'artist': a.json()}, 200

        return {"message": "Error Get EventArtist"}, 500

    @auth.login_required(role='admin')
    def post(self, id_event):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('genre', type=str, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            event = EventModel.find_by_id(id_event)
            artist = ArtistModel(data['name'], data['country'], data['genre'])
            ArtistModel.save_to_db(artist)

            event.artists.append(artist)
            EventModel.save_to_db(event)
            return {"message": "Artista anadido correctamente al evento"}, 200

        except:
            return {"message": "Error Post EventArtist"}, 500

    @auth.login_required(role='admin')
    def delete(self, id_event, id_artist):
        try:
            event = EventModel.find_by_id(id_event)
            artists = EventModel.get_artists(event)
            for a in artists:
                if a.id == int(id_artist):
                    event.artists.remove(a)
            EventModel.save_to_db(event)

            return {"message": "Artista eliminado correctamente del event"}, 200
        except:
            return {"message": "Error Delete EventArtist"}, 500


class ArtistEventsList(Resource):
    def get(self, id):
        artist = ArtistModel.find_by_id(id)
        events = EventModel.find_by_artist(id)

        return events


class Orders(Resource):
    def get(self, username):
        try:
            data = {'orders': []}
            orders = OrdersModel.find_by_username(username)
            for o in orders:
                data['orders'].append(o.json())

            return data, 200
        except:
            return {"message": "User not found"}, 404

    @auth.login_required(role='user')
    def post(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('tickets_bought', type=int, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            account = AccountsModel.find_by_username(username)
            event = EventModel.find_by_id(data['event_id'])

            total_available_tickets = event.total_available_tickets
            available_money = account.available_money
            price_ticket = event.price
            if username == g.user.username:
                if total_available_tickets >= data['tickets_bought']:
                    if available_money >= price_ticket:
                        event.set_tickets_free(total_available_tickets - 1)
                        account.set_available_money(available_money - (price_ticket * data['tickets_bought']))
                    else:
                        return {"message": "Error Post Order(dinero insuficiente)"}, 500
                else:
                    return {"message": "Error Post Order(no hay tickets disponibles)"}, 500
            else:
                return {"message": "Error token invalid, doesn't match user name"}, 400

            order = OrdersModel(data['event_id'], data['tickets_bought'])
            account.orders.append(order)

            EventModel.save_to_db(event)
            AccountsModel.save_to_db(account)
            OrdersModel.save_to_db(order)
            return {"order": order.json()}, 201
        except:
            return {"message": "Error Post Order"}, 500


class OrdersList(Resource):
    @auth.login_required(role='admin')
    def get(self):
        data = {'events': []}
        events = EventModel.get_all()
        for a in events:
            data['events'].append(a.json())

        return data, 200


class Accounts(Resource):
    @auth.login_required(role='user')
    def get(self, username):
        account = AccountsModel.find_by_username(username)
        return {'account': account.json()}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            if AccountsModel.find_by_username(data['username']):
                return {"message": "An user with same username [" + data['username'] + "] already exists"}, 409
            else:
                account = AccountsModel(data['username'])
                AccountsModel.hash_password(account, data['password'])

                AccountsModel.save_to_db(account)
                return {"message": "Account created successfully"}, 201
        except:
            return {"message": "Error creating new user"}, 500

    @auth.login_required(role='admin')
    def delete(self, username):
        try:
            account = AccountsModel.find_by_username(username)
            orders = account.get_orders()
            for o in orders:
                order = OrdersModel.find_by_id(o.id)
                OrdersModel.delete_from_db(order)

            AccountsModel.delete_from_db(account)

            return {"message": "Account deleted successfully"}, 200
        except:
            return {"message": "Error deleting account"}, 500


class AccountsList(Resource):
    @auth.login_required(role='admin')
    def get(self):
        data = {'accounts': []}
        accounts = AccountsModel.get_all()
        for a in accounts:
            data['accounts'].append(a.json())

        return data, 200


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            account = AccountsModel.find_by_username(data['username'])
            if AccountsModel.find_by_username(data['username']):
                if AccountsModel.verify_password(account, data['password']):
                    token = AccountsModel.generate_auth_token(account)
                    return {'token': token.decode('ascii')}, 200
                else:
                    return {"message": "Wrong password"}, 400
            else:
                return {"message": "User not found"}, 404
        except:
            return {"message": "Error Post Login"}, 500


api.add_resource(Orders, '/orders/<string:username>')
api.add_resource(OrdersList, '/orders')

api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(Event, '/event/<int:id>', '/event')

api.add_resource(ArtistList, '/artists')
api.add_resource(EventList, '/events')

api.add_resource(EventArtistsList, '/event/<int:id>/artists')
api.add_resource(EventArtist, '/event/<int:id_event>/artist/<id_artist>', '/event/<int:id_event>/artist')
api.add_resource(ArtistEventsList, '/artist/<int:id>/events')

api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
