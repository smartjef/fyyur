#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from hashlib import new
import os
import sys
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, template_rendered, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from model import *
# from model import *
#----------------------------------------------------------------------------#
# App C\lonfig.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Models in model.py file

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if not isinstance(value, datetime):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  latest_artist = Artist.query.order_by(db.desc(Artist.created_at)).limit(10).all()
  latest_venue = Venue.query.order_by(db.desc(Venue.created_at)).limit(10).all()
  return render_template('pages/home.html', latest_artists=latest_artist,latest_venues=latest_venue)

# Cities
#-----------------------------------
@app.route('/city/create', methods=['GET'])
def create_city():
  form = CityForm()
  return render_template('/forms/new_city.html',form=form)

@app.route('/city/create', methods=['POST'])
def create_city_submit():
  form = CityForm()
  try:
    city = request.form.get('city')
    state = request.form.get('state')
    new_city = City(city=city,state=state)
    db.session.add(new_city)
    db.session.commit()
    flash(f"City {city} added successfully")
    return redirect('/')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured while creating city')
  finally:
    db.session.close()
  return render_template('/pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = City.query.all()
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term','')
  data = Venue.query.filter(Venue.name.like('%'+search_term+'%'))
  count=data.count()
  response={
    'count':count,
    'data' : data,
    'search_term' : search_term,
  }
  return render_template('pages/search_venues.html', results=response)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  city = City.query.get(venue.city_id)

  #upcoming shows
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show. start_time>datetime.now()).all()   
  upcoming_shows = []
  for u_show in upcoming_shows_query:
      upcoming_shows.append(u_show)
  
  #past
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show. start_time<datetime.now()).all()   
  past_shows = []
  for p_show in past_shows_query:
      past_shows.append(p_show)

  data={
    'venue':venue,
    'city':city,
    'upcoming_shows': upcoming_shows,
    'past_shows': past_shows
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  cities = City.query.all()
  return render_template('forms/new_venue.html', form=form, cities=cities)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    if form.validate_on_submit():
      name = request.form.get('name')
      city_id = request.form.get('city_id')
      if city_id == None:
        city_id = 1
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      web_link = request.form.get('website_link')
      looking_for_talent = request.form.get('seeking_talent')
      seeking_desc =None
      if looking_for_talent == 'y':
        looking_for_talent = True
        seeking_desc = request.form.get('seeking_description')
      else:
        looking_for_talent = False

      venue = Venue(name=name,city_id=city_id,address=address,phone=phone,genres=genres, image_link=image_link,facebook_link=facebook_link,web_link=web_link,looking_for_talent=looking_for_talent, seeking_desc=seeking_desc)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return redirect('/venues')
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured')
  finally:
    db.session.close()
  return render_template('/forms/new_venue.html', form=form)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue= Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  cities = City.query.all()
  return render_template('forms/edit_venue.html', form=form, venue=venue, cities=cities)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  try:
    if form.validate_on_submit():
      venue=Venue.query.get(venue_id)
      venue.name = request.form.get('name')
      city_id = request.form.get('city_id')
      if city_id == None:
        city_id = 1
      venue.city_id = city_id
      venue.address = request.form.get('address')
      venue.phone = request.form.get('phone')
      venue.genres = request.form.getlist('genres')
      venue.image_link = request.form.get('image_link')
      venue.facebook_link = request.form.get('facebook_link')
      venue.web_link = request.form.get('web_link')
      looking_for_talent = request.form.get('looking_for_talent')
      seeking_desc = None
      if looking_for_talent == 'y':
        looking_for_talent = True
        seeking_desc = request.form.get('seeking_desc')
      else:
        looking_for_talent = False

      venue.looking_for_talent =looking_for_talent
      venue.seeking_desc = seeking_desc
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_venue', venue_id=venue_id))
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured while updating')
  finally:
    db.session.close()

  return redirect(url_for('edit_venue', venue_id=venue_id))

@app.route('/venues/<venue_id>/delete')
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue was successfully deleted!')
    return redirect('/venues')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured')
  finally:
    db.session.close()
  return redirect('/venues')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term','')
  data = Artist.query.filter(Artist.name.ilike('%'+search_term+'%'))
  count=data.count()
  response={
    'count':count,
    'data' : data,
    'search_term' : search_term,
  }
  return render_template('pages/search_artists.html', results=response)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  city = City.query.get(artist.city_id)

  #upcoming shows
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show. start_time>datetime.now()).all()   
  upcoming_shows = []
  for u_show in upcoming_shows_query:
      upcoming_shows.append(u_show)
  
  #past
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show. start_time<datetime.now()).all()   
  past_shows = []
  for p_show in past_shows_query:
      past_shows.append(p_show)

  data={
    'artist':artist,
    'city':city,
    'upcoming_shows': upcoming_shows,
    'past_shows': past_shows
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  city = City.query.all()
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist, cities=city)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  try:
    if form.validate_on_submit():
      artist=Artist.query.get(artist_id)
      artist.name = request.form.get('name')
      city_id = request.form.get('city_id')
      if city_id == None:
        city_id = 1
      artist.city_id = city_id
      artist.phone = request.form.get('phone')
      artist.genres = request.form.getlist('genres')
      artist.image_link = request.form.get('image_link')
      artist.facebook_link = request.form.get('facebook_link')
      artist.web_link = request.form.get('web_link')
      looking_for_venue = request.form.get('looking_for_venue')
      seeking_desc = None
      if looking_for_venue == 'y':
        looking_for_venue = True
        seeking_desc = request.form.get('seeking_desc')
      else:
        looking_for_venue = False
      artist.looking_for_venue =looking_for_venue
      artist.seeking_desc = seeking_desc
      db.session.commit()
      flash('artist ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_artist', artist_id=artist_id))
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured while updating')
  finally:
    db.session.close()

  return redirect(url_for('edit_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  cities = City.query.all()
  return render_template('forms/new_artist.html', form=form, cities=cities)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  try:
    if form.validate_on_submit():
      name = request.form.get('name')
      city_id = request.form.get('city_id')
      if city_id == None:
        city_id = 1
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      web_link = request.form.get('web_link')
      looking_for_venue = request.form.get('looking_for_venue')
      seeking_desc = None
      if looking_for_venue == 'y':
        looking_for_venue = True
        seeking_desc = request.form.get('seeking_desc')
      else:
        looking_for_venue = False
      seeking_desc = seeking_desc  
      artist = Artist(name=name,phone=phone,city_id=city_id,genres=genres,image_link=image_link,facebook_link=facebook_link,web_link=web_link,looking_for_venue=looking_for_venue,seeking_desc=seeking_desc)
      db.session.add(artist)
      db.session.commit()
      flash('artist ' + request.form['name'] + ' was successfully listed!')
      return redirect('/artists')
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured while adding artist')
  finally:
    db.session.close()

  return render_template('forms/new_artist.html', form=form)

#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  data = Show.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  try:
    if form.validate_on_submit():
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
      return redirect('/')
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message), 'danger')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured')
  finally:
    db.session.close()
  return render_template('forms/new_show.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)

