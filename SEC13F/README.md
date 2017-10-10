# SEC13F Analysis: Berkshire Hathaway 

The purpose of this project was to analyze the holdings of Berkshire Hathaway to determine what securities and classifications the the company is invested in.

## Form: SEC13F

The SEC Form 13F is a filing with the Securities and Exchange Commission (SEC) also known as the Information Required of Institutional Investment Managers Form. It is a quarterly filing required of institutional investment managers with over $100 million in qualifying assets. Companies required to file SEC Form 13F may include insurance companies, banks, pension funds, investment advisers and broker-dealers.

SEC Form 13F, which must be filed within 45 days of the end of each quarter, contains information about the investment manager and potentially a list of their recent investment holdings. **It provides investors with an inside look at the holdings of Wall Street's largest investment managers.**

Companies submit their SEC13F filings using the [EDGAR System](https://www.sec.gov/page/everythingedgar).  These filings are made public on the [SEC website](https://www.sec.gov/edgar/searchedgar/companysearch.html).

## Berkshire Hathaway

Berkshire Hathaway is a holding company run by Warren Buffett.  Warren Buffett is one of the most successful investors of all time, with $32 billion in assets.  He regarded as the ultimate value investor following the Benjamin Graham approach to finding value. Berkshire's 13F holdings are often held for years and even decades at a time. With low turnover and high conviction top holdings, Berkshire's portfolio is a popular investment model for backtesting and copying.


### Step 0: SEC13F API

The EDGAR system also has an [API](http://developer.edgar-online.com/).

Jupyter Notebok: [SEC13F_API](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_API.ipynb)
This notebook was developed to explore the API.

**Limitation**  The API only has current holdings available.  My communications with the API contact confirmed that no historical data is available and the request is not on their roadmap.  So using the API for information was not a possibility.

### Step 1: Save SEC13F Filings

Jupyter Notebook: [SEC13F_STEP1_SaveFilings](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP1_SaveFilings.ipynb)

Since all the SEC13F filings are available online.  I used BeautifulSoup to save the xml filings from onine to the filings directory.

**Limitation** 
* XML formation for SEC13F submission was implemented as of 06/30/2013.  Prior filings are in a text fixed width submission.  This project will only analyze xml submissions.
* SEC13F amendments are not analyzed

### Step 2: Parse and Clean SEC13F Filings

Jupyter Notebook: [SEC13F_STEP2_CleanFilings](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP2_CleanFilings.ipynb)

This notebook opens each xml file and parses the data for the following fields
* file date: SEC13F quarter end submission date
* name: security name
* cusip: cusip of the security
* mval: market value of the shares held
* shares: shares or principal held

The aggregate data for all xml files is saved to a csv file, sec13f_clean_data.csv.

### Step 3: Save SEC13F Information to Database

Jupyter Notebook [SEC13F_STEP3_SaveDataToDB](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP3_SaveDataToDB.ipynb)

This notebook reads the csv file into a Pandas dataframe and uses SQLAlchmey's ORM functionality to save the data to a SQLite database.  The csv data is saved to a positions table.

### Step 4: Get Industry Sector and Industry Group for Securities

Jupyter Notebook [SEC13F_STEP4_GetDecoratedData](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP4_GetDecoratedData.ipynb)

This notebook reads the positions table in the SQLite database: sec13f.sqlite to get a unique list of CUSIP.  The notebook then scrapes the  [Search13F](https://search13f.com/securities/neighbors/) website to get decorated information such as the Industry Sector and Industry Group.

The CUSIP, Industry Sector, and Industry Group data are then stored into a csv file, decorated_data.csv

### Step 5: Save Industry Sector and Industry Group to Database

Jupyter Notebook [SEC13F_STEP5_SaveDecoratedDataToDB](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP5_SaveDecoratedDataToDB.ipynb)

This notebook reads the csv file into a Pandas dataframe and uses SQLAlchmey's ORM functionality to save the data to a SQLite database.  The csv data is saved to a indsectorindgroup table.

### Step 6: Handle missing data

Jupyter Notebook [SEC13F_STEP6_HandleMissingData](https://github.com/shanegela/DataAnalytics/blob/gh-pages/SEC13F/SEC13F_STEP6_HandleMissingData.ipynb)

Some CUSIP have missing Industry Sector or Industry Group because they are no longer traded due to corporation reorganizations like mergers, exchanges, or spinoffs.

This notebook identifies CUSIP with missing industry sector and/or industry group.  A manual intervention is done to lookup the missing information.  The research information is then put into a dictionary which is then used to update the indsectorindgroup table in the SQLite database.




