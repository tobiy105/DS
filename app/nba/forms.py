from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators ,ValidationError,DateField,DateTimeField, TimeField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_wtf import FlaskForm
from _datetime import datetime
from datetime import datetime
from datetime import time

#creating a form for team_api search
class TeamSearchForm(Form):
    team = StringField('Team: ', [validators.DataRequired()])

#creating a form for team_api search
class SearchForm(Form):
    search = StringField('Team: ', [validators.DataRequired()])
