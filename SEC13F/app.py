import datetime as dt
import requests as req
import json
import numpy as np
import pandas as pd
from datetime import datetime
import os
from urllib.parse import urlparse
from flask_cors import CORS

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
CORS(app)
#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
	"""List all available api routes."""
	return (
		f"Avalable Routes:<br><br>"
		f"<ul>"
		f"	<li>/api/v1.0/dates</li>"
		f"		<ul>"
		f"			<li>List available dates</li>"
		f"		</ul>"
		f"	<li>/api/v1.0/positions/&lt;date&gt;"
		f"		<ul>"
		f"			<li>List of holdings from file date</li>"
		f"		</ul>"
		f"	<li>/api/v1.0/positions/&lt;start date&gt;/&lt;end date&gt;</li>"
		f"		<ul>"
		f"			<li>List of holdings from filings in the date range</li>"
		f"		</ul>"
		f"	<li>/api/v1.0/srr/&lt;start date&gt;/&lt;end date&gt;</li>"
		f"		<ul>"
		f"			<li>List of holdings on end_date with a simple rate of return</li>"
		f"		</ul>"
		f"	<li>/api/v1.0/indgrp/&lt;start date&gt;/&lt;end date&gt;"
		f"		<ul>"
		f"			<li>List of industry groups held from filings in the date range</li>"
		f"		</ul>"
		f"	<li>api/v1.0/indsec/&lt;start date&gt;/&lt;end date&gt;</li>"
		f"		<ul>"
		f"			<li>List of industry sectors held from filings in the date range</li>"
		f"		</ul>"
		f"	<li>/api/v1.0/classification_dates</li>"
		f"		<ul>"
		f"			<li>List of filing dates with industry sector and industry group information</li>"
		f"		</ul>"
		f"</ul>"
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

dburl = 'dbname={} user={} password={} host={} port={}'
dburl = dburl.format(db, user, password, host, port)
db = psycopg2.connect(dburl)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the invoices and invoice_items tables
SecuritiesEx = Base.classes.securitiesex
ProcessedPositions = Base.classes.processed_positions
Positions = Base.classes.positions
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

#################################################
@app.route("/api/v1.0/classification_dates")
def getClassificationDates():
	"""Return a list of available older file dates that table SecuritieEx is based on"""
	# can't filter by date string using sqlalchemy!!!!!11
	# results = session.query(Positions.file_date).\
	# 	group_by(Positions.file_date).having(Positions.file_date <= '2017-03-31')

	# dates_list = list(np.ravel(results))
	# dates_list.sort()
	# return jsonify(dates_list)

	sql = ("SELECT DISTINCT file_date from positions where file_date <= '2017-03-31' order by file_date")
	print(sql)
	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		positions.append(record[0])

	return jsonify(positions)

#################################################

@app.route("/api/v1.0/srr/<start_date>/<end_date>")
def getSRR(start_date, end_date):
	## List of holdings on end_date with a simple rate of return
	sql = ('SELECT p2.name as name, p2.ticker as ticker, ' +
			'p1.file_date as date1, p2.file_date as date2, ' +
			'p1.mval as mval1, p1.shares as shares1, p1.price as price1, ' +
			'p2.mval as mval2, p2.shares as shares2, p2.price as price2, ' +
			'case when p1.price = 0 then 0 ' +
			'	when p2.shares = 0 then 0 ' +
			'	else ((p2.price-p1.price)/p1.price) * 100 end as SSR ' +
			'FROM vPositions as p2 ' +
			'LEFT JOIN vPositions as p1 ON ' +
			'p1.name = p2.name AND ' +
			'p1.ticker = p2.ticker AND ' +
			"p1.file_date = '" + start_date + "' " +
			"WHERE p2.file_date = '" + end_date + "';")
	
	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		if record[4] is None: 
			mval1 = None 
		else: 
			mval1 = int(record[4])
		if record[5] is None: 
			shares1 = None 
		else: 
			shares1 = int(record[5])
		if record[6] is None: 
			price1 = None 
		else: 
			price1 = float(record[6])
		if record[7] is None: 
			mval2 = None 
		else: 
			mval2 = int(record[7])
		if record[8] is None: 
			shares2 =None 
		else: 
			shares2 = int(record[8])
		if record[9] is None: 
			price2 = None 
		else: 
			price2 = float(record[9])
		if record[10] is None: 
			srr = None 
		else: 
			srr = float(record[10])
		positions.append({
			"name": record[0],
			"ticker": record[1],
			"file_date1": record[2],
			"file_date2": record[3],
			"mval1": mval1,
			"shares1": shares1,
			"price1": price1,
			"mval2": mval2,
			"shares2": shares2,
			"price2": price2,
			"srr": srr
		})

	return jsonify(positions)

#################################################

@app.route("/api/v1.0/indsec/<start_date>/<end_date>")
def getIndSector(start_date, end_date):
	## List of market values by industry sector for a date range
	sql = ('SELECT p.file_date, s.indsec, SUM(p.mval) as mval, SUM(p.shares) as shares ' +
			'FROM vPositions as p ' +
			'JOIN securitiesex as s ON p.ticker = s.ticker ' +
			"WHERE indsec <> 'Nan' and '" + start_date + "' <= p.file_date and p.file_date <= '" + end_date + "' " +
			"GROUP BY p.file_date, s.indsec " +
			"HAVING '" + start_date + "' <= file_date and file_date <= '" + end_date + "' " +
			"ORDER BY indsec, file_date;")
	print(sql)
	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		if record[2] is None: 
			mval = None 
		else: 
			mval = int(record[2])
		if record[3] is None: 
			shares = None 
		else: 
			shares = int(record[3])
		positions.append({
			"file_date": record[0],
			"indsec": record[1],
			"mval": mval,
			"shares":shares
		})

	return jsonify(positions)

#################################################

@app.route("/api/v1.0/indgrp/<start_date>/<end_date>")
def getIndGroup(start_date, end_date):
	## List of market values by industry group for a date range
	sql = ('SELECT p.file_date, s.indgrp, SUM(p.mval) as mval, SUM(p.shares) as shares ' +
			'FROM vPositions as p ' +
			'JOIN securitiesex as s ON p.ticker = s.ticker ' +
			"WHERE indgrp <> 'Nan' and '" + start_date + "' <= p.file_date and p.file_date <= '" + end_date + "' " +
			"GROUP BY p.file_date, s.indgrp " +
			"HAVING '" + start_date + "' <= file_date and file_date <= '" + end_date + "' " +
			"ORDER BY indgrp, file_date;")
	print(sql)
	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		if record[2] is None: 
			mval = None 
		else: 
			mval = int(record[2])
		if record[3] is None: 
			shares = None 
		else: 
			shares = int(record[3])
		positions.append({
			"file_date": record[0],
			"indgrp": record[1],
			"mval": mval,
			"shares": shares
		})

	return jsonify(positions)


#################################################
# WITH data AS
# ( SELECT file_date, name, ticker, mval, shares, price
#   FROM vPositions
#   WHERE '2015-06-30' <= file_date and file_date <= '2017-06-30'
# ), all_dates AS 
# (
#   SELECT DISTINCT file_date
#   FROM vPositions
#   WHERE '2015-06-30' <= file_date and file_date <= '2017-06-30'
# ), all_secs AS 
# (
#   SELECT DISTINCT ticker, name
#   FROM vPositions
#   WHERE '2015-06-30' <= file_date and file_date <= '2017-06-30'
# )
# SELECT x.ticker, x.file_date, x.name, data.mval, data.shares, data.price
# from (
#   SELECT file_date, ticker, name
#   FROM all_dates
#   CROSS JOIN all_secs
# ) x
# LEFT JOIN data on x.file_date = data.file_date AND x.ticker = data.ticker
# ORDER BY x.ticker, x.file_date;

@app.route("/api/v1.0/positions/<start_date>/<end_date>")
def getPositionsOverTime(start_date, end_date):
	## List of holdings from start date to end date
	sql = ('WITH data AS                                                             ' +
			'( SELECT file_date, name, ticker, mval, shares, price                    ' +
			'  FROM vPositions                                                        ' +
			"  WHERE '" + start_date + "' <= file_date and file_date <= '" + end_date + "' " +
			'), all_dates AS                                                          ' +
			'(                                                                        ' +
			'  SELECT DISTINCT file_date                                              ' +
			'  FROM vPositions                                                        ' +
			"  WHERE '" + start_date + "' <= file_date and file_date <= '" + end_date + "' " +
			'), all_secs AS                                                           ' +
			'(                                                                        ' +
			'  SELECT DISTINCT ticker, name                                           ' +
			'  FROM vPositions                                                        ' +
			"  WHERE '" + start_date + "' <= file_date and file_date <= '" + end_date + "' " +
			')                                                                        ' +
			'SELECT x.ticker, x.file_date, x.name, data.mval, data.shares, data.price ' +
			'from (                                                                   ' +
			'  SELECT file_date, ticker, name                                         ' +
			'  FROM all_dates                                                         ' +
			'  CROSS JOIN all_secs                                                    ' +
			') x                                                                      ' +
			'LEFT JOIN data on x.file_date = data.file_date AND x.ticker = data.ticker' +
			' ORDER BY x.ticker, x.file_date;')

	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		if record[3] is None:
			mval = None
		else:
			mval = float(record[3])
		if record[4] is None:
			shares = None
		else:
			shares = float(record[4])
		if record[5] is None:
			price = None
		else:
			price = float(record[5])
		positions.append({
			"ticker": record[0],
			"file_date": record[1],
			"name": record[2],
			"mval": mval,
			"shares": shares,
			"price": price
		})

	return jsonify(positions)

#################################################
@app.route("/api/v1.0/positions/<date>")
def getPositions(date):
	## Get current holdings

	# Use `declarative_base` from SQLAlchemy to connect your class to your PostgreSQL database
	Base2 = declarative_base()

	class Lastest_Positions(Base2):
		__tablename__ = 'latest_positions'
		id = Column(Integer, primary_key=True)
		querydate = Column(Text)
		filerid = Column(Text)
		cik = Column(Text)
		currentreportdate = Column(Text)
		priorreportdate = Column(Text)
		ownername = Column(Text)
		issueid = Column(Text)
		ticker = Column(Text)
		companyname = Column(Text)
		issuetitle = Column(Text)
		exchangeid = Column(Text)
		street1 = Column(Text)
		city = Column(Text)
		state = Column(Text)
		zipcode = Column(Text)
		country = Column(Text)
		phonecountrycode = Column(Text)
		phoneareacode = Column(Text)
		phonenumber = Column(Text)
		sharesout = Column(Text)
		sharesoutdate = Column(Text)
		price = Column(Text)
		pricedate = Column(Text)
		sharesheld = Column(Text)
		sharesheldchange = Column(Text)
		sharesheldpercentchange = Column(Text)
		marketvalue = Column(Text)
		marketvaluechange = Column(Text)
		portfoliopercent = Column(Text)
		sharesoutpercent = Column(Text)
		marketoperator = Column(Text)
		marketoperatorid = Column(Text)
		markettier = Column(Text)
		markettierid = Column(Text)

		def __repr__(self):
			return f"companyname={self.companyname}, ticker={self.ticker}, marketvalue={self.marketvalue}, sharesheld={self.sharesheld}"


	# Use `create_all` to create the latest_positions table in the database
	Base2.metadata.create_all(engine)

	# Use MetaData from SQLAlchemy to reflect the tables\n",
	metadata = MetaData(bind=engine)
	metadata.reflect()

	# Save the reference to the `latest_positions` table as a variable called `table`
	table = sqlalchemy.Table('latest_positions', metadata, autoload=True)

	query_url = "http://edgaronline.api.mashery.com/v2/ownerships/currentownerholdings?ciks=%s&appkey=%s" % (sec13f_brkcik, sec13f_appkey)
	sec_data = req.get(query_url).json()


	file_date = None
	securities = []
	for row in sec_data["result"]["rows"]:
		querydate = None
		filerid = None
		cik = None
		currentreportdate = None
		priorreportdate = None
		ownername = None
		issueid = None
		ticker = None
		companyname = None
		issuetitle = None
		exchangeid = None
		street1 = None
		city = None
		state = None
		zipcode = None
		country = None
		phonecountrycode = None
		phoneareacode = None
		phonenumber = None
		sharesout = None
		sharesoutdate = None
		price = None
		pricedate = None
		sharesheld = None
		sharesheldchange = None
		sharesheldpercentchange = None
		marketvalue = None
		marketvaluechange = None
		portfoliopercent = None
		sharesoutpercent = None
		marketoperator = None
		marketoperatorid = None
		markettier = None
		markettierid = None
		for value in row["values"]:
			if not(file_date) and value["field"] == "currentreportdate":
				file_date = reformat_date(value["value"])
			if value["field"] == "querydate":
				querydate = reformat_date(value["value"])
			if value["field"] == "filerid":
				filerid = value["value"]
			if value["field"] == "cik":
				cik = value["value"]
			if value["field"] == "currentreportdate":
				currentreportdate = reformat_date(value["value"])
			if value["field"] == "priorreportdate":
				 priorreportdate = reformat_date(value["value"])
			if value["field"] == "owername":
				ownername = value["value"]
			if value["field"] == "issueid":
				issueid = value["value"]
			if value["field"] == "ticker":
				ticker = value["value"]
			if value["field"] == "companyname":
				companyname = value["value"]
			if value["field"] == "issuetitle":
				issuetitle = value["value"]
			if value["field"] == "exchangeid":
				exchangeid = value["value"]
			if value["field"] == "street1":
				street1 = value["value"]
			if value["field"] == "city":
				city = value["value"]
			if value["field"] == "state":
				state = value["value"]
			if value["field"] == "zip":
				zipcode = value["value"]
			if value["field"] == "country":
				country = value["value"]
			if value["field"] == "phonecountrycode":
				phonecountrycode = value["value"]
			if value["field"] == "phoneareacode":
				phoneareacode = value["value"]
			if value["field"] == "phonenumber":
				phonenumber = value["value"]
			if value["field"] == "sharesout":
				sharesout = value["value"]
			if value["field"] == "sharesoutdate":
				sharesoutdate = value["value"]
			if value["field"] == "price":
				price = value["value"]
			if value["field"] == "pricedate":
				pricedate = reformat_date(value["value"])
			if value["field"] == "sharesheld":
				sharesheld = value["value"]
			if value["field"] == "sharesheldchange":
				sharesheldchange = value["value"]
			if value["field"] == "sharesheldpercentchange":
				sharesheldpercentchange = value["value"]
			if value["field"] == "marketvalue":
				marketvalue = value["value"]
			if value["field"] == "marketvaluechange":
				marketvaluechange = value["value"]
			if value["field"] == "portfoliopercent":
				portfoliopercent = value["value"]
			if value["field"] == "sharesoutpercent":
				sharesoutpercent = value["value"]
			if value["field"] == "marketoperator":
				marketoperator = value["value"]
			if value["field"] == "marketoperatorid":
				marketoperatorid = value["value"]
			if value["field"] == "markettier":
				markettier = value["value"]
			if value["field"] == "markettierid":
				markettierid = value["value"]
		securities.append({
			 "querydate" :               querydate
			,"filerid" :                 filerid
			,"cik" :                     cik
			,"currentreportdate" :       currentreportdate
			,"priorreportdate" :         priorreportdate
			,"ownername" :               ownername
			,"issueid" :                 issueid
			,"ticker" :                  ticker
			,"companyname" :             companyname
			,"issuetitle" :              issuetitle
			,"exchangeid" :              exchangeid
			,"street1" :                 street1
			,"city" :                    city
			,"state" :                   state
			,"zipcode" :                 zipcode
			,"country" :                 country
			,"phonecountrycode" :        phonecountrycode
			,"phoneareacode" :           phoneareacode
			,"phonenumber" :             phonenumber
			,"sharesout" :               sharesout
			,"sharesoutdate" :           sharesoutdate
			,"price" :                   price
			,"pricedate" :               pricedate
			,"sharesheld" :              sharesheld
			,"sharesheldchange" :        sharesheldchange
			,"sharesheldpercentchange" : sharesheldpercentchange
			,"marketvalue" :             marketvalue
			,"marketvaluechange" :       marketvaluechange
			,"portfoliopercent" :        portfoliopercent
			,"sharesoutpercent" :        sharesoutpercent
			,"marketoperator" :          marketoperator
			,"marketoperatorid" :        marketoperatorid
			,"markettier" :              markettier
			,"markettierid" :            markettierid
		})
	
	# check if holdings for the date exist
	results = session.query(
			LatestPositions.companyname,\
			LatestPositions.ticker,\
			sqlalchemy.sql.expression.literal_column("''").label("cusip"),\
			func.sum(func.cast(LatestPositions.marketvalue, Float)).label('mval'),\
			func.sum(func.cast(LatestPositions.marketvaluechange, Float)).label('cmval'),\
			func.sum(func.cast(LatestPositions.sharesheld, Float)).label('shares'),\
			func.sum(func.cast(LatestPositions.sharesheldchange, Float)).label('cshares'))\
		.group_by(LatestPositions.companyname, LatestPositions.ticker)\
		.filter(LatestPositions.currentreportdate == file_date).all()

	if (len(results) == 0):

		# delete existing file date data from table
		sql = f"DELETE FROM latest_positions WHERE currentreportdate = '{file_date}'"
		conn.execute(sql)

		sql = f"DELETE FROM processed_positions WHERE file_date = '{file_date}'"
		conn.execute(sql)


		conn.execute(table.insert(), securities)

	sql = ("SELECT file_Date, name, ticker, mval, cmval, shares, cshares, price     " +
		    " FROM vPositions                                                       " +
			"  WHERE '" + date + "' = file_date;                               ")

	cursor = db.cursor()
	cursor.execute(sql)
	response = cursor.fetchall()
	positions = []
	for record in response:
		if record[3] is None:
			mval = None
		else:
			mval = float(record[3])
		if record[4] is None:
			cmval = None
		else:
			cmval = float(record[4])
		if record[5] is None:
			shares = None
		else:
			shares = float(record[5])
		if record[6] is None:
			cshares = None
		else:
			cshares = float(record[6])
		if record[7] is None:
			price = None
		else:
			price = float(record[7])
		positions.append({
			"file_date": record[0],
			"name": record[1],
			"ticker": record[2],
			"mval": mval,
			"cmval": cmval,
			"shares": shares,
			"cshares": cshares,
			"price": price
		})

	return jsonify(positions)

#################################################
if __name__ == '__main__':
    app.run()


#################################################
# POSTGRESQL VIEW
#################################################
# CREATE VIEW vPositions
# AS
# SELECT file_date, name, ticker, mval, cmval, shares, cshares, price                 
# FROM (                                                           
#   SELECT file_date, name, ticker, SUM(mval) as mval, SUM(cmval) as cmval,      
#     SUM(shares) as shares, SUM(cshares) as cshares, MIN(price) as price       
#   FROM (                                                                       
#     SELECT p.file_date, p.name, s.ticker, CAST(p.mval AS NUMERIC) as mval,     
#       CAST(p.cmval AS NUMERIC) as cmval, CAST(p.shares AS NUMERIC) as shares,  
#       CAST(p.cshares AS NUMERIC) as cshares, CAST(p.price AS NUMERIC) as price,
#       CAST(p.prior_price AS NUMERIC) as pprice                                 
#     FROM processed_positions p                                                 
#     LEFT JOIN securitiesex s ON p.cusip = s.cusip
#   ) x                                                                         
#   GROUP BY file_date, name, ticker                                             
#   UNION ALL                                                                    
#   SELECT lp.currentreportdate, lp.companyname, lp.ticker,                      
#     CAST(lp.marketvalue AS NUMERIC), CAST(lp.marketvaluechange AS NUMERIC),    
#     CAST(lp.sharesheld AS NUMERIC), CAST(lp.sharesheldchange AS NUMERIC),       
#     case when CAST(lp.sharesheld AS NUMERIC) = 0 then 0 else  CAST(lp.marketvalue AS NUMERIC)/( CAST(lp.sharesheld AS NUMERIC) * 1.0) end
#   FROM latest_positions lp                                                     
# ) t;