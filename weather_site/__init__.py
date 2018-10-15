from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# --------------------------------- #
#         Database Set-up           #
# --------------------------------- #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# --------------------------------- #
#             Blue Prints           #
# --------------------------------- #
from weather_site.core.views import core
from weather_site.weather.views import weather

app.register_blueprint(core)
app.register_blueprint(weather)
