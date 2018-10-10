from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField


class FindLocation(FlaskForm):
    form_name = HiddenField('Form Name')
    state_full = SelectField('State', id='select_state')
    city = SelectField('City', id='select_city')
    station = SelectField('Station', id='select_station')
    submit = SubmitField('Get Forecast')
