# Honolulu, Hawaii sqlalchemy-challenge

## Background

Planning for self awarded long vacation in Honolulu, Hawaii. Plan includes climate analysis about the area.

## Data Source

sqlite database with two tables:

1. measurements (station, date, prcp, tobs)

2. station (station, name, latitude, longitude, elevation)

## Project Scope

1. Analyze and Explore the Climate Data: SQLAlchemy ORM queries, Pandas, and Matplotlib used to do a basic climate analysis and data exploration of the climate database. Specifically, 

2. Climate App: Flask API used to create the following routes:

  - Static APIs: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br><br>

  - Dynamics APIs: <br>
    /api/v1.0/start_date(as yyyy-mm-dd) <br>
    /api/v1.0/start_date(as yyyy-mm-dd)/end_date(as yyyy-mm-dd) <br><br>

  - Examples for the Dynamic APIs: <br>
    /api/v1.0/2016-01-24 <br>
    /api/v1.0/2016-01-24/2017-01-25 <br><br>

  - Rules for the Dynamics APIs: <br>
    + Start and End dates must be within the available date range in the data set <br>
    + Start date must be chronologically before end date <br>

### Shortcuts

- [SQLalchemy Notebook](https://github.com/Ahmadhha/sqlalchemy-challenge/blob/main/climate_starter.ipynb)

- [Flask App Code](https://github.com/Ahmadhha/sqlalchemy-challenge/blob/main/app.py)
