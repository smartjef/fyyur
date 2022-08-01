from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length, Regexp

#City - State Form
class CityForm(FlaskForm):
    city = StringField(
        'city', validators=[DataRequired(), Length(min=3, max=40, message="3 - 40 characters allowed for city name")]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired(), Length(min=3, max=40, message="3 - 40 characters allowed for venue name")]
    )

    address = StringField(
        'address', validators=[DataRequired(), Length(min=3, max=20, message="3 - 20 characters allowed for address")]
    )
    phone = StringField(
        'phone', validators=[
            Regexp(r"[\d]{3}-[\d]{3}-[\d]{4}", message="Invalid format!! Try xxx-xxx-xxxx, e.g 123-456-7890, include the hyphens"),
            DataRequired()
        ]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    web_link = StringField(
        'web_link', validators=[URL()]
    )

    looking_for_talent = BooleanField( 'looking_for_talent' )

    seeking_desc = StringField(
        'seeking_desc'
    )

#Artist Form
class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[
            Regexp(r"[\d]{3}-[\d]{3}-[\d]{4}", message="Invalid format!! Try xxx-xxx-xxxx, only numbers allowed"),
            DataRequired()
        ]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )

    web_link = StringField(
        'web_link', validators=[URL()]
     )

    looking_for_venue = BooleanField( 'looking_for_venue' )

    seeking_desc= StringField(
            'seeking_desc'
     )

#Shows Form
class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id', validators=[DataRequired(), Regexp(r"^[1-9]\d*$", message="positive integer id required")]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired(), Regexp(r"^[1-9]\d*$", message="positive integer id required")]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
