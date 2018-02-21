# Python SQL toolkit and Object Relational Mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the stations class to a variable called `Station`
Station = Base.classes.stations

# Assign the measurements class to a variable called `Measurement`
Measurement = Base.classes.measurements

# Create a session
session = Session(engine)

# create flask api
app = Flask(__name__)

# Home
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/after/'enter start date in %Y-%m-%d format'<br>"
        f"/api/v1.0/between/'enter start date in %Y-%m-%d format'/'enter end date in %Y-%m-%d format'<br>"
    )

# precipitaion
@app.route("/api/v1.0/precipitation")
def prcp():
    """Query for the dates and precipitation observations from the last year"""
    
    query_start_date = '2017-01-01'

    prcp_data = (session
                 .query(Measurement.date, Measurement.prcp)
                 .filter(Measurement.date >= query_start_date)
                 .all())
    
    prcp_list = []
    
    for result in prcp_data:
        
        row = {}
        
        row[str(result[0])] = result[1]
        
        prcp_list.append(row)
        
    return jsonify(prcp_list)

# stations
@app.route("/api/v1.0/stations")
def stations():
    """Query for the stations"""
    stations = (session
                .query(Station)
                .all())

    stations_list = []
    
    for station in stations:
    
        row = {}
        row['station'] = station.station
        row['name'] = station.name
        row['latitude'] = station.latitude
        row['longitude'] = station.longitude
        row['elevation'] = station.elevation

        stations_list.append(row)
        
    return jsonify(stations_list)       

# Temperature
@app.route("/api/v1.0/tobs")
def tobs():
    """Query for the dates and temperature observations from the last year"""
    
    query_start_date = '2017-01-01'

    tobs_data = (session
                 .query(Measurement.date, Measurement.tobs)
                 .filter(Measurement.date >= query_start_date)
                 .all())
    
    tobs_list = []
    
    for result in tobs_data:
        
        row = {}
        
        row[str(result[0])] = result[1]
        
        tobs_list.append(row)
        
    return jsonify(tobs_list)

# start end
@app.route("/api/v1.0/after")
@app.route("/api/v1.0/after/<start>")
def temp_analysis_after(start='2017-01-01'):
    
    # query for min temp
    temp_min = (session
                .query(func.min(Measurement.tobs))
                .filter(Measurement.date >= start)
                .scalar())
    
    # query for max temp
    temp_max = (session
                .query(func.max(Measurement.tobs))
                .filter(Measurement.date >= start)
                .scalar())  
    
    # query for average temp
    temp_avg = (session
                .query(func.avg(Measurement.tobs))
                .filter(Measurement.date >= start)
                .scalar())
    
    temp_analysis_dict= {}
    
    temp_analysis_dict['min'] = temp_min
    
    temp_analysis_dict['max'] = temp_max
    
    temp_analysis_dict['average'] = temp_avg
    
    return jsonify(temp_analysis_dict)


@app.route("/api/v1.0/between")
@app.route("/api/v1.0/between/<start>/<end>")
def temp_analysis_between(start='2017-01-01', end='2017-12-31'):
    
    # query for min temp
    temp_min = (session
                .query(func.min(Measurement.tobs))
                .filter(Measurement.date >= start)
                .filter(Measurement.date <= end)
                .scalar())
    
    # query for max temp
    temp_max = (session
                .query(func.max(Measurement.tobs))
                .filter(Measurement.date >= start)
                .filter(Measurement.date <= end)
                .scalar())  
    
    # query for average temp
    temp_avg = (session
                .query(func.avg(Measurement.tobs))
                .filter(Measurement.date >= start)
                .filter(Measurement.date <= end)
                .scalar())
    
    temp_analysis_dict= {}
    
    temp_analysis_dict['min'] = temp_min
    
    temp_analysis_dict['max'] = temp_max
    
    temp_analysis_dict['average'] = temp_avg
    
    return jsonify(temp_analysis_dict)

if __name__ == '__main__':
    app.run(debug=True)