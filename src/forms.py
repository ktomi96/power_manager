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

    submit = SubmitField("Submit")
