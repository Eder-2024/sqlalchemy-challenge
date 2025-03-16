# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///C:/Users/eek_e/Documents/Data A/sqlalchemy-challenge/Resources/hawaii.sqlite")


# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route: List all available routes
@app.route("/")
def welcome():
    return (
        f"List all available api routes.!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Retrieve the last 12 months of precipitation data
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= a_year_ago).all()
    precip_dict = {date: prcp for date, prcp in precip_data}
    return jsonify(precip_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations
    station_data = session.query(Station.station).all()
    station_list = [station[0] for station in station_data]
    return jsonify(station_list)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the temperature observations of the most active station for the last 12 months
    most_active_station = 'USC00519281'
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= a_year_ago).all()
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)

# Start route
@app.route("/api/v1.0/<start>")
def start(start):
    # Query TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    temps = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    temp_dict = {
        "TMIN": temps[0][0],
        "TAVG": temps[0][1],
        "TMAX": temps[0][2]
    }
    return jsonify(temp_dict)

# Start/End route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query TMIN, TAVG, and TMAX for dates between the start and end date
    temps = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temp_dict = {
        "TMIN": temps[0][0],
        "TAVG": temps[0][1],
        "TMAX": temps[0][2]
    }
    return jsonify(temp_dict)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)