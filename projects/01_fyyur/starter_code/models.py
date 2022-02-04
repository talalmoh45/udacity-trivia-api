from app import db

shows = db.Table('shows',
db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True))
db.Column('start_time',db.DateTime(timezone=True))


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    looking_for_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    artists = db.relationship(
        'Artist', secondary=shows, backref=db.backref('venues', lazy=True))

    def __repr__(self):
        return f'''
        id : {self.id}
        Name : {self.name}
        city : {self.city}
        state : {self.state}
        image_link : {self.image_link}
        '''

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    looking_for_venues = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
   
    def __repr__(self):
        return f'''
        id : {self.id}
        Name : {self.name}
        city : {self.city}
        state : {self.state}
        image_link : {self.image_link}
        '''
