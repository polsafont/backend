from models.artist import ArtistModel
from models.event import EventModel

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate

from db import db

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

#from add_data import init_db
#init_db()


class Artist(Resource):
    def get(self, id):
        try:
            artist = ArtistModel.find_by_id(id)
            return {'artist': artist.json()}, 200
        except:
            return {"message": "Error Get Artist"}, 500

    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('genre', type=str, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()

        try:
            artist = ArtistModel(data['name'], data['country'], data['genre'])
            ArtistModel.save_to_db(artist)
            return {"message": "Artist añadido correctamente"}, 200
        except:
            return {"message": "Error Post Artist"}, 500

    def delete(self, id):
        try:
            artist = ArtistModel.find_by_id(id)
            ArtistModel.delete_from_db(artist)
            return {"message": "Artist eliminado correctamente"}, 200
        except:
            return {"message": "Error Delete Artist"}, 500

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
            event = EventModel(data['name'], data['place'], data['city'], data['date'], data['price'], data['total_available_tickets'])
            EventModel.save_to_db(event)
            return {"message": "Event añadido correctamente"}, 200
        except:
            return {"message": "Error Post Event"}, 500

    def delete(self, id):
        try:
            event = EventModel.find_by_id(id)
            EventModel.delete_from_db(event)
            return {"message": "Event eliminado correctamente"}, 200
        except:
            return {"message": "Error Delete Event"}, 500

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
            event.set_event(data['name'], data['place'], data['city'], data['date'], data['price'], data['total_available_tickets'])
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


"""
class EventArtist(Resource):
    def get(self, id_event, id_artist):
        event = EventModel.find_by_id(id_event)
        artists = EventModel.get_artists(event)
        artist = ArtistModel.find_by_id(id_artist)
        data = {'artists': []}
        for a in artists:
            data['artists'].append(a.json())

        return data
"""


api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(Event, '/event/<int:id>', '/event')

api.add_resource(ArtistList, '/artists')
api.add_resource(EventList, '/events')

api.add_resource(EventArtistsList, '/event/<int:id>/artists')
#api.add_resource(EventArtist, '/event/<int:id_event>/artist/<id_artist>', '/event/<int:id_event>/artist')

#api.add_resource(ArtistEventsList, '/artist/<int:id>/events')

if __name__ == '__main__':
    app.run(port=5000, debug=True)