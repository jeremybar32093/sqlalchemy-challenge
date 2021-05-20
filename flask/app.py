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

# base/index root
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

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation measurements taken on each date"""
    # Query all stations
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    precip_dict = {}
    for date, prcp in results:        
        # Check if date key is already in dict
        # If so, append to corresponding list of precipitation measurements
        # If not, add key into dictionary and add precipitation value into list
        if date in precip_dict:
            # Append precipitation measure to existing key-value pair
            precip_dict[date].append(prcp)
        else:
            # Add precipitation measure into precipitation measure list
            precip_measure_list = []
            precip_measure_list.append(prcp)
            precip_dict[date] = precip_measure_list

    return jsonify(precip_dict)

# stations route
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

# tobs route
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

    # Create a dictionary from the row data and append to a list 
    most_active_station_temps = []
    for station, date, tobs in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        most_active_station_temps.append(temp_dict)

    return jsonify(most_active_station_temps)

# start route
@app.route("/api/v1.0/<start>")
def return_summary_temp_start(start):
    """Returns the minimum, maximum, and average temperatures for all dates after start date provided."""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return the min, max, and average temperatures for temperatures past the start date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start)
    temp_dict = {}
    temp_dict["min_temp"] = results[0][0]
    temp_dict["max_temp"] = results[0][1]
    temp_dict["avg_temp"] = results[0][2]

    session.close()

    return jsonify(temp_dict)

# start/end route
@app.route("/api/v1.0/<start>/<end>")
def return_summary_temp_start_end(start,end):
    """Returns the minimum, maximum, and average temperatures for all dates between the start and end date provided (inclusive)."""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return the min, max, and average temperatures for temperatures past the start date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end)
    temp_dict = {}
    temp_dict["tmin"] = results[0][0]
    temp_dict["tmax"] = results[0][1]
    temp_dict["tavg"] = results[0][2]

    session.close()

    return jsonify(temp_dict)


#################################################
# Run Flask
#################################################
if __name__ == '__main__':
    app.run(debug=True)