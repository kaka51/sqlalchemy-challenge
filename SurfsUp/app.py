# 1. Import Flask & SQLalchemy
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

session = Session(engine)

measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= date).\
    order_by(measurement.date).all()
    precipitation = {date: prcp for date, prcp in prcp}
    return jsonify(precipitation = precipitation)


@app.route("/api/v1.0/stations")
def station():
    stations = session.query(Station.station).all()
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations = all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    sel = [measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    temp = session.query(measurement.station, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= date).all()
    temperature = list(np.ravel(temp))
    return jsonify(temperature = temperature)


@app.route("/api/v1.0/<start>")
def start(start = None):
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    data = session.query(*sel).\
    filter(measurement.date >= start).all()
    result = list(np.ravel(data))
    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def end(start = None, end = None):
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    data = session.query(*sel).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    result = list(np.ravel(data))
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
