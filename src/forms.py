from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField, EmailField
from wtforms.validators import InputRequired, Email, DataRequired, NumberRange, AnyOf, Length


class AC_login_setup(FlaskForm):
    ADDRESS = StringField(
        "IP address of the ac", validators=[InputRequired()])
    TOKEN = StringField(
        "Token from ac app/lib", validators=[InputRequired()])
    KEY = StringField(
        "Key from ac app/lib", validators=[InputRequired()])
    LOCATION_ID = StringField(
        "Site location id", validators=[InputRequired()])
    SOLAR_API_KEY = StringField(
        "Solar site API key", validators=[InputRequired()])
    SOLAR_LOGGER_TRIGGER_VALUE = StringField(
        "Solar logging trigger HH:MM", validators=[InputRequired()])
    AC_LOGGER_TRIGGER_VALUE = StringField(
        "AC logging tigger  or HH:MM", validators=[InputRequired()])
    LOG_PATH = StringField(
        "Logs path ex.: ./logs/", validators=[InputRequired()])
    DB_PATH = StringField(
        "Database path ex.:./database/power_manager.db", validators=[InputRequired()])
    DB = StringField(
        "SQLALCHEMY databe type ex.:sqlite:///", validators=[InputRequired()])
    TIME_ZONE = StringField(
        "Time zone Country/City", validators=[InputRequired()])

    submit = SubmitField("Submit")
