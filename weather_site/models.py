from weather_site import db


class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    city = db.Column(db.String(255))
    state_full = db.Column(db.String(255))
    station_id = db.Column(db.String(10))
    forecast_url = db.Column(db.String(255))
    hourForecast_url = db.Column(db.String(255))

    def __init__(self, name, city, state):
        self.name = name
        self.city = city
        self.state = state
        self.id = id
