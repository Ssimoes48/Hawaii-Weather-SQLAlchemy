import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
        filter(Measurement.date > "2016, 08, 23").group_by(Measurement.date).order_by(Measurement.date).all()
    
    result_list = []

    for date, prcp in results:
        result_dict = {date: prcp}
        result_list.append(result_dict)

    session.close()

    return jsonify(result_list)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    stations = session.query((Station.station)).all()

    station_list = list(np.ravel(stations))

    session.close()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    active_station = session.query(Measurement.date, (Measurement.tobs)).\
        filter(Measurement.date > "2016, 08, 23").all()
    
    active_station_list = []

    for date, tobs in active_station:
        station_dict = {date: tobs}
        active_station_list.append(station_dict)    

    session.close()

    return jsonify(active_station_list)


@app.route("/api/v1.0/<start>")
def start_temp(start):

    session = Session(engine)

    temp_summary = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    temp_list = list(np.ravel(temp_summary))

    session.close()

    return jsonify(temp_summary)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    temp_summary = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp_list = list(np.ravel(temp_summary))

    session.close()

    return jsonify(temp_summary)

if __name__ == '__main__':
    app.run(debug=True)
