import datetime as dt
import requests as req
import json
import numpy as np
import pandas as pd
from datetime import datetime
import os

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

database_url = "postgres://ojlfjznfjutcuy:b34c1967c47a5f3749aca820c904a9711651057d596aacbb1d902b7d65536bfa@ec2-54-163-255-181.compute-1.amazonaws.com:5432/d9hv65hdijka83"
sec13f_appkey = os.environ.get("SEC13F_APPKEY")
sec13f_brkcik = os.environ.get("SEC13F_BRKCIK")

#connection_params = urlparse.urlparse(os.environ["DATABASE_URL"])
connection_params = urlparse.urlparse(database_url)
db = connection_params.path[1:]
user = connection_params.username
password = connection_params.password
host = connection_params.hostname
port = connection_params.port)
  
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
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
			'	else p2.price-p1.price/p1.price end as SSR ' +
			'FROM vPositions as p2 ' +
			'LEFT JOIN vPositions as p1 ON ' +
			'p1.name = p2.name AND ' +
			'p1.ticker = p2.ticker AND ' +
			"p1.file_date = '" + start_date + "' " +
			"WHERE p2.file_date = '" + end_date + "';")
	print(sql)
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

	if (file_date != date or len(results) == 0):
		results = session.query(
				ProcessedPositions.name,\
				sqlalchemy.sql.expression.literal_column("''").label("ticker"),\
				ProcessedPositions.cusip,\
				func.sum(ProcessedPositions.mval).label('mval'),\
				func.sum(ProcessedPositions.cmval).label('cmval'),\
				func.sum(ProcessedPositions.shares).label('shares'),\
				func.sum(ProcessedPositions.cshares).label('chares'))\
			.group_by(ProcessedPositions.name, ProcessedPositions.cusip)\
			.filter(ProcessedPositions.file_date == date).all()

	# Create a dictionary from the row data and append to a list of all_passengers
	positions = []
	for result in results:
		if result[3] is None:
			mval = None
		else:
			mval = float(result[3])
		if result[4] is None:
			cmval = None
		else:
			cmval = float(result[4])
		if result[5] is None:
			shares = None
		else:
			shares = float(result[5])
		if result[6] is None:
			cshares = None
		else:
			cshares = float(result[6])
		positions.append({
			"name": result[0],
			"ticker": result[1],
			"cusip": result[2],
			"mval": mval,
			"cmval": cmval,
			"shares": shares,
			"cshares": cshares
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