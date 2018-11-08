from flask import render_template, Blueprint
from flask import request, jsonify
from weather_site.weather.forms import FindLocation
from weather_site.models import Locations
from weather_site.data_pulls.current_conditions import get_current_conditions
from weather_site import mongo
from pymongo import MongoClient


weather = Blueprint('weather', __name__)

# ----------------------- CURRENT CONDITIONS -------------------------------- #


@weather.route('/', methods=['GET', 'POST'])
def current():

    form = FindLocation(form_name='PickCity')
    form.state_full.choices = [(row.state_full, row.state_full) for row in Locations.query.distinct(Locations.state_full).all()]
    form.city.choices = [(row.city, row.city) for row in Locations.query.distinct(Locations.city).all()]
    form.station.choices = [(row.name, row.name) for row in Locations.query.distinct(Locations.name).all()]

    return render_template('current.html', form=form)


@weather.route('/_get_cities')
def _get_cities():
    new_state = request.args.get('state', '01', type=str)
    cities = [(row.city, row.city) for row in Locations.query.filter_by(state_full=new_state).order_by(Locations.city).all()]
    return jsonify(cities)


@weather.route('/_get_stations')
def _get_stations():
    # gets stations on current stations have already been reported
    new_city = request.args.get('city', '01', type=str)
    stations = [(row.name, row.name) for row in Locations.query.filter_by(city=new_city).order_by(Locations.name).all()]
    return jsonify(stations)


@weather.route('/_map_get_stations')
def _map_get_stations():
    # gets stations for map view dropdown
    new_state = request.args.get('state', '01', type=str)
    stations = [(row.name, row.name) for row in Locations.query.filter_by(state_full=new_state).order_by(Locations.name).all()]
    return jsonify(stations)


@weather.route('/_get_conditions', methods=['GET', 'POST'])
def _get_conditions():

    new_station = request.args.get('station', '01', type=str)
    station_abbr = Locations.query.filter_by(name=new_station).first()
    station_abbr = station_abbr.station_id
    conditions = get_current_conditions(station_abbr)

    return jsonify(conditions)

# ----------------------- FORCAST CONDITIONS -------------------------------- #


@weather.route('/forecast')
def forecast():

    form = FindLocation(form_name='PickCity')

    all_states = mongo.db.forecast_5day.find({}, {'_id': 0, 'state': 1, 'state_full': 2})
    form.state_full.choices = sorted(set([(n['state'], n['state_full']) for n in all_states]))

    all_cities = mongo.db.forecast_5day.find({}, {'_id': 0, 'city': 1})
    form.city.choices = sorted(set([(n['city'], n['city']) for n in all_cities]))

    return render_template('forecast.html', form=form)


@weather.route('/_get_forecast_cities')
def _get_forecast_cities():
    new_state = request.args.get('state', '01', type=str)
    cities = sorted(set([(n['city'], n['city']) for n in mongo.db.forecast_5day.find({'state': new_state})]))

    return jsonify(cities)


@weather.route('/_get_forecast_data', methods=['GET', 'POST'])
def _get_forecast_data():
    new_city = request.args.get('city', '01', type=str)
    forecast = mongo.db.forecast_5day.find_one({'city': new_city})
    if '_id' in forecast.keys():
        forecast.pop('_id')

    return jsonify(forecast)

# --------------------------- BUOY REPORTING -------------------------------- #


@weather.route('/buoys')
def buoys():

    return render_template('buoys.html')
