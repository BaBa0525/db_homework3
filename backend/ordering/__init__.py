from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import event
from haversine import haversine, Unit
import logging

from ordering.config import LOGGING, DB_URI, SECRET_KEY

if LOGGING:
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

def distance(latA, lngA, latB, lngB):
    locationA = (latA, lngA)
    locationB = (latB, lngB)
    return haversine(locationA, locationB, unit=Unit.METERS)

@event.listens_for(db.engine, 'connect')
def receive_connect(dbapi_connection, connection_record):
    dbapi_connection.create_function('distance', 4, distance, deterministic=True)

'''
routes must be import after app is initalized
otherwise, it would cause error
'''
from ordering.routes import userRoutes
from ordering.routes import shopRoutes
from ordering.routes import mealRoutes
