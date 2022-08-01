from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func
db = SQLAlchemy()

class City(db.Model):
  __tablename__='cities'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  venues = db.relationship('Venue', backref=db.backref('vCity', lazy=True))
  artists = db.relationship('Artist', backref=db.backref('aCity', lazy=True))

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    web_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String(300))
    shows = db.relationship('Show', backref=db.backref('sVenue', lazy=True))
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False) 
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    web_link = db.Column(db.String())
    looking_for_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String())
    shows = db.relationship('Show', backref=db.backref('sArtist', lazy=True))
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())

class Show(db.Model):
  __tablename__= 'show'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id =db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)
