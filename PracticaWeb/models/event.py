from db import db

artists = db.Table('event_artists', db.Column('events_id', db.Integer, db.ForeignKey('events.id')), db.Column('artists_id', db.Integer, db.ForeignKey('artists.id')))

class EventModel(db.Model):
    __tablename__ = 'events'  # This is table name
    __table_args__ = (db.UniqueConstraint('name', 'date', 'city'),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    place = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_available_tickets = db.Column(db.Integer, nullable=False)

    artists = db.relationship('ArtistModel', secondary=artists, backref=db.backref('events', lazy='dynamic'))

    def __init__(self, name, place, city, date, price, total_available_tickets):
        self.name = name
        self.place = place
        self.city = city
        self.date = date
        self.price = price
        self.total_available_tickets = total_available_tickets

    def json(self):
        data = {'artists': []}
        for a in self.artists:
            data['artists'].append(a.json())

        data = {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'city': self.city,
            'date': self.date,
            'artists': data,
            'price': self.price,
            'total_available_tickets': self.total_available_tickets
        }

        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_event(self, name, place, city, date, price, total_available_tickets):
        self.name = name
        self.place = place
        self.city = city
        self.date = date
        self.price = price
        self.total_available_tickets = total_available_tickets

    def set_tickets_free(self, total_available_tickets):
        self.total_available_tickets = total_available_tickets

    def get_artists(self):
        return self.artists

    @classmethod
    def find_by_id(cls, id):
        return EventModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return EventModel.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return EventModel.query.all()

    @classmethod
    def find_by_artist(cls, artist):
        events = EventModel.query.filter(EventModel.artists.any(id=2)).all()
        data = {'events': []}
        for a in events:
            data['events'].append(a.json())

        return data




