# SEC13F Analysis: Berkshire Hathaway 

The purpose of this project was to analyze the holdings of Berkshire Hathaway to determine what securities and classifications the the company is invested in.

## Form: SEC13F

The SEC Form 13F is a filing with the Securities and Exchange Commission (SEC) also known as the Information Required of Institutional Investment Managers Form. It is a quarterly filing required of institutional investment managers with over $100 million in qualifying assets. Companies required to file SEC Form 13F may include insurance companies, banks, pension funds, investment advisers and broker-dealers.

SEC Form 13F, which must be filed within 45 days of the end of each quarter, contains information about the investment manager and potentially a list of their recent investment holdings. **It provides investors with an inside look at the holdings of Wall Street's largest investment managers.**

Companies submit their SEC13F filings using the [EDGAR System](https://www.sec.gov/page/everythingedgar).  These filings are made public on the [SEC website](https://www.sec.gov/edgar/searchedgar/companysearch.html).

## Berkshire Hathaway

Berkshire Hathaway is a holding company run by Warren Buffett.  Warren Buffett is one of the most successful investors of all time, with $32 billion in assets.  He regarded as the ultimate value investor following the Benjamin Graham approach to finding value. Berkshire's 13F holdings are often held for years and even decades at a time. With low turnover and high conviction top holdings, Berkshire's portfolio is a popular investment model for backtesting and copying.


### Investigate SEC13F API

The EDGAR system also has an [API](http://developer.edgar-online.com/).

Jupyter Notebook: [SEC13F_API](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_API.ipynb)
This notebook was developed to explore the API.

**API Limitation**  The API only has current holdings available.  My communications with the API contact confirmed that no historical data is available and the request is not on their roadmap.  So using the API for information was not a possibility.

### Step 1: Save SEC13F Filings

Jupyter Notebook: [SEC13F_STEP1_SaveFilings](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP1_SaveFilings.ipynb)

Since all the SEC13F filings are available online.  I used BeautifulSoup to save the xml filings from online to the filings directory.

**Limitations** 
* XML formation for SEC13F submission was implemented as of 06/30/2013.  Prior filings are in a text fixed width submission.  This project will only analyze xml submissions.
* SEC13F amendments are not analyzed

### Step 2: Parse and Clean SEC13F Filings

Jupyter Notebook: [SEC13F_STEP2_CleanFilings](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP2_CleanFilings.ipynb)

This notebook opens each xml file and parses the data for the following fields
* file date: SEC13F quarter end submission date
* name: security name
* cusip: CUSIP of the security
* mval: market value of the shares held
* shares: shares or principal held

The aggregate data for all xml files is saved to a csv file, sec13f_clean_data.csv.

### Step 3: Save SEC13F Information to Database

Jupyter Notebook [SEC13F_STEP3_SaveDataToDB](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP3_SaveDataToDB.ipynb)

This notebook reads the csv file into a Pandas dataframe and uses SQLAlchmey's ORM functionality to save the data to a PostgreSQL database.  The csv data is saved to a positions table.

### Step 4: Get Industry Sector and Industry Group for Securities

Jupyter Notebook [SEC13F_STEP4_GetDecoratedData](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP4_GetDecoratedData.ipynb)

This notebook reads the positions table in the PostgreSQL database: sec13f to get a unique list of CUSIP.  The notebook then scrapes the  [Search13F](https://search13f.com/securities/neighbors/) website to get decorated information such as the Industry Sector and Industry Group.

The CUSIP, Industry Sector, and Industry Group data are then stored into a csv file, decorated_data.csv

### Step 5: Save Industry Sector and Industry Group to Database

Jupyter Notebook [SEC13F_STEP5_SaveDecoratedDataToDB](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP5_SaveDecoratedDataToDB.ipynb)

This notebook reads the csv file into a Pandas dataframe and uses SQLAlchmey's ORM functionality to save the data to a PostgreSQL database.  The csv data is saved to a indsectorindgroup table.

### Step 6: Handle missing data

Jupyter Notebook [SEC13F_STEP6_HandleMissingData](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP6_HandleMissingData.ipynb)

Some CUSIP have missing Industry Sector or Industry Group because they are no longer traded due to corporation reorganizations like mergers, exchanges, or spinoffs.

This notebook identifies CUSIP with missing industry sector and/or industry group.  A manual intervention is done to lookup the missing information.  The research information is then put into a dictionary which is then used to update the indsectorindgroup table in the PostgreSQL database.

### Step 7: Analyze data in Python

Jupyter Notebook [SEC13F_STEP7_AnalyzeData](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP7_AnalyzeData.ipynb)

### Step 8: Process Positions

SEC13F data from sec13f.xml filings only include name, CUSIP, market value and shares held.  Where as, data attained from the SEC13F API is more comprehensive and includes derived values like change in market value and change in shares held.

This notebook uses Pandas dataframes to join data to get the prior quarter filing to get derived values for change in market value and change in shares held.  These values are not available for the first date, 2013-06-30.

Jupyter Notebook [SEC13F_STEP8_ProcessPositions](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP8_ProcessPositions.ipynb)

### Step 9: Create API 

This python script uses Flask to create APIs to retrieve data from the SEC13F postgresql DB.

#### API Endpoints
* [root](https://sec13f-flask-heroku.herokuapp.com/)
* [/api/v1.0/dates](https://sec13f-flask-heroku.herokuapp.com/api/v1.0/dates) - List available dates
* [/api/v1.0/positions/filedate](https://sec13f-flask-heroku.herokuapp.com/api/v1.0/positions/2017-06-30) - List of holdings from file date.  Will also hit the Edgar API to get positions from the latest file date and store them in the database
* [/api/v1.0/positions/startdate/enddate](https://sec13f-flask-heroku.herokuapp.com/api/v1.0/positions/2017-06-30/2017-09-30) - List of holdings from filings in the date range
* [/api/v1.0/srr/startdate/endate](https://sec13f-flask-heroku.herokuapp.com/api/v1.0/srr/2017-06-30/2017-09-30) - List of holdings on file end date with a simple rate of return

Jupyter Notebook [SEC13F_STEP9_API.py](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_STEP9_API.py)


### Step 10: Web Dashboard

[index.html](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/index.html) and [index.js](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/index.js) uses bootstrap, D3, D3Plus, and DataTables to allow the user to select a file date and display the positions held by Berkshire Hathaway according to the SEC13F form filed.

**Issue**
Ran into CORS Not Allowed (Cross-Origin Resource Sharing) when querying the API.

**Solution**
Import flask-cors into the flask app.

**Alterntive Solution**
Enabled CORS through Chrome extension: [Allow-Control-Allow-Origin](https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?hl=en).  Note that Jupyter Notebook does not work well with CORS enabled.

### Step 11: Heroku

Deploy application to Heroku to host the application and database.

Herokup [app.py](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/app.py) (in synch with SEC13F_STEP9_API)

Reference [Flask-HEROKU](https://github.com/agopez/flask-heroku)

### Step 12: Issues

* Industry Sector and Group classifications are available through the Edgar API for the latest holdings.  However these classifications are different from the classifications I'm able to retrieve from the scraping done in Step 4.  So classification analysis was not performed.
* After analyzing the filings, I wanted to analyze what my potential gain if I were to purchase stocks that have a positive change in shares. See [SEC13F_Strategy01](https://github.com/shanegela/DataAnalytics/blob/master/SEC13F/SEC13F_Strategy01.ipynb).  It was difficult to grab historical prices for securities that had corporate reorgnizations and prices were not correctly reflected because of the possibility of splits.  So additional split information is needed.