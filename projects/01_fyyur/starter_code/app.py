#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.headerregistry import Address
from email.mime import image
import json
from tkinter.messagebox import NO
from unicodedata import name
from wsgiref import validate
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from pytz import timezone
from forms import *
from flask_migrate import Migrate
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    data = list()
    states = Venue.query.with_entities(Venue.state).distinct().all()
    i = 0
    for state in states:
        state = state[0]
        citites = Venue.query.with_entities(Venue.city).filter(
            Venue.state == state).distinct().all()
        for city in citites:
            city = city[0]
            subdata = dict()
            subdata['city'] = city
            subdata['state'] = state
            venues = Venue.query.with_entities(Venue.id, Venue.name).filter(
                Venue.state == state, Venue.city == city).distinct().all()
            subdata['venues'] = venues
            data.append(subdata)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    searched = request.form.get('search_term', '')
    venue = Venue.query
    venue = venue.filter(Venue.name.ilike('%' + searched + '%'))
    result = dict()

    for v in venue:
        result['count'] = venue.count()
        result['data'] = venue
    return render_template('pages/search_venues.html', results=result, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    VenueData=dict()
    VenueList= Venue.query.with_entities(Venue.id,Venue.name,Venue.city,Venue.state,Venue.address,Venue.facebook_link,Venue.website_link,Venue.image_link,Venue.seeking_description,Venue.looking_for_talent).filter(Venue.id==venue_id).all()
    genres = Venue.query.with_entities(Venue.genres).filter(Venue.id==venue_id).all()

    genres = genres[0][0].split(',')
    length = len(genres)
    for i in range(length):
        for char in '{ }':
            genres[i] = genres[i].replace(char,'')

    for v in VenueList:
        VenueData['id'] = v[0]
        VenueData['name'] = v[1]
        VenueData['city'] = v[2]
        VenueData['state'] = v[3]
        VenueData['address'] = v[4]
        VenueData['facebook_link'] = v[5]
        VenueData['website_link'] = v[6]
        VenueData['image_link'] = v[7]
        VenueData['seeking_description'] = v[8]
        VenueData['looking_for_talent'] = v[9]
        VenueData['genres'] = genres
    
    # data = list(filter(lambda d: d['id'] == venue_id, VenueData))[0]
    return render_template('pages/show_venue.html', venue=VenueData)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    form = VenueForm()
    newVenue = Venue(name=form.name.data,
                     city=form.city.data,
                     state=form.state.data,
                     address=form.address.data, phone=form.phone.data,
                     image_link=form.image_link.data,
                     genres=form.genres.data,
                     facebook_link=form.facebook_link.data,
                     website_link=form.website_link.data,
                     looking_for_talent=form.seeking_talent.data,
                     seeking_description=form.seeking_description.data)

    try:
        db.session.add(newVenue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('cannot add' + request.form['name'])
    finally:
        db.session.close()

    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')



@app.route('/venues/<int:venue_id>/delete', methods=['GET','DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
      DeletedVenue = Venue.query.filter(Venue.id == venue_id)
      DeletedVenue.delete()
      db.session.commit()
      flash("Venue with id :" + request.form['id']+" deleted succesfylly!")
    except:
        db.session.rollback()
        flash("Error cannot delete the Venue")
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    searched = request.form.get('search_term', '')
    artist = Artist.query
    artist = artist.filter(Artist.name.ilike('%' + searched + '%'))
    result = dict()

    for art in artist:
        result['count'] = artist.count()
        result['data'] = artist
    return render_template('pages/search_artists.html', results=result, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    
    ArtisitDict = dict()
    ArtistList = Artist.query.with_entities(Artist.id,Artist.name,Artist.city,Artist.state,Artist.phone,Artist.looking_for_venues,
    Artist.image_link,
    Artist.facebook_link,
    Artist.website_link,
    Artist.seeking_description
    ).filter(Artist.id==artist_id).all()
    ArtistGenres = Artist.query.with_entities(Artist.genres).filter(Artist.id==artist_id).all()

    ArtistGenres = ArtistGenres[0][0].split(',')
    length = len(ArtistGenres)
    for i in range(length):
        for char in '{ }':
            ArtistGenres[i] = ArtistGenres[i].replace(char,'')

    for item in ArtistList:
        ArtisitDict['id'] = item[0]
        ArtisitDict['name'] = item[1]
        ArtisitDict['city'] = item[2]
        ArtisitDict['state'] = item[3]
        ArtisitDict['phone'] = item[4]
        ArtisitDict['seeking_venue'] = item[5]
        ArtisitDict['image_link'] = item[6]
        ArtisitDict['facebook_link'] = item[7]
        ArtisitDict['website_link'] = item[8]
        ArtisitDict['seeking_description'] = item[9]
        ArtisitDict['genres'] = ArtistGenres

    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=ArtisitDict)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    
    artist = Artist.query.get(artist_id)
       
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    artist.name = form.name.data
    artist.genre = form.genres.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.website_link = form.website_link.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = form.facebook_link.data
    artist.seeking_description = form.seeking_venue.data
    artist.image_link = form.image_link.data
    artist.genres = form.genres.data
    try:
        db.session.commit()
        flash('artist has been added succesfully')
    except:
        db.session.rollback()
        flash('Can not Add Artist')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.address = form.address.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website_link = form.website_link.data
        venue.looking_for_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.genres = form.genres.data
        db.session.commit()
        flash('venue has been added succesgfully')
    except:
        db.session.rollback()
        flash('venue hasnot been added succesgfully')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))
    

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm()
    newArtist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        looking_for_venues=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
    )

    try:
        db.session.add(newArtist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist could not be listed.')
    finally:
        db.session.close()

    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    form = ShowForm()
    Shows = Venue.query.with_entities(Venue.id,Venue.name,Artist.id,Artist.name,Artist.image_link).join(Venue.artists).all()
    showData = []
    date = str(form.start_time.default)
    for index, tuple in enumerate(Shows):
        for index in tuple:
            data = dict()
            data['venue_id'] = tuple[0]
            data['venue_name'] = tuple[1]
            data['artist_id'] = tuple[2]
            data['artist_name'] = tuple[3]
            data['artist_image_link'] = tuple[4]
            data['start_time'] = date 
        showData.append(data)
    return render_template('pages/shows.html', shows=showData)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    venue_id = form.venue_id.data
    artist_id = form.artist_id.data
    ven = Venue.query.get(venue_id)
    art = Artist.query.get(artist_id)
    ven.artists = [art]
    art.venues = [ven]
    try:
        db.session.add(ven)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('error' + request.form['venue_id']+'cannot be added')
    finally:
        db.session.close()
    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
