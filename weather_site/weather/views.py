from flask import render_template, Blueprint
from flask import request, jsonify, redirect, url_for
from bokeh.embed import components
from weather_site.graphs.graphs_bar import bar_1
from weather_site.weather.forms import FindLocation
from weather_site.models import Locations
from weather_site.data_pulls.current_conditions import get_current_conditions


weather = Blueprint('weather', __name__)

# ----------------------- CURRENT CONDITIONS -------------------------------- #


@weather.route('/current_blank', methods=['GET', 'POST'])
def current_blank():

    form = FindLocation(form_name='PickCity')
    form.state_full.choices = [(row.state_full, row.state_full) for row in Locations.query.distinct(Locations.state_full).all()]
    form.city.choices = [(row.city, row.city) for row in Locations.query.distinct(Locations.city).all()]
    form.station.choices = [(row.name, row.name) for row in Locations.query.distinct(Locations.name).all()]

    return render_template('current_blank.html', form=form)


@weather.route('/current', methods=['GET', 'POST'])
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

    x = ["Jan", "Feb", "Mar", "Apr", "May", "June"]
    y = [1.2, 2.5, 3.7, 4, 8, 3]

    plot = bar_1(x, y)

    script, div = components(plot)
    return render_template('forecast.html', script=script, div=div)

# --------------------------- BUOY REPORTING -------------------------------- #


@weather.route('/buoys')
def buoys():

    return render_template('buoys.html')
