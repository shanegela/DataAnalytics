import datetime as dt
import requests as req
import json
import numpy as np
import pandas as pd
from datetime import datetime
import os
from urllib.parse import urlparse

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float

import psycopg2
from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
	"""List all available api routes."""
	return (
		f"Avalable Routes:<br/>"
		f"/api/v1.0/dates - List available dates<br/>"

		f"/api/v1.0/positions/<date>"
		f"- List of holdings from file date<br/>"

		f"/api/v1.0/positions/<start_date>/<end_date>"
		f"- List of holdings from filings in the date range<br/>"

		f"/api/v1.0/srr/<start_date>/<end_date>"
		f"- List of holdings on end_date with a simple rate of return<br/>"
	)

#################################################
# Reformat date from 6/30/2017 12:00 AM to 2017-06-30
#################################################

def reformat_date(str_date):
	return datetime.strptime(str_date, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d')


#################################################
# Database Setup
#################################################
# create an engine to postgresql db
database_url = os.environ.get("DATABASE_URL")
sec13f_appkey = os.environ.get("SEC13F_APPKEY")
sec13f_brkcik = os.environ.get("SEC13F_BRKCIK")

connection_params = urlparse(database_url)
db = connection_params.path[1:]
user = connection_params.username
password = connection_params.password
host = connection_params.hostname
port = connection_params.port

url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)

# The return value of create_engine() is our connection object
engine = sqlalchemy.create_engine(url, client_encoding='utf8')

dburl = 'dbname={} user={} password={} host={}, port={}'
dburl = dburl.format(db, user, password, host, port)
db = psycopg2.connect(dburl)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the invoices and invoice_items tables
SecuritiesEx = Base.classes.securitiesex
ProcessedPositions = Base.classes.processed_positions
LatestPositions = Base.classes.latest_positions

# Create our session (link) from Python to the DB
session = Session(engine)

# Create a connection to the engine called conn
conn = engine.connect()


#################################################
@app.route("/api/v1.0/dates")
def getDates():
	"""Return a list of available dates"""
	# Query all countries from the Invoices table
	results1 = session.query(LatestPositions.currentreportdate).\
		group_by(LatestPositions.currentreportdate).all()

	results2 = session.query(ProcessedPositions.file_date).\
		group_by(ProcessedPositions.file_date).all()

	# Convert list of tuples into normal list
	dates_list = list(np.ravel(results1)) + list(np.ravel(results2))
	dates_list.sort()
	return jsonify(dates_list)



if __name__ == '__main__':
	app.run()

