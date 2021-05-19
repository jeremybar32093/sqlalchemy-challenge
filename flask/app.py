import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station,Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates/temperatures for the most active station in the last year"""
    # First, get latest measurement taken and convert to datetime object
    max_date = session.query(func.max(Measurement.date)).all()[0][0]
    max_date_datetime = dt.datetime.strptime(max_date, '%Y-%m-%d')
    # Calculate date as of 1 year ago - these 2 dates will constitute date range for filtering
    max_date_minus_1yr = max_date_datetime - relativedelta(years=1)

    # Calculate most active station (station with highest count of measurements)
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).first()[0]


    # Return the last year's temperatures for the most active station calculated above
    results = session.query(Measurement.station,Measurement.date,Measurement.tobs).\
              filter(Measurement.station == most_active_station).\
              filter(Measurement.date >= max_date_minus_1yr).\
              filter(Measurement.date <= max_date).\
              all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    most_active_station_temps = []
    for station, date, tobs in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        most_active_station_temps.append(temp_dict)

    return jsonify(most_active_station_temps)


#################################################
# Run Flask
#################################################
if __name__ == '__main__':
    app.run(debug=True)