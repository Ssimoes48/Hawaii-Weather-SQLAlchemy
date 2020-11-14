import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end>"
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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_list = session.query((Station.station)).all()

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


@app.route("/api/v1.0/start_end")
def start_end():

    session = Session(engine)

    end_date = "2017, 8, 23"
    start_date = "2016, 08, 23"

    temp_summary = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.count(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).group_by(Measurement.date).all()

    return jsonify(temp_summary)

if __name__ == '__main__':
    app.run(debug=True)
