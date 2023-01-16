import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"Available Routes:<br/><br/>"
        f"Static APIs:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Dynamics APIs:<br/>"
        f"/api/v1.0/start_date(as yyyy-mm-dd)<br/>"
        f"/api/v1.0/start_date(as yyyy-mm-dd)/end_date(as yyyy-mm-dd)<br/><br/>"
        f"Examples for the Dynamic APIs:<br/>"
        f"/api/v1.0/2016-01-24<br/>"
        f"/api/v1.0/2016-01-24/2017-01-25<br/><br/>"
        f"Rules for the Dynamics APIs:<br/>"
        f"- Start and End dates must be within the available date range in the data set<br/>"
        f"- Start date must be chronologically before end date"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve the last 12 months of data"""
    # find the date one year form most recent
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_earlier = dt.date.fromisoformat(most_recent[0]) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_year_data = session.query(measurement.date, measurement.prcp).\
                  filter(measurement.date > year_earlier).all()
    
    session.close()

    # Convert list of tuples into normal list
    last_year_dict = {row[0]:row[1] for row in last_year_data}

    return jsonify(last_year_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations IDs"""
    # Query all stations
    station_ids = session.query(station.station).all()

    session.close()

    # Create a list of station ids
    all_stations = list(np.ravel(station_ids))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures for the most active station"""

    # find the date one year form most recent
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_earlier = dt.date.fromisoformat(most_recent[0]) - dt.timedelta(days=365)

    # Query most active station data
    sel = [station.station]
    most_active_station = session.query(*sel).\
    filter(measurement.station == station.station).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).\
    first()

    # Query the last 12 months of temperature observation data for this station
    station_year = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == most_active_station[0]).\
    filter(measurement.date > year_earlier).\
    all()

    session.close()

    # Create a list of temperatures for the most active station
    date_list, temp_list = zip(*station_year)

    return jsonify(temp_list)


@app.route("/api/v1.0/<start_date>")
def start_date_ref(start_date):
    """Return a JSON list of the minimum temperature, the average temperature, 
        and the maximum temperature for a specified start"""

    session = Session(engine)

    date_range = session.query(measurement.date).all()

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    range_temps = session.query(*sel).\
        filter(measurement.date >= start_date).\
        all()

    session.close()

    if start_date not in list(np.ravel(date_range)):
        return ("Error, Date Out of Range")

    return jsonify(list(np.ravel(range_temps)))


@app.route("/api/v1.0/<start_date>/<end_date>")
def start__end_date_ref(start_date, end_date):
    """Return a JSON list of the minimum temperature, the average temperature, 
        and the maximum temperature for a specified start and end date"""

    session = Session(engine)

    date_range = session.query(measurement.date).all()

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    range_temps = session.query(*sel).\
        filter(measurement.date >= start_date).\
        filter(measurement.date >= end_date).\
        all()

    session.close()

    if (start_date not in list(np.ravel(date_range))) or (end_date not in list(np.ravel(date_range))):
        return ("Error, Date Out of Range")

    if start_date > end_date:
        return ("Error, Start Date must be before End Date")

    return jsonify(list(np.ravel(range_temps)))



if __name__ == '__main__':
    app.run(debug=True)