
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
measurement = Base.classes.measurement
station = Base.classes.station


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
        f"/api/v1.0/sations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    return jsonify(results)
#################################################
@app.route("/api/v1.0/stations")
def stations():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations"""
    # Query all stations
    results1 = session.query(station.name, station.station).distinct().all()

    session.close()

    return jsonify(results1)

#################################################
@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    Busy_temp_1yr =session.query(measurement.date, measurement.tobs).filter(measurement.date <"2017-08-23").filter(measurement.date >"2016-08-23").filter(measurement.station == "USC00519281").all()

    session.close()
   

    return jsonify(Busy_temp_1yr)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return_list = []

    results = session.query( measurement.data,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results_list = []

    results = session.query( measurement.data,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    for date, min, avg, max in results:
        start_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(results_list)

    session.close()    

    return jsonify(return_list)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results_list_SE = []

    results = session.query( measurement.data,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(and_(measurement.date >= start, measurement.date <= end)).group_by(measurement.date).all()

    for date, min, avg, max in results:
        startend_dict = {}
        startend_dict["Date"] = date
        startend_dict["TMIN"] = min
        startend_dict["TAVG"] = avg
        startend_dict["TMAX"] = max
        return_list_SE.append(startend_dict)

    session.close()    

    return jsonify(results_list_SE)






filter(and_(Measurement.date >= start, Measurement.date <= end))

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
     app.run(debug=True)