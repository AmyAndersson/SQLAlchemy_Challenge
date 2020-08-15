import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
# @TODO: Initialize your Flask app here
app = Flask(__name__)

#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<strong>Temperature Search."
        f" Enter data as: (YYYY-MM-DD)</strong><br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
     )
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    return jsonify(results)
#################################################
@app.route("/api/v1.0/stations")
def stations():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations"""
    # Query all stations
    results1 = session.query(Station.name, Station.station).distinct().all()

    session.close()

    return jsonify(results1)

#################################################
@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    Busy_temp_1yr =session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <"2017-08-23").filter(Measurement.date >"2016-08-23").filter(Measurement.station == "USC00519281").all()

    session.close()
   

    return jsonify(Busy_temp_1yr)

@app.route("/api/v1.0/<start>")
def temp_range_stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return_list = []

    stats = session.query( Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    

    for date, min, avg, max in stats:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close() 

    return jsonify(return_list)

    


@app.route("/api/v1.0/<start>/<end>")
def temp_range_stats_end(start, end):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return_list_end= []

    stats_end = session.query( Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

   

    for date, min, avg, max in stats_end:
        new_dict_2 = {}
        new_dict_2["Date"] = date
        new_dict_2["TMIN"] = min
        new_dict_2["TAVG"] = avg
        new_dict_2["TMAX"] = max
        return_list_end.append(new_dict_2)

    session.close() 

    return jsonify(return_list_end)

    
    

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
     app.run(debug=True)