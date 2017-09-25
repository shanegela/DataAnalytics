
# Angela Shane

## SQL Homework 1

### Database Setup
The following queries run against the [Pagila database](https://www.postgresql.org/ftp/projects/pgFoundry/dbsamples/pagila/pagila/).  Run the following steps to setup the database
1. Download pagila-0.10.1.zip
2. Unzip the zip file
3. From the command line:
  * change directories to the unzipped files
  * run psql
4. run each sql file by doing: \i filename.sql
  * Run files in this order: pagila-schema.sql, pagila-insert-data.sql, pagila-data.sql



```python
import pandas as pd
import psycopg2
import 
```


```python
# parameters
host="localhost"
database="pagila"
user="postgres"
password="************"

# Creating a connection
conn_str = "host={} dbname={} user={} password={}".format(host, database, user, password)
conn = psycopg2.connect(conn_str)
```

### 1a. You need a list of all the actors’ first name and last name


```python
df = pd.read_sql('SELECT first_name, last_name FROM actor', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PENELOPE</td>
      <td>GUINESS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NICK</td>
      <td>WAHLBERG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ED</td>
      <td>CHASE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>JENNIFER</td>
      <td>DAVIS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>JOHNNY</td>
      <td>LOLLOBRIGIDA</td>
    </tr>
  </tbody>
</table>
</div>



### 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name


```python
df = pd.read_sql('SELECT UPPER(first_name || \' \' || last_name) as "Actor Name" FROM actor', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PENELOPE GUINESS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NICK WAHLBERG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ED CHASE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>JENNIFER DAVIS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>JOHNNY LOLLOBRIGIDA</td>
    </tr>
  </tbody>
</table>
</div>



### 2a. You need to find the id, first name, and last name of an actor, of whom you know only the first name of "Joe." What is one query would you use to obtain this information?


```python
df = pd.read_sql('SELECT actor_id, first_name, last_name FROM actor WHERE first_name ilike \'Joe\'', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9</td>
      <td>JOE</td>
      <td>SWANK</td>
    </tr>
  </tbody>
</table>
</div>



### 2b. Find all actors whose last name contain the letters GEN. Make this case insensitive



```python
df = pd.read_sql('SELECT actor_id, first_name, last_name FROM actor WHERE last_name ilike \'%GEN%\'', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>14</td>
      <td>VIVIEN</td>
      <td>BERGEN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>41</td>
      <td>JODIE</td>
      <td>DEGENERES</td>
    </tr>
    <tr>
      <th>2</th>
      <td>107</td>
      <td>GINA</td>
      <td>DEGENERES</td>
    </tr>
    <tr>
      <th>3</th>
      <td>166</td>
      <td>NICK</td>
      <td>DEGENERES</td>
    </tr>
  </tbody>
</table>
</div>



### 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order. Make this case insensitive.



```python
df = pd.read_sql('SELECT actor_id, first_name, last_name FROM actor WHERE last_name ilike \'%LI%\' ORDER BY last_name, first_name', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>86</td>
      <td>GREG</td>
      <td>CHAPLIN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>82</td>
      <td>WOODY</td>
      <td>JOLIE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>34</td>
      <td>AUDREY</td>
      <td>OLIVIER</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>CUBA</td>
      <td>OLIVIER</td>
    </tr>
    <tr>
      <th>4</th>
      <td>172</td>
      <td>GROUCHO</td>
      <td>WILLIAMS</td>
    </tr>
    <tr>
      <th>5</th>
      <td>137</td>
      <td>MORGAN</td>
      <td>WILLIAMS</td>
    </tr>
    <tr>
      <th>6</th>
      <td>72</td>
      <td>SEAN</td>
      <td>WILLIAMS</td>
    </tr>
    <tr>
      <th>7</th>
      <td>83</td>
      <td>BEN</td>
      <td>WILLIS</td>
    </tr>
    <tr>
      <th>8</th>
      <td>96</td>
      <td>GENE</td>
      <td>WILLIS</td>
    </tr>
    <tr>
      <th>9</th>
      <td>164</td>
      <td>HUMPHREY</td>
      <td>WILLIS</td>
    </tr>
  </tbody>
</table>
</div>



### 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:



```python
df = pd.read_sql('SELECT * FROM country WHERE country IN (\'Afghanistan\',\'Bangladesh\', \'China\')', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country_id</th>
      <th>country</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Afghanistan</td>
      <td>2006-02-15 09:44:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12</td>
      <td>Bangladesh</td>
      <td>2006-02-15 09:44:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>23</td>
      <td>China</td>
      <td>2006-02-15 09:44:00</td>
    </tr>
  </tbody>
</table>
</div>



### 3a. Add a middle_name column to the table actor. Specify the appropriate column type



```python
cur = conn.cursor()
cur.execute('ALTER TABLE actor ADD COLUMN middle_name varchar(45);')
df = pd.read_sql('SELECT * FROM actor', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
      <th>middle_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>PENELOPE</td>
      <td>GUINESS</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NICK</td>
      <td>WAHLBERG</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ED</td>
      <td>CHASE</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>JENNIFER</td>
      <td>DAVIS</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>JOHNNY</td>
      <td>LOLLOBRIGIDA</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



### 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to something that can hold more than varchar.



```python
cur = conn.cursor()
cur.execute('ALTER TABLE actor ALTER COLUMN middle_name TYPE text;')
df = pd.read_sql('SELECT * FROM actor', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
      <th>middle_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>PENELOPE</td>
      <td>GUINESS</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NICK</td>
      <td>WAHLBERG</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ED</td>
      <td>CHASE</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>JENNIFER</td>
      <td>DAVIS</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>JOHNNY</td>
      <td>LOLLOBRIGIDA</td>
      <td>2006-02-15 09:34:33</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



### 3c. Now write a query that would remove the middle_name column.



```python
cur = conn.cursor()
cur.execute('ALTER TABLE actor DROP COLUMN IF EXISTS middle_name;')
df = pd.read_sql('SELECT * FROM actor', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>PENELOPE</td>
      <td>GUINESS</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NICK</td>
      <td>WAHLBERG</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ED</td>
      <td>CHASE</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>JENNIFER</td>
      <td>DAVIS</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>JOHNNY</td>
      <td>LOLLOBRIGIDA</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
  </tbody>
</table>
</div>



### 4a. List the last names of actors, as well as how many actors have that last name.



```python
df = pd.read_sql('SELECT last_name, COUNT(*) FROM actor GROUP BY last_name ORDER BY last_name', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AKROYD</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALLEN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ASTAIRE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BACALL</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BAILEY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>BALE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>BALL</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>BARRYMORE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>BASINGER</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>BENING</td>
      <td>2</td>
    </tr>
    <tr>
      <th>10</th>
      <td>BERGEN</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>BERGMAN</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>BERRY</td>
      <td>3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>BIRCH</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>BLOOM</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>BOLGER</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>BRIDGES</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>BRODY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>BULLOCK</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>CAGE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>CARREY</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>CHAPLIN</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>CHASE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>23</th>
      <td>CLOSE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>COSTNER</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>CRAWFORD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>26</th>
      <td>CRONYN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>27</th>
      <td>CROWE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>CRUISE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>29</th>
      <td>CRUZ</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>91</th>
      <td>POSEY</td>
      <td>1</td>
    </tr>
    <tr>
      <th>92</th>
      <td>PRESLEY</td>
      <td>1</td>
    </tr>
    <tr>
      <th>93</th>
      <td>REYNOLDS</td>
      <td>1</td>
    </tr>
    <tr>
      <th>94</th>
      <td>RYDER</td>
      <td>1</td>
    </tr>
    <tr>
      <th>95</th>
      <td>SILVERSTONE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>96</th>
      <td>SINATRA</td>
      <td>1</td>
    </tr>
    <tr>
      <th>97</th>
      <td>SOBIESKI</td>
      <td>1</td>
    </tr>
    <tr>
      <th>98</th>
      <td>STALLONE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>99</th>
      <td>STREEP</td>
      <td>2</td>
    </tr>
    <tr>
      <th>100</th>
      <td>SUVARI</td>
      <td>1</td>
    </tr>
    <tr>
      <th>101</th>
      <td>SWANK</td>
      <td>1</td>
    </tr>
    <tr>
      <th>102</th>
      <td>TANDY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>103</th>
      <td>TAUTOU</td>
      <td>1</td>
    </tr>
    <tr>
      <th>104</th>
      <td>TEMPLE</td>
      <td>4</td>
    </tr>
    <tr>
      <th>105</th>
      <td>TOMEI</td>
      <td>1</td>
    </tr>
    <tr>
      <th>106</th>
      <td>TORN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>107</th>
      <td>TRACY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>108</th>
      <td>VOIGHT</td>
      <td>1</td>
    </tr>
    <tr>
      <th>109</th>
      <td>WAHLBERG</td>
      <td>2</td>
    </tr>
    <tr>
      <th>110</th>
      <td>WALKEN</td>
      <td>1</td>
    </tr>
    <tr>
      <th>111</th>
      <td>WAYNE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>112</th>
      <td>WEST</td>
      <td>2</td>
    </tr>
    <tr>
      <th>113</th>
      <td>WILLIAMS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>114</th>
      <td>WILLIS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>115</th>
      <td>WILSON</td>
      <td>1</td>
    </tr>
    <tr>
      <th>116</th>
      <td>WINSLET</td>
      <td>2</td>
    </tr>
    <tr>
      <th>117</th>
      <td>WITHERSPOON</td>
      <td>1</td>
    </tr>
    <tr>
      <th>118</th>
      <td>WOOD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>119</th>
      <td>WRAY</td>
      <td>1</td>
    </tr>
    <tr>
      <th>120</th>
      <td>ZELLWEGER</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
<p>121 rows × 2 columns</p>
</div>



### 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors



```python
df = pd.read_sql('SELECT last_name, COUNT(*) FROM actor GROUP BY last_name HAVING COUNT(*) >= 2 ORDER BY last_name', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AKROYD</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALLEN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BAILEY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BENING</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BERRY</td>
      <td>3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>BOLGER</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>BRODY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>CAGE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>CHASE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>9</th>
      <td>CRAWFORD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>10</th>
      <td>CRONYN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>DAVIS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>12</th>
      <td>DEAN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>DEE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>DEGENERES</td>
      <td>3</td>
    </tr>
    <tr>
      <th>15</th>
      <td>DENCH</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>DEPP</td>
      <td>2</td>
    </tr>
    <tr>
      <th>17</th>
      <td>DUKAKIS</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>FAWCETT</td>
      <td>2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>GARLAND</td>
      <td>3</td>
    </tr>
    <tr>
      <th>20</th>
      <td>GOODING</td>
      <td>2</td>
    </tr>
    <tr>
      <th>21</th>
      <td>GUINESS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>22</th>
      <td>HACKMAN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>23</th>
      <td>HARRIS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>24</th>
      <td>HOFFMAN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>25</th>
      <td>HOPKINS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>26</th>
      <td>HOPPER</td>
      <td>2</td>
    </tr>
    <tr>
      <th>27</th>
      <td>JACKMAN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>28</th>
      <td>JOHANSSON</td>
      <td>3</td>
    </tr>
    <tr>
      <th>29</th>
      <td>KEITEL</td>
      <td>3</td>
    </tr>
    <tr>
      <th>30</th>
      <td>KILMER</td>
      <td>5</td>
    </tr>
    <tr>
      <th>31</th>
      <td>MCCONAUGHEY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>32</th>
      <td>MCKELLEN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>33</th>
      <td>MCQUEEN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>34</th>
      <td>MONROE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>35</th>
      <td>MOSTEL</td>
      <td>2</td>
    </tr>
    <tr>
      <th>36</th>
      <td>NEESON</td>
      <td>2</td>
    </tr>
    <tr>
      <th>37</th>
      <td>NOLTE</td>
      <td>4</td>
    </tr>
    <tr>
      <th>38</th>
      <td>OLIVIER</td>
      <td>2</td>
    </tr>
    <tr>
      <th>39</th>
      <td>PALTROW</td>
      <td>2</td>
    </tr>
    <tr>
      <th>40</th>
      <td>PECK</td>
      <td>3</td>
    </tr>
    <tr>
      <th>41</th>
      <td>PENN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>42</th>
      <td>SILVERSTONE</td>
      <td>2</td>
    </tr>
    <tr>
      <th>43</th>
      <td>STREEP</td>
      <td>2</td>
    </tr>
    <tr>
      <th>44</th>
      <td>TANDY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>45</th>
      <td>TEMPLE</td>
      <td>4</td>
    </tr>
    <tr>
      <th>46</th>
      <td>TORN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>47</th>
      <td>TRACY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>48</th>
      <td>WAHLBERG</td>
      <td>2</td>
    </tr>
    <tr>
      <th>49</th>
      <td>WEST</td>
      <td>2</td>
    </tr>
    <tr>
      <th>50</th>
      <td>WILLIAMS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>51</th>
      <td>WILLIS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>52</th>
      <td>WINSLET</td>
      <td>2</td>
    </tr>
    <tr>
      <th>53</th>
      <td>WOOD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>54</th>
      <td>ZELLWEGER</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



### 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.



```python
df = pd.read_sql('SELECT * FROM actor WHERE first_name ilike \'Groucho\' and last_name ilike \'Williams\'', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>172</td>
      <td>GROUCHO</td>
      <td>WILLIAMS</td>
      <td>2006-02-15 09:34:33</td>
    </tr>
  </tbody>
</table>
</div>




```python
cur = conn.cursor()
cur.execute('UPDATE actor SET first_name = \'HARPO\' WHERE first_name ilike \'Groucho\' and last_name ilike \'Williams\';')

```


```python
df = pd.read_sql('SELECT * FROM actor WHERE actor_id = 172', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>172</td>
      <td>HARPO</td>
      <td>WILLIAMS</td>
      <td>2017-09-24 17:30:14.644315</td>
    </tr>
  </tbody>
</table>
</div>



### 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! 


```python
cur = conn.cursor()
cur.execute('UPDATE actor SET first_name = CASE WHEN first_name = \'HARPO\' THEN \'GROUCHO\' ELSE \'MUCHO GROUCHO\' END WHERE actor_id = 172;')
#cur.execute('UPDATE actor SET first_name = \'HARPO\' WHERE actor_id = 172;')

```


```python
df = pd.read_sql('SELECT * FROM actor WHERE actor_id = 172', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>172</td>
      <td>GROUCHO</td>
      <td>WILLIAMS</td>
      <td>2017-09-24 17:30:14.644315</td>
    </tr>
  </tbody>
</table>
</div>



### 5a. What’s the difference between a left join and a right join?


#### Left Join
A left join returns all rows in the left table and matching rows in the right table.
In the example below, the address table has 603 rows.
In a left join from the address table to the city table, each address row is returned with the matching city value from the city table.   The left join returns 603 rows.



```python
df = pd.read_sql('SELECT COUNT(*) FROM address;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>603</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = pd.read_sql('SELECT a.address_id, a.city_id, c.city FROM address a LEFT JOIN city c ON a.city_id = c.city_id ORDER BY a.address_id DESC;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address_id</th>
      <th>city_id</th>
      <th>city</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>605</td>
      <td>537</td>
      <td>Tieli</td>
    </tr>
    <tr>
      <th>1</th>
      <td>604</td>
      <td>296</td>
      <td>Lausanne</td>
    </tr>
    <tr>
      <th>2</th>
      <td>603</td>
      <td>503</td>
      <td>Sullana</td>
    </tr>
    <tr>
      <th>3</th>
      <td>602</td>
      <td>401</td>
      <td>Patras</td>
    </tr>
    <tr>
      <th>4</th>
      <td>601</td>
      <td>242</td>
      <td>Jinzhou</td>
    </tr>
    <tr>
      <th>5</th>
      <td>600</td>
      <td>241</td>
      <td>Jining</td>
    </tr>
    <tr>
      <th>6</th>
      <td>599</td>
      <td>177</td>
      <td>Garden Grove</td>
    </tr>
    <tr>
      <th>7</th>
      <td>598</td>
      <td>512</td>
      <td>Szkesfehrvr</td>
    </tr>
    <tr>
      <th>8</th>
      <td>597</td>
      <td>248</td>
      <td>Juiz de Fora</td>
    </tr>
    <tr>
      <th>9</th>
      <td>596</td>
      <td>14</td>
      <td>al-Manama</td>
    </tr>
    <tr>
      <th>10</th>
      <td>595</td>
      <td>311</td>
      <td>Loja</td>
    </tr>
    <tr>
      <th>11</th>
      <td>594</td>
      <td>574</td>
      <td>Weifang</td>
    </tr>
    <tr>
      <th>12</th>
      <td>593</td>
      <td>106</td>
      <td>Celaya</td>
    </tr>
    <tr>
      <th>13</th>
      <td>592</td>
      <td>546</td>
      <td>Tsaotun</td>
    </tr>
    <tr>
      <th>14</th>
      <td>591</td>
      <td>424</td>
      <td>Quilmes</td>
    </tr>
    <tr>
      <th>15</th>
      <td>590</td>
      <td>54</td>
      <td>Banjul</td>
    </tr>
    <tr>
      <th>16</th>
      <td>589</td>
      <td>494</td>
      <td>Southampton</td>
    </tr>
    <tr>
      <th>17</th>
      <td>588</td>
      <td>212</td>
      <td>Huejutla de Reyes</td>
    </tr>
    <tr>
      <th>18</th>
      <td>587</td>
      <td>246</td>
      <td>Jos Azueta</td>
    </tr>
    <tr>
      <th>19</th>
      <td>586</td>
      <td>219</td>
      <td>Iligan</td>
    </tr>
    <tr>
      <th>20</th>
      <td>585</td>
      <td>344</td>
      <td>Mosul</td>
    </tr>
    <tr>
      <th>21</th>
      <td>584</td>
      <td>103</td>
      <td>Carmen</td>
    </tr>
    <tr>
      <th>22</th>
      <td>583</td>
      <td>526</td>
      <td>Tanshui</td>
    </tr>
    <tr>
      <th>23</th>
      <td>582</td>
      <td>168</td>
      <td>Fengshan</td>
    </tr>
    <tr>
      <th>24</th>
      <td>581</td>
      <td>131</td>
      <td>Cuernavaca</td>
    </tr>
    <tr>
      <th>25</th>
      <td>580</td>
      <td>10</td>
      <td>Akishima</td>
    </tr>
    <tr>
      <th>26</th>
      <td>579</td>
      <td>598</td>
      <td>Zhezqazghan</td>
    </tr>
    <tr>
      <th>27</th>
      <td>578</td>
      <td>133</td>
      <td>Czestochowa</td>
    </tr>
    <tr>
      <th>28</th>
      <td>577</td>
      <td>409</td>
      <td>Plock</td>
    </tr>
    <tr>
      <th>29</th>
      <td>576</td>
      <td>341</td>
      <td>Monclova</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>573</th>
      <td>30</td>
      <td>121</td>
      <td>Citt del Vaticano</td>
    </tr>
    <tr>
      <th>574</th>
      <td>29</td>
      <td>472</td>
      <td>Shikarpur</td>
    </tr>
    <tr>
      <th>575</th>
      <td>28</td>
      <td>128</td>
      <td>Crdoba</td>
    </tr>
    <tr>
      <th>576</th>
      <td>27</td>
      <td>303</td>
      <td>Liepaja</td>
    </tr>
    <tr>
      <th>577</th>
      <td>26</td>
      <td>443</td>
      <td>Sal</td>
    </tr>
    <tr>
      <th>578</th>
      <td>25</td>
      <td>525</td>
      <td>Tangail</td>
    </tr>
    <tr>
      <th>579</th>
      <td>24</td>
      <td>327</td>
      <td>Mardan</td>
    </tr>
    <tr>
      <th>580</th>
      <td>23</td>
      <td>267</td>
      <td>Kimberley</td>
    </tr>
    <tr>
      <th>581</th>
      <td>22</td>
      <td>252</td>
      <td>Kaduna</td>
    </tr>
    <tr>
      <th>582</th>
      <td>21</td>
      <td>156</td>
      <td>Elista</td>
    </tr>
    <tr>
      <th>583</th>
      <td>20</td>
      <td>495</td>
      <td>Southend-on-Sea</td>
    </tr>
    <tr>
      <th>584</th>
      <td>19</td>
      <td>76</td>
      <td>Bhopal</td>
    </tr>
    <tr>
      <th>585</th>
      <td>18</td>
      <td>120</td>
      <td>Citrus Heights</td>
    </tr>
    <tr>
      <th>586</th>
      <td>17</td>
      <td>384</td>
      <td>Osmaniye</td>
    </tr>
    <tr>
      <th>587</th>
      <td>16</td>
      <td>582</td>
      <td>Yamuna Nagar</td>
    </tr>
    <tr>
      <th>588</th>
      <td>15</td>
      <td>440</td>
      <td>Sagamihara</td>
    </tr>
    <tr>
      <th>589</th>
      <td>14</td>
      <td>162</td>
      <td>Esfahan</td>
    </tr>
    <tr>
      <th>590</th>
      <td>13</td>
      <td>329</td>
      <td>Masqat</td>
    </tr>
    <tr>
      <th>591</th>
      <td>12</td>
      <td>200</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>592</th>
      <td>11</td>
      <td>280</td>
      <td>Kragujevac</td>
    </tr>
    <tr>
      <th>593</th>
      <td>10</td>
      <td>295</td>
      <td>Laredo</td>
    </tr>
    <tr>
      <th>594</th>
      <td>9</td>
      <td>361</td>
      <td>Nantou</td>
    </tr>
    <tr>
      <th>595</th>
      <td>8</td>
      <td>349</td>
      <td>Myingyan</td>
    </tr>
    <tr>
      <th>596</th>
      <td>7</td>
      <td>38</td>
      <td>Athenai</td>
    </tr>
    <tr>
      <th>597</th>
      <td>6</td>
      <td>449</td>
      <td>San Bernardino</td>
    </tr>
    <tr>
      <th>598</th>
      <td>5</td>
      <td>463</td>
      <td>Sasebo</td>
    </tr>
    <tr>
      <th>599</th>
      <td>4</td>
      <td>576</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>600</th>
      <td>3</td>
      <td>300</td>
      <td>Lethbridge</td>
    </tr>
    <tr>
      <th>601</th>
      <td>2</td>
      <td>576</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>602</th>
      <td>1</td>
      <td>300</td>
      <td>Lethbridge</td>
    </tr>
  </tbody>
</table>
<p>603 rows × 3 columns</p>
</div>



#### Right Joint
A right join returns all rows in the right table and matching rows in the left table. In the example below, the city table has 600 rows.
In a right join to the address table, each city row is returned with the matching address value from the address table.   The right join returns 604 rows.  The city London has no address with a city in London.



```python
df = pd.read_sql('SELECT COUNT(*) FROM city;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>600</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = pd.read_sql('SELECT a.address_id, a.city_id, c.city FROM address a RIGHT JOIN city c ON a.city_id = c.city_id ORDER BY a.address_id DESC;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address_id</th>
      <th>city_id</th>
      <th>city</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>London</td>
    </tr>
    <tr>
      <th>1</th>
      <td>605.0</td>
      <td>537.0</td>
      <td>Tieli</td>
    </tr>
    <tr>
      <th>2</th>
      <td>604.0</td>
      <td>296.0</td>
      <td>Lausanne</td>
    </tr>
    <tr>
      <th>3</th>
      <td>603.0</td>
      <td>503.0</td>
      <td>Sullana</td>
    </tr>
    <tr>
      <th>4</th>
      <td>602.0</td>
      <td>401.0</td>
      <td>Patras</td>
    </tr>
    <tr>
      <th>5</th>
      <td>601.0</td>
      <td>242.0</td>
      <td>Jinzhou</td>
    </tr>
    <tr>
      <th>6</th>
      <td>600.0</td>
      <td>241.0</td>
      <td>Jining</td>
    </tr>
    <tr>
      <th>7</th>
      <td>599.0</td>
      <td>177.0</td>
      <td>Garden Grove</td>
    </tr>
    <tr>
      <th>8</th>
      <td>598.0</td>
      <td>512.0</td>
      <td>Szkesfehrvr</td>
    </tr>
    <tr>
      <th>9</th>
      <td>597.0</td>
      <td>248.0</td>
      <td>Juiz de Fora</td>
    </tr>
    <tr>
      <th>10</th>
      <td>596.0</td>
      <td>14.0</td>
      <td>al-Manama</td>
    </tr>
    <tr>
      <th>11</th>
      <td>595.0</td>
      <td>311.0</td>
      <td>Loja</td>
    </tr>
    <tr>
      <th>12</th>
      <td>594.0</td>
      <td>574.0</td>
      <td>Weifang</td>
    </tr>
    <tr>
      <th>13</th>
      <td>593.0</td>
      <td>106.0</td>
      <td>Celaya</td>
    </tr>
    <tr>
      <th>14</th>
      <td>592.0</td>
      <td>546.0</td>
      <td>Tsaotun</td>
    </tr>
    <tr>
      <th>15</th>
      <td>591.0</td>
      <td>424.0</td>
      <td>Quilmes</td>
    </tr>
    <tr>
      <th>16</th>
      <td>590.0</td>
      <td>54.0</td>
      <td>Banjul</td>
    </tr>
    <tr>
      <th>17</th>
      <td>589.0</td>
      <td>494.0</td>
      <td>Southampton</td>
    </tr>
    <tr>
      <th>18</th>
      <td>588.0</td>
      <td>212.0</td>
      <td>Huejutla de Reyes</td>
    </tr>
    <tr>
      <th>19</th>
      <td>587.0</td>
      <td>246.0</td>
      <td>Jos Azueta</td>
    </tr>
    <tr>
      <th>20</th>
      <td>586.0</td>
      <td>219.0</td>
      <td>Iligan</td>
    </tr>
    <tr>
      <th>21</th>
      <td>585.0</td>
      <td>344.0</td>
      <td>Mosul</td>
    </tr>
    <tr>
      <th>22</th>
      <td>584.0</td>
      <td>103.0</td>
      <td>Carmen</td>
    </tr>
    <tr>
      <th>23</th>
      <td>583.0</td>
      <td>526.0</td>
      <td>Tanshui</td>
    </tr>
    <tr>
      <th>24</th>
      <td>582.0</td>
      <td>168.0</td>
      <td>Fengshan</td>
    </tr>
    <tr>
      <th>25</th>
      <td>581.0</td>
      <td>131.0</td>
      <td>Cuernavaca</td>
    </tr>
    <tr>
      <th>26</th>
      <td>580.0</td>
      <td>10.0</td>
      <td>Akishima</td>
    </tr>
    <tr>
      <th>27</th>
      <td>579.0</td>
      <td>598.0</td>
      <td>Zhezqazghan</td>
    </tr>
    <tr>
      <th>28</th>
      <td>578.0</td>
      <td>133.0</td>
      <td>Czestochowa</td>
    </tr>
    <tr>
      <th>29</th>
      <td>577.0</td>
      <td>409.0</td>
      <td>Plock</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>574</th>
      <td>30.0</td>
      <td>121.0</td>
      <td>Citt del Vaticano</td>
    </tr>
    <tr>
      <th>575</th>
      <td>29.0</td>
      <td>472.0</td>
      <td>Shikarpur</td>
    </tr>
    <tr>
      <th>576</th>
      <td>28.0</td>
      <td>128.0</td>
      <td>Crdoba</td>
    </tr>
    <tr>
      <th>577</th>
      <td>27.0</td>
      <td>303.0</td>
      <td>Liepaja</td>
    </tr>
    <tr>
      <th>578</th>
      <td>26.0</td>
      <td>443.0</td>
      <td>Sal</td>
    </tr>
    <tr>
      <th>579</th>
      <td>25.0</td>
      <td>525.0</td>
      <td>Tangail</td>
    </tr>
    <tr>
      <th>580</th>
      <td>24.0</td>
      <td>327.0</td>
      <td>Mardan</td>
    </tr>
    <tr>
      <th>581</th>
      <td>23.0</td>
      <td>267.0</td>
      <td>Kimberley</td>
    </tr>
    <tr>
      <th>582</th>
      <td>22.0</td>
      <td>252.0</td>
      <td>Kaduna</td>
    </tr>
    <tr>
      <th>583</th>
      <td>21.0</td>
      <td>156.0</td>
      <td>Elista</td>
    </tr>
    <tr>
      <th>584</th>
      <td>20.0</td>
      <td>495.0</td>
      <td>Southend-on-Sea</td>
    </tr>
    <tr>
      <th>585</th>
      <td>19.0</td>
      <td>76.0</td>
      <td>Bhopal</td>
    </tr>
    <tr>
      <th>586</th>
      <td>18.0</td>
      <td>120.0</td>
      <td>Citrus Heights</td>
    </tr>
    <tr>
      <th>587</th>
      <td>17.0</td>
      <td>384.0</td>
      <td>Osmaniye</td>
    </tr>
    <tr>
      <th>588</th>
      <td>16.0</td>
      <td>582.0</td>
      <td>Yamuna Nagar</td>
    </tr>
    <tr>
      <th>589</th>
      <td>15.0</td>
      <td>440.0</td>
      <td>Sagamihara</td>
    </tr>
    <tr>
      <th>590</th>
      <td>14.0</td>
      <td>162.0</td>
      <td>Esfahan</td>
    </tr>
    <tr>
      <th>591</th>
      <td>13.0</td>
      <td>329.0</td>
      <td>Masqat</td>
    </tr>
    <tr>
      <th>592</th>
      <td>12.0</td>
      <td>200.0</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>593</th>
      <td>11.0</td>
      <td>280.0</td>
      <td>Kragujevac</td>
    </tr>
    <tr>
      <th>594</th>
      <td>10.0</td>
      <td>295.0</td>
      <td>Laredo</td>
    </tr>
    <tr>
      <th>595</th>
      <td>9.0</td>
      <td>361.0</td>
      <td>Nantou</td>
    </tr>
    <tr>
      <th>596</th>
      <td>8.0</td>
      <td>349.0</td>
      <td>Myingyan</td>
    </tr>
    <tr>
      <th>597</th>
      <td>7.0</td>
      <td>38.0</td>
      <td>Athenai</td>
    </tr>
    <tr>
      <th>598</th>
      <td>6.0</td>
      <td>449.0</td>
      <td>San Bernardino</td>
    </tr>
    <tr>
      <th>599</th>
      <td>5.0</td>
      <td>463.0</td>
      <td>Sasebo</td>
    </tr>
    <tr>
      <th>600</th>
      <td>4.0</td>
      <td>576.0</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>601</th>
      <td>3.0</td>
      <td>300.0</td>
      <td>Lethbridge</td>
    </tr>
    <tr>
      <th>602</th>
      <td>2.0</td>
      <td>576.0</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>603</th>
      <td>1.0</td>
      <td>300.0</td>
      <td>Lethbridge</td>
    </tr>
  </tbody>
</table>
<p>604 rows × 3 columns</p>
</div>



### 5b. What about an inner join and an outer join?

### Inner Join
An inner join returns only matching rows between the left and right table.


```python
df = pd.read_sql('SELECT a.address_id, a.city_id, c.city FROM address a JOIN city c ON a.city_id = c.city_id ORDER BY a.address_id DESC;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address_id</th>
      <th>city_id</th>
      <th>city</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>605</td>
      <td>537</td>
      <td>Tieli</td>
    </tr>
    <tr>
      <th>1</th>
      <td>604</td>
      <td>296</td>
      <td>Lausanne</td>
    </tr>
    <tr>
      <th>2</th>
      <td>603</td>
      <td>503</td>
      <td>Sullana</td>
    </tr>
    <tr>
      <th>3</th>
      <td>602</td>
      <td>401</td>
      <td>Patras</td>
    </tr>
    <tr>
      <th>4</th>
      <td>601</td>
      <td>242</td>
      <td>Jinzhou</td>
    </tr>
    <tr>
      <th>5</th>
      <td>600</td>
      <td>241</td>
      <td>Jining</td>
    </tr>
    <tr>
      <th>6</th>
      <td>599</td>
      <td>177</td>
      <td>Garden Grove</td>
    </tr>
    <tr>
      <th>7</th>
      <td>598</td>
      <td>512</td>
      <td>Szkesfehrvr</td>
    </tr>
    <tr>
      <th>8</th>
      <td>597</td>
      <td>248</td>
      <td>Juiz de Fora</td>
    </tr>
    <tr>
      <th>9</th>
      <td>596</td>
      <td>14</td>
      <td>al-Manama</td>
    </tr>
    <tr>
      <th>10</th>
      <td>595</td>
      <td>311</td>
      <td>Loja</td>
    </tr>
    <tr>
      <th>11</th>
      <td>594</td>
      <td>574</td>
      <td>Weifang</td>
    </tr>
    <tr>
      <th>12</th>
      <td>593</td>
      <td>106</td>
      <td>Celaya</td>
    </tr>
    <tr>
      <th>13</th>
      <td>592</td>
      <td>546</td>
      <td>Tsaotun</td>
    </tr>
    <tr>
      <th>14</th>
      <td>591</td>
      <td>424</td>
      <td>Quilmes</td>
    </tr>
    <tr>
      <th>15</th>
      <td>590</td>
      <td>54</td>
      <td>Banjul</td>
    </tr>
    <tr>
      <th>16</th>
      <td>589</td>
      <td>494</td>
      <td>Southampton</td>
    </tr>
    <tr>
      <th>17</th>
      <td>588</td>
      <td>212</td>
      <td>Huejutla de Reyes</td>
    </tr>
    <tr>
      <th>18</th>
      <td>587</td>
      <td>246</td>
      <td>Jos Azueta</td>
    </tr>
    <tr>
      <th>19</th>
      <td>586</td>
      <td>219</td>
      <td>Iligan</td>
    </tr>
    <tr>
      <th>20</th>
      <td>585</td>
      <td>344</td>
      <td>Mosul</td>
    </tr>
    <tr>
      <th>21</th>
      <td>584</td>
      <td>103</td>
      <td>Carmen</td>
    </tr>
    <tr>
      <th>22</th>
      <td>583</td>
      <td>526</td>
      <td>Tanshui</td>
    </tr>
    <tr>
      <th>23</th>
      <td>582</td>
      <td>168</td>
      <td>Fengshan</td>
    </tr>
    <tr>
      <th>24</th>
      <td>581</td>
      <td>131</td>
      <td>Cuernavaca</td>
    </tr>
    <tr>
      <th>25</th>
      <td>580</td>
      <td>10</td>
      <td>Akishima</td>
    </tr>
    <tr>
      <th>26</th>
      <td>579</td>
      <td>598</td>
      <td>Zhezqazghan</td>
    </tr>
    <tr>
      <th>27</th>
      <td>578</td>
      <td>133</td>
      <td>Czestochowa</td>
    </tr>
    <tr>
      <th>28</th>
      <td>577</td>
      <td>409</td>
      <td>Plock</td>
    </tr>
    <tr>
      <th>29</th>
      <td>576</td>
      <td>341</td>
      <td>Monclova</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>573</th>
      <td>30</td>
      <td>121</td>
      <td>Citt del Vaticano</td>
    </tr>
    <tr>
      <th>574</th>
      <td>29</td>
      <td>472</td>
      <td>Shikarpur</td>
    </tr>
    <tr>
      <th>575</th>
      <td>28</td>
      <td>128</td>
      <td>Crdoba</td>
    </tr>
    <tr>
      <th>576</th>
      <td>27</td>
      <td>303</td>
      <td>Liepaja</td>
    </tr>
    <tr>
      <th>577</th>
      <td>26</td>
      <td>443</td>
      <td>Sal</td>
    </tr>
    <tr>
      <th>578</th>
      <td>25</td>
      <td>525</td>
      <td>Tangail</td>
    </tr>
    <tr>
      <th>579</th>
      <td>24</td>
      <td>327</td>
      <td>Mardan</td>
    </tr>
    <tr>
      <th>580</th>
      <td>23</td>
      <td>267</td>
      <td>Kimberley</td>
    </tr>
    <tr>
      <th>581</th>
      <td>22</td>
      <td>252</td>
      <td>Kaduna</td>
    </tr>
    <tr>
      <th>582</th>
      <td>21</td>
      <td>156</td>
      <td>Elista</td>
    </tr>
    <tr>
      <th>583</th>
      <td>20</td>
      <td>495</td>
      <td>Southend-on-Sea</td>
    </tr>
    <tr>
      <th>584</th>
      <td>19</td>
      <td>76</td>
      <td>Bhopal</td>
    </tr>
    <tr>
      <th>585</th>
      <td>18</td>
      <td>120</td>
      <td>Citrus Heights</td>
    </tr>
    <tr>
      <th>586</th>
      <td>17</td>
      <td>384</td>
      <td>Osmaniye</td>
    </tr>
    <tr>
      <th>587</th>
      <td>16</td>
      <td>582</td>
      <td>Yamuna Nagar</td>
    </tr>
    <tr>
      <th>588</th>
      <td>15</td>
      <td>440</td>
      <td>Sagamihara</td>
    </tr>
    <tr>
      <th>589</th>
      <td>14</td>
      <td>162</td>
      <td>Esfahan</td>
    </tr>
    <tr>
      <th>590</th>
      <td>13</td>
      <td>329</td>
      <td>Masqat</td>
    </tr>
    <tr>
      <th>591</th>
      <td>12</td>
      <td>200</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>592</th>
      <td>11</td>
      <td>280</td>
      <td>Kragujevac</td>
    </tr>
    <tr>
      <th>593</th>
      <td>10</td>
      <td>295</td>
      <td>Laredo</td>
    </tr>
    <tr>
      <th>594</th>
      <td>9</td>
      <td>361</td>
      <td>Nantou</td>
    </tr>
    <tr>
      <th>595</th>
      <td>8</td>
      <td>349</td>
      <td>Myingyan</td>
    </tr>
    <tr>
      <th>596</th>
      <td>7</td>
      <td>38</td>
      <td>Athenai</td>
    </tr>
    <tr>
      <th>597</th>
      <td>6</td>
      <td>449</td>
      <td>San Bernardino</td>
    </tr>
    <tr>
      <th>598</th>
      <td>5</td>
      <td>463</td>
      <td>Sasebo</td>
    </tr>
    <tr>
      <th>599</th>
      <td>4</td>
      <td>576</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>600</th>
      <td>3</td>
      <td>300</td>
      <td>Lethbridge</td>
    </tr>
    <tr>
      <th>601</th>
      <td>2</td>
      <td>576</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>602</th>
      <td>1</td>
      <td>300</td>
      <td>Lethbridge</td>
    </tr>
  </tbody>
</table>
<p>603 rows × 3 columns</p>
</div>



### Full Outer Join
A full outer join will return matching rows from the left and right table and non-matching rows returning null for non-matching columns.  In the example below, London is in the city table but has no matching address value and returns null.


```python
df = pd.read_sql('SELECT a.address_id, a.city_id, c.city FROM address a FULL OUTER JOIN city c ON a.city_id = c.city_id ORDER BY a.address_id DESC;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address_id</th>
      <th>city_id</th>
      <th>city</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>London</td>
    </tr>
    <tr>
      <th>1</th>
      <td>605.0</td>
      <td>537.0</td>
      <td>Tieli</td>
    </tr>
    <tr>
      <th>2</th>
      <td>604.0</td>
      <td>296.0</td>
      <td>Lausanne</td>
    </tr>
    <tr>
      <th>3</th>
      <td>603.0</td>
      <td>503.0</td>
      <td>Sullana</td>
    </tr>
    <tr>
      <th>4</th>
      <td>602.0</td>
      <td>401.0</td>
      <td>Patras</td>
    </tr>
    <tr>
      <th>5</th>
      <td>601.0</td>
      <td>242.0</td>
      <td>Jinzhou</td>
    </tr>
    <tr>
      <th>6</th>
      <td>600.0</td>
      <td>241.0</td>
      <td>Jining</td>
    </tr>
    <tr>
      <th>7</th>
      <td>599.0</td>
      <td>177.0</td>
      <td>Garden Grove</td>
    </tr>
    <tr>
      <th>8</th>
      <td>598.0</td>
      <td>512.0</td>
      <td>Szkesfehrvr</td>
    </tr>
    <tr>
      <th>9</th>
      <td>597.0</td>
      <td>248.0</td>
      <td>Juiz de Fora</td>
    </tr>
    <tr>
      <th>10</th>
      <td>596.0</td>
      <td>14.0</td>
      <td>al-Manama</td>
    </tr>
    <tr>
      <th>11</th>
      <td>595.0</td>
      <td>311.0</td>
      <td>Loja</td>
    </tr>
    <tr>
      <th>12</th>
      <td>594.0</td>
      <td>574.0</td>
      <td>Weifang</td>
    </tr>
    <tr>
      <th>13</th>
      <td>593.0</td>
      <td>106.0</td>
      <td>Celaya</td>
    </tr>
    <tr>
      <th>14</th>
      <td>592.0</td>
      <td>546.0</td>
      <td>Tsaotun</td>
    </tr>
    <tr>
      <th>15</th>
      <td>591.0</td>
      <td>424.0</td>
      <td>Quilmes</td>
    </tr>
    <tr>
      <th>16</th>
      <td>590.0</td>
      <td>54.0</td>
      <td>Banjul</td>
    </tr>
    <tr>
      <th>17</th>
      <td>589.0</td>
      <td>494.0</td>
      <td>Southampton</td>
    </tr>
    <tr>
      <th>18</th>
      <td>588.0</td>
      <td>212.0</td>
      <td>Huejutla de Reyes</td>
    </tr>
    <tr>
      <th>19</th>
      <td>587.0</td>
      <td>246.0</td>
      <td>Jos Azueta</td>
    </tr>
    <tr>
      <th>20</th>
      <td>586.0</td>
      <td>219.0</td>
      <td>Iligan</td>
    </tr>
    <tr>
      <th>21</th>
      <td>585.0</td>
      <td>344.0</td>
      <td>Mosul</td>
    </tr>
    <tr>
      <th>22</th>
      <td>584.0</td>
      <td>103.0</td>
      <td>Carmen</td>
    </tr>
    <tr>
      <th>23</th>
      <td>583.0</td>
      <td>526.0</td>
      <td>Tanshui</td>
    </tr>
    <tr>
      <th>24</th>
      <td>582.0</td>
      <td>168.0</td>
      <td>Fengshan</td>
    </tr>
    <tr>
      <th>25</th>
      <td>581.0</td>
      <td>131.0</td>
      <td>Cuernavaca</td>
    </tr>
    <tr>
      <th>26</th>
      <td>580.0</td>
      <td>10.0</td>
      <td>Akishima</td>
    </tr>
    <tr>
      <th>27</th>
      <td>579.0</td>
      <td>598.0</td>
      <td>Zhezqazghan</td>
    </tr>
    <tr>
      <th>28</th>
      <td>578.0</td>
      <td>133.0</td>
      <td>Czestochowa</td>
    </tr>
    <tr>
      <th>29</th>
      <td>577.0</td>
      <td>409.0</td>
      <td>Plock</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>574</th>
      <td>30.0</td>
      <td>121.0</td>
      <td>Citt del Vaticano</td>
    </tr>
    <tr>
      <th>575</th>
      <td>29.0</td>
      <td>472.0</td>
      <td>Shikarpur</td>
    </tr>
    <tr>
      <th>576</th>
      <td>28.0</td>
      <td>128.0</td>
      <td>Crdoba</td>
    </tr>
    <tr>
      <th>577</th>
      <td>27.0</td>
      <td>303.0</td>
      <td>Liepaja</td>
    </tr>
    <tr>
      <th>578</th>
      <td>26.0</td>
      <td>443.0</td>
      <td>Sal</td>
    </tr>
    <tr>
      <th>579</th>
      <td>25.0</td>
      <td>525.0</td>
      <td>Tangail</td>
    </tr>
    <tr>
      <th>580</th>
      <td>24.0</td>
      <td>327.0</td>
      <td>Mardan</td>
    </tr>
    <tr>
      <th>581</th>
      <td>23.0</td>
      <td>267.0</td>
      <td>Kimberley</td>
    </tr>
    <tr>
      <th>582</th>
      <td>22.0</td>
      <td>252.0</td>
      <td>Kaduna</td>
    </tr>
    <tr>
      <th>583</th>
      <td>21.0</td>
      <td>156.0</td>
      <td>Elista</td>
    </tr>
    <tr>
      <th>584</th>
      <td>20.0</td>
      <td>495.0</td>
      <td>Southend-on-Sea</td>
    </tr>
    <tr>
      <th>585</th>
      <td>19.0</td>
      <td>76.0</td>
      <td>Bhopal</td>
    </tr>
    <tr>
      <th>586</th>
      <td>18.0</td>
      <td>120.0</td>
      <td>Citrus Heights</td>
    </tr>
    <tr>
      <th>587</th>
      <td>17.0</td>
      <td>384.0</td>
      <td>Osmaniye</td>
    </tr>
    <tr>
      <th>588</th>
      <td>16.0</td>
      <td>582.0</td>
      <td>Yamuna Nagar</td>
    </tr>
    <tr>
      <th>589</th>
      <td>15.0</td>
      <td>440.0</td>
      <td>Sagamihara</td>
    </tr>
    <tr>
      <th>590</th>
      <td>14.0</td>
      <td>162.0</td>
      <td>Esfahan</td>
    </tr>
    <tr>
      <th>591</th>
      <td>13.0</td>
      <td>329.0</td>
      <td>Masqat</td>
    </tr>
    <tr>
      <th>592</th>
      <td>12.0</td>
      <td>200.0</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>593</th>
      <td>11.0</td>
      <td>280.0</td>
      <td>Kragujevac</td>
    </tr>
    <tr>
      <th>594</th>
      <td>10.0</td>
      <td>295.0</td>
      <td>Laredo</td>
    </tr>
    <tr>
      <th>595</th>
      <td>9.0</td>
      <td>361.0</td>
      <td>Nantou</td>
    </tr>
    <tr>
      <th>596</th>
      <td>8.0</td>
      <td>349.0</td>
      <td>Myingyan</td>
    </tr>
    <tr>
      <th>597</th>
      <td>7.0</td>
      <td>38.0</td>
      <td>Athenai</td>
    </tr>
    <tr>
      <th>598</th>
      <td>6.0</td>
      <td>449.0</td>
      <td>San Bernardino</td>
    </tr>
    <tr>
      <th>599</th>
      <td>5.0</td>
      <td>463.0</td>
      <td>Sasebo</td>
    </tr>
    <tr>
      <th>600</th>
      <td>4.0</td>
      <td>576.0</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>601</th>
      <td>3.0</td>
      <td>300.0</td>
      <td>Lethbridge</td>
    </tr>
    <tr>
      <th>602</th>
      <td>2.0</td>
      <td>576.0</td>
      <td>Woodridge</td>
    </tr>
    <tr>
      <th>603</th>
      <td>1.0</td>
      <td>300.0</td>
      <td>Lethbridge</td>
    </tr>
  </tbody>
</table>
<p>604 rows × 3 columns</p>
</div>



### 5c. When would you use rank? 
Rank assigns a unique number within your ordered partition. Ties are assigned the same rank, with the next ranking(s) skipped. So, if you have 3 items at rank 2, the next rank listed would be ranked 5.

### 5d. What about dense_rank? 
DENSE_RANK assigns a unique number within your ordered partition, but the ranks are consecutive. No ranks are skipped if there are ranks with multiple items.

### 5e. When would you use a subquery in a select? 
A subqueries are a tool for performing operations in multiple steps.  For example this query is done in two separate queries:


```python
df = pd.read_sql('SELECT AVG(p.amount) FROM payment p;', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4.200667</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = pd.read_sql('SELECT p.customer_id, p.amount FROM payment p WHERE p.amount > 4.2006673312979002;', con=conn)
df

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>269</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>269</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>270</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>271</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>272</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>5</th>
      <td>272</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>6</th>
      <td>274</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7</th>
      <td>274</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>8</th>
      <td>274</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>9</th>
      <td>276</td>
      <td>10.99</td>
    </tr>
    <tr>
      <th>10</th>
      <td>277</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>11</th>
      <td>278</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>12</th>
      <td>280</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>13</th>
      <td>282</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>14</th>
      <td>284</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>15</th>
      <td>286</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>16</th>
      <td>288</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>17</th>
      <td>288</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>18</th>
      <td>288</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>19</th>
      <td>291</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>20</th>
      <td>291</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>21</th>
      <td>293</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>22</th>
      <td>293</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>23</th>
      <td>296</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>24</th>
      <td>296</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>25</th>
      <td>296</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>26</th>
      <td>299</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>27</th>
      <td>299</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>28</th>
      <td>300</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>29</th>
      <td>301</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7716</th>
      <td>22</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7717</th>
      <td>42</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7718</th>
      <td>44</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7719</th>
      <td>52</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7720</th>
      <td>53</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7721</th>
      <td>56</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7722</th>
      <td>60</td>
      <td>9.98</td>
    </tr>
    <tr>
      <th>7723</th>
      <td>64</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7724</th>
      <td>75</td>
      <td>8.97</td>
    </tr>
    <tr>
      <th>7725</th>
      <td>83</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7726</th>
      <td>87</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7727</th>
      <td>91</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7728</th>
      <td>94</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7729</th>
      <td>108</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7730</th>
      <td>114</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7731</th>
      <td>120</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7732</th>
      <td>152</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7733</th>
      <td>155</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7734</th>
      <td>163</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7735</th>
      <td>178</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7736</th>
      <td>180</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7737</th>
      <td>190</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7738</th>
      <td>192</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7739</th>
      <td>208</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7740</th>
      <td>211</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7741</th>
      <td>216</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7742</th>
      <td>219</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7743</th>
      <td>227</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7744</th>
      <td>244</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7745</th>
      <td>252</td>
      <td>4.99</td>
    </tr>
  </tbody>
</table>
<p>7746 rows × 2 columns</p>
</div>



A subquery can be used to perform the same queries in a single query.


```python
df = pd.read_sql('SELECT p.customer_id, p.amount FROM payment p WHERE p.amount > (SELECT AVG(p.amount) FROM payment p);', con=conn)
df

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>269</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>1</th>
      <td>269</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>270</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>3</th>
      <td>271</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>272</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>5</th>
      <td>272</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>6</th>
      <td>274</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7</th>
      <td>274</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>8</th>
      <td>274</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>9</th>
      <td>276</td>
      <td>10.99</td>
    </tr>
    <tr>
      <th>10</th>
      <td>277</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>11</th>
      <td>278</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>12</th>
      <td>280</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>13</th>
      <td>282</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>14</th>
      <td>284</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>15</th>
      <td>286</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>16</th>
      <td>288</td>
      <td>6.99</td>
    </tr>
    <tr>
      <th>17</th>
      <td>288</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>18</th>
      <td>288</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>19</th>
      <td>291</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>20</th>
      <td>291</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>21</th>
      <td>293</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>22</th>
      <td>293</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>23</th>
      <td>296</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>24</th>
      <td>296</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>25</th>
      <td>296</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>26</th>
      <td>299</td>
      <td>5.99</td>
    </tr>
    <tr>
      <th>27</th>
      <td>299</td>
      <td>8.99</td>
    </tr>
    <tr>
      <th>28</th>
      <td>300</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>29</th>
      <td>301</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7716</th>
      <td>22</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7717</th>
      <td>42</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7718</th>
      <td>44</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7719</th>
      <td>52</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7720</th>
      <td>53</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7721</th>
      <td>56</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7722</th>
      <td>60</td>
      <td>9.98</td>
    </tr>
    <tr>
      <th>7723</th>
      <td>64</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7724</th>
      <td>75</td>
      <td>8.97</td>
    </tr>
    <tr>
      <th>7725</th>
      <td>83</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7726</th>
      <td>87</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7727</th>
      <td>91</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7728</th>
      <td>94</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7729</th>
      <td>108</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7730</th>
      <td>114</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7731</th>
      <td>120</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7732</th>
      <td>152</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7733</th>
      <td>155</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7734</th>
      <td>163</td>
      <td>7.98</td>
    </tr>
    <tr>
      <th>7735</th>
      <td>178</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7736</th>
      <td>180</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7737</th>
      <td>190</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7738</th>
      <td>192</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7739</th>
      <td>208</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7740</th>
      <td>211</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7741</th>
      <td>216</td>
      <td>5.98</td>
    </tr>
    <tr>
      <th>7742</th>
      <td>219</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7743</th>
      <td>227</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7744</th>
      <td>244</td>
      <td>4.99</td>
    </tr>
    <tr>
      <th>7745</th>
      <td>252</td>
      <td>4.99</td>
    </tr>
  </tbody>
</table>
<p>7746 rows × 2 columns</p>
</div>



### 5f. When would you use a right join?
When you want all rows from the right table and matching values from the left table.

### 5g. When would you use an inner join over an outer join?
When you only want rows that match in the left and right table use an inner join.


### 5h. What’s the difference between a left outer and a left join
A left outer and a left join are the same thing. Both return the rows in the left table and matching values in the right table. The word Outer is optional.

### 5i. When would you use a group by?
A group by is useful anytime you want to perform an aggregate calculation like max, min, sum, count... For example, if you wanted to know how many addresses are in each city, you can use the count function and group by city.



```python
df = pd.read_sql('SELECT city_id, count(*) as address_cnt FROM address GROUP BY city_id ORDER BY address_cnt DESC;', con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city_id</th>
      <th>address_cnt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>42</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>312</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>300</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>576</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>264</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### 5j. Describe how you would do data reformatting
You can use string functions like replace, position and substring to manipulate string values.  For example, you could replace the word "Drive" with "Dr." in the address.


```python
query = ("SELECT address,\n"
             "OVERLAY(address PLACING \'Dr. \' FROM POSITION(\'Drive\' IN address) FOR 5)\n"
         "FROM address\n"
         "WHERE address LIKE \'%Drive%\';\n")
df = pd.read_sql(query, con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address</th>
      <th>overlay</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>47 MySakila Drive</td>
      <td>47 MySakila Dr.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1411 Lillydale Drive</td>
      <td>1411 Lillydale Dr.</td>
    </tr>
    <tr>
      <th>2</th>
      <td>613 Korolev Drive</td>
      <td>613 Korolev Dr.</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1531 Sal Drive</td>
      <td>1531 Sal Dr.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>391 Callao Drive</td>
      <td>391 Callao Dr.</td>
    </tr>
  </tbody>
</table>
</div>



### 5k. When would you use a with clause?
A with clause is like an in-line view, that can only be executed once.  A with clause allows you to make a complicate query easier to read and also allows you to chain selects.  Below is an example with clause:


```python
query = ("WITH s AS(\n"
            "SELECT *\n"
            "FROM staff\n"
        ")\n"
        "SELECT s.staff_id, st.store_id\n"
        "FROM s\n"
        "LEFT JOIN store st ON st.store_id = s.store_id;\n")

df = pd.read_sql(query, con=conn)
df.head()


```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>staff_id</th>
      <th>store_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



### 5l. bonus: When would you use a self join?
You can use a self join to join a table to itself.  For example, you can use a self join to delete duplicates in a table. The example below shows duplicate actors with the same last name.


```python
query = ("SELECT DISTINCT a.actor_id, a.last_name\n"
        "FROM actor a, actor b\n"
        "WHERE a.actor_id > b.actor_id\n"
            "AND a.last_name = b.last_name\n"
        "ORDER BY a.last_name;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>92</td>
      <td>AKROYD</td>
    </tr>
    <tr>
      <th>1</th>
      <td>182</td>
      <td>AKROYD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>145</td>
      <td>ALLEN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>194</td>
      <td>ALLEN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>190</td>
      <td>BAILEY</td>
    </tr>
    <tr>
      <th>5</th>
      <td>174</td>
      <td>BENING</td>
    </tr>
    <tr>
      <th>6</th>
      <td>60</td>
      <td>BERRY</td>
    </tr>
    <tr>
      <th>7</th>
      <td>91</td>
      <td>BERRY</td>
    </tr>
    <tr>
      <th>8</th>
      <td>185</td>
      <td>BOLGER</td>
    </tr>
    <tr>
      <th>9</th>
      <td>159</td>
      <td>BRODY</td>
    </tr>
    <tr>
      <th>10</th>
      <td>40</td>
      <td>CAGE</td>
    </tr>
    <tr>
      <th>11</th>
      <td>176</td>
      <td>CHASE</td>
    </tr>
    <tr>
      <th>12</th>
      <td>129</td>
      <td>CRAWFORD</td>
    </tr>
    <tr>
      <th>13</th>
      <td>104</td>
      <td>CRONYN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>101</td>
      <td>DAVIS</td>
    </tr>
    <tr>
      <th>15</th>
      <td>110</td>
      <td>DAVIS</td>
    </tr>
    <tr>
      <th>16</th>
      <td>143</td>
      <td>DEAN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>148</td>
      <td>DEE</td>
    </tr>
    <tr>
      <th>18</th>
      <td>107</td>
      <td>DEGENERES</td>
    </tr>
    <tr>
      <th>19</th>
      <td>166</td>
      <td>DEGENERES</td>
    </tr>
    <tr>
      <th>20</th>
      <td>123</td>
      <td>DENCH</td>
    </tr>
    <tr>
      <th>21</th>
      <td>160</td>
      <td>DEPP</td>
    </tr>
    <tr>
      <th>22</th>
      <td>188</td>
      <td>DUKAKIS</td>
    </tr>
    <tr>
      <th>23</th>
      <td>199</td>
      <td>FAWCETT</td>
    </tr>
    <tr>
      <th>24</th>
      <td>165</td>
      <td>GARLAND</td>
    </tr>
    <tr>
      <th>25</th>
      <td>184</td>
      <td>GARLAND</td>
    </tr>
    <tr>
      <th>26</th>
      <td>191</td>
      <td>GOODING</td>
    </tr>
    <tr>
      <th>27</th>
      <td>90</td>
      <td>GUINESS</td>
    </tr>
    <tr>
      <th>28</th>
      <td>179</td>
      <td>GUINESS</td>
    </tr>
    <tr>
      <th>29</th>
      <td>175</td>
      <td>HACKMAN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>49</th>
      <td>178</td>
      <td>MONROE</td>
    </tr>
    <tr>
      <th>50</th>
      <td>99</td>
      <td>MOSTEL</td>
    </tr>
    <tr>
      <th>51</th>
      <td>62</td>
      <td>NEESON</td>
    </tr>
    <tr>
      <th>52</th>
      <td>122</td>
      <td>NOLTE</td>
    </tr>
    <tr>
      <th>53</th>
      <td>125</td>
      <td>NOLTE</td>
    </tr>
    <tr>
      <th>54</th>
      <td>150</td>
      <td>NOLTE</td>
    </tr>
    <tr>
      <th>55</th>
      <td>34</td>
      <td>OLIVIER</td>
    </tr>
    <tr>
      <th>56</th>
      <td>69</td>
      <td>PALTROW</td>
    </tr>
    <tr>
      <th>57</th>
      <td>33</td>
      <td>PECK</td>
    </tr>
    <tr>
      <th>58</th>
      <td>87</td>
      <td>PECK</td>
    </tr>
    <tr>
      <th>59</th>
      <td>133</td>
      <td>PENN</td>
    </tr>
    <tr>
      <th>60</th>
      <td>195</td>
      <td>SILVERSTONE</td>
    </tr>
    <tr>
      <th>61</th>
      <td>116</td>
      <td>STREEP</td>
    </tr>
    <tr>
      <th>62</th>
      <td>155</td>
      <td>TANDY</td>
    </tr>
    <tr>
      <th>63</th>
      <td>149</td>
      <td>TEMPLE</td>
    </tr>
    <tr>
      <th>64</th>
      <td>193</td>
      <td>TEMPLE</td>
    </tr>
    <tr>
      <th>65</th>
      <td>200</td>
      <td>TEMPLE</td>
    </tr>
    <tr>
      <th>66</th>
      <td>94</td>
      <td>TORN</td>
    </tr>
    <tr>
      <th>67</th>
      <td>102</td>
      <td>TORN</td>
    </tr>
    <tr>
      <th>68</th>
      <td>117</td>
      <td>TRACY</td>
    </tr>
    <tr>
      <th>69</th>
      <td>95</td>
      <td>WAHLBERG</td>
    </tr>
    <tr>
      <th>70</th>
      <td>197</td>
      <td>WEST</td>
    </tr>
    <tr>
      <th>71</th>
      <td>137</td>
      <td>WILLIAMS</td>
    </tr>
    <tr>
      <th>72</th>
      <td>172</td>
      <td>WILLIAMS</td>
    </tr>
    <tr>
      <th>73</th>
      <td>96</td>
      <td>WILLIS</td>
    </tr>
    <tr>
      <th>74</th>
      <td>164</td>
      <td>WILLIS</td>
    </tr>
    <tr>
      <th>75</th>
      <td>147</td>
      <td>WINSLET</td>
    </tr>
    <tr>
      <th>76</th>
      <td>156</td>
      <td>WOOD</td>
    </tr>
    <tr>
      <th>77</th>
      <td>111</td>
      <td>ZELLWEGER</td>
    </tr>
    <tr>
      <th>78</th>
      <td>186</td>
      <td>ZELLWEGER</td>
    </tr>
  </tbody>
</table>
<p>79 rows × 2 columns</p>
</div>



### 6a. Use a JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:



```python
query = ("SELECT s.first_name, s.last_name, a.address\n"
        "FROM staff s\n"
        "JOIN address a on s.address_id = a.address_id;\n")
df = pd.read_sql(query, con=conn)
df.head()

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mike</td>
      <td>Hillyer</td>
      <td>23 Workhaven Lane</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Jon</td>
      <td>Stephens</td>
      <td>1411 Lillydale Drive</td>
    </tr>
  </tbody>
</table>
</div>



### 6b. Use a JOIN to display the total amount rung up by each staff member in January of 2007. Use tables staff and payment.


```python
query = ("WITH x AS (\n"
            "SELECT s.first_name, s.last_name, s.staff_id, p.amount, p.payment_date\n"
            "FROM staff s\n"
            "JOIN payment p ON s.staff_id = p.staff_id\n"
            "WHERE EXTRACT(YEAR FROM p.payment_date) = 2007 AND EXTRACT(MONTH FROM p.payment_date) = 1\n"
        ")\n"
        "SELECT x.first_name, x.last_name, SUM(x.amount) as TotalPayment\n"
        "FROM x\n"
        "GROUP BY x.staff_id, x.first_name, x.last_name;\n")
df = pd.read_sql(query, con=conn)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>totalpayment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mike</td>
      <td>Hillyer</td>
      <td>2621.83</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Jon</td>
      <td>Stephens</td>
      <td>2202.60</td>
    </tr>
  </tbody>
</table>
</div>



### 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.


```python
query = ("SELECT f.film_id, f.title, COUNT(fa.actor_id)\n"
        "FROM film f\n"
        "JOIN film_actor fa ON f.film_id = fa.film_id\n"
        "GROUP BY f.film_id;\n")
df = pd.read_sql(query, con=conn)
df.head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>251</td>
      <td>DRAGONFLY STRANGERS</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>106</td>
      <td>BULWORTH COMMANDMENTS</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>285</td>
      <td>ENGLISH BULWORTH</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>120</td>
      <td>CARIBBEAN LIBERTY</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>681</td>
      <td>PIRATES ROXANNE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>866</td>
      <td>SUNSET RACER</td>
      <td>3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>887</td>
      <td>THIEF PELICAN</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>264</td>
      <td>DWARFS ALTER</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>802</td>
      <td>SKY MIRACLE</td>
      <td>12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>664</td>
      <td>PATRIOT ROMAN</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



### 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
There are 6 copies.


```python
query = ("SELECT COUNT(*)\n"
        "FROM inventory i\n"
        "WHERE film_id = (SELECT f.film_id\n"
                        "FROM film f\n"
                        "WHERE f.title ilike 'Hunchback Impossible')\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



### 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:


```python
query = ("SELECT c.last_name, c.first_name, SUM(p.amount) as total_payment\n"
        "FROM customer c\n"
        "JOIN payment p on c.customer_id = p.customer_id\n"
        "GROUP BY c.customer_id, c.last_name, c.first_name\n"
        "ORDER BY c.last_name;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>first_name</th>
      <th>total_payment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ABNEY</td>
      <td>RAFAEL</td>
      <td>97.79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ADAM</td>
      <td>NATHANIEL</td>
      <td>133.72</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ADAMS</td>
      <td>KATHLEEN</td>
      <td>92.73</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ALEXANDER</td>
      <td>DIANA</td>
      <td>105.73</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ALLARD</td>
      <td>GORDON</td>
      <td>160.68</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ALLEN</td>
      <td>SHIRLEY</td>
      <td>126.69</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ALVAREZ</td>
      <td>CHARLENE</td>
      <td>114.73</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ANDERSON</td>
      <td>LISA</td>
      <td>106.76</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ANDREW</td>
      <td>JOSE</td>
      <td>96.75</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ANDREWS</td>
      <td>IDA</td>
      <td>76.77</td>
    </tr>
    <tr>
      <th>10</th>
      <td>AQUINO</td>
      <td>OSCAR</td>
      <td>99.80</td>
    </tr>
    <tr>
      <th>11</th>
      <td>ARCE</td>
      <td>HARRY</td>
      <td>157.65</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ARCHULETA</td>
      <td>JORDAN</td>
      <td>132.70</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ARMSTRONG</td>
      <td>MELANIE</td>
      <td>92.75</td>
    </tr>
    <tr>
      <th>14</th>
      <td>ARNOLD</td>
      <td>BEATRICE</td>
      <td>119.74</td>
    </tr>
    <tr>
      <th>15</th>
      <td>ARSENAULT</td>
      <td>KENT</td>
      <td>134.73</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ARTIS</td>
      <td>CARL</td>
      <td>106.77</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ASHCRAFT</td>
      <td>DARRYL</td>
      <td>76.77</td>
    </tr>
    <tr>
      <th>18</th>
      <td>ASHER</td>
      <td>TYRONE</td>
      <td>112.76</td>
    </tr>
    <tr>
      <th>19</th>
      <td>AUSTIN</td>
      <td>ALMA</td>
      <td>151.65</td>
    </tr>
    <tr>
      <th>20</th>
      <td>BAILEY</td>
      <td>MILDRED</td>
      <td>98.75</td>
    </tr>
    <tr>
      <th>21</th>
      <td>BAKER</td>
      <td>PAMELA</td>
      <td>95.77</td>
    </tr>
    <tr>
      <th>22</th>
      <td>BALES</td>
      <td>MARTIN</td>
      <td>103.73</td>
    </tr>
    <tr>
      <th>23</th>
      <td>BANDA</td>
      <td>EVERETT</td>
      <td>110.72</td>
    </tr>
    <tr>
      <th>24</th>
      <td>BANKS</td>
      <td>JESSIE</td>
      <td>91.74</td>
    </tr>
    <tr>
      <th>25</th>
      <td>BARBEE</td>
      <td>CLAYTON</td>
      <td>96.74</td>
    </tr>
    <tr>
      <th>26</th>
      <td>BARCLAY</td>
      <td>ANGEL</td>
      <td>115.68</td>
    </tr>
    <tr>
      <th>27</th>
      <td>BARFIELD</td>
      <td>NICHOLAS</td>
      <td>145.68</td>
    </tr>
    <tr>
      <th>28</th>
      <td>BARKLEY</td>
      <td>VICTOR</td>
      <td>91.76</td>
    </tr>
    <tr>
      <th>29</th>
      <td>BARNES</td>
      <td>RACHEL</td>
      <td>84.78</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>569</th>
      <td>WATSON</td>
      <td>THERESA</td>
      <td>99.70</td>
    </tr>
    <tr>
      <th>570</th>
      <td>WATTS</td>
      <td>SHELLY</td>
      <td>113.74</td>
    </tr>
    <tr>
      <th>571</th>
      <td>WAUGH</td>
      <td>JAMIE</td>
      <td>118.75</td>
    </tr>
    <tr>
      <th>572</th>
      <td>WAY</td>
      <td>MIKE</td>
      <td>166.65</td>
    </tr>
    <tr>
      <th>573</th>
      <td>WEAVER</td>
      <td>YOLANDA</td>
      <td>110.73</td>
    </tr>
    <tr>
      <th>574</th>
      <td>WEBB</td>
      <td>ETHEL</td>
      <td>135.68</td>
    </tr>
    <tr>
      <th>575</th>
      <td>WEINER</td>
      <td>RONALD</td>
      <td>132.70</td>
    </tr>
    <tr>
      <th>576</th>
      <td>WELCH</td>
      <td>MARLENE</td>
      <td>117.74</td>
    </tr>
    <tr>
      <th>577</th>
      <td>WELLS</td>
      <td>SHEILA</td>
      <td>73.82</td>
    </tr>
    <tr>
      <th>578</th>
      <td>WEST</td>
      <td>EDNA</td>
      <td>107.74</td>
    </tr>
    <tr>
      <th>579</th>
      <td>WESTMORELAND</td>
      <td>MITCHELL</td>
      <td>134.68</td>
    </tr>
    <tr>
      <th>580</th>
      <td>WHEAT</td>
      <td>FRED</td>
      <td>88.75</td>
    </tr>
    <tr>
      <th>581</th>
      <td>WHEELER</td>
      <td>LUCY</td>
      <td>91.74</td>
    </tr>
    <tr>
      <th>582</th>
      <td>WHITE</td>
      <td>BETTY</td>
      <td>117.72</td>
    </tr>
    <tr>
      <th>583</th>
      <td>WHITING</td>
      <td>ROY</td>
      <td>143.71</td>
    </tr>
    <tr>
      <th>584</th>
      <td>WILES</td>
      <td>JON</td>
      <td>87.76</td>
    </tr>
    <tr>
      <th>585</th>
      <td>WILLIAMS</td>
      <td>LINDA</td>
      <td>135.74</td>
    </tr>
    <tr>
      <th>586</th>
      <td>WILLIAMSON</td>
      <td>GINA</td>
      <td>111.72</td>
    </tr>
    <tr>
      <th>587</th>
      <td>WILLIS</td>
      <td>BERNICE</td>
      <td>145.67</td>
    </tr>
    <tr>
      <th>588</th>
      <td>WILSON</td>
      <td>SUSAN</td>
      <td>92.76</td>
    </tr>
    <tr>
      <th>589</th>
      <td>WINDHAM</td>
      <td>DARREN</td>
      <td>108.76</td>
    </tr>
    <tr>
      <th>590</th>
      <td>WOFFORD</td>
      <td>VIRGIL</td>
      <td>107.73</td>
    </tr>
    <tr>
      <th>591</th>
      <td>WOOD</td>
      <td>LORI</td>
      <td>141.69</td>
    </tr>
    <tr>
      <th>592</th>
      <td>WOODS</td>
      <td>FLORENCE</td>
      <td>126.70</td>
    </tr>
    <tr>
      <th>593</th>
      <td>WREN</td>
      <td>TYLER</td>
      <td>88.79</td>
    </tr>
    <tr>
      <th>594</th>
      <td>WRIGHT</td>
      <td>BRENDA</td>
      <td>104.74</td>
    </tr>
    <tr>
      <th>595</th>
      <td>WYMAN</td>
      <td>BRIAN</td>
      <td>52.88</td>
    </tr>
    <tr>
      <th>596</th>
      <td>YANEZ</td>
      <td>LUIS</td>
      <td>79.80</td>
    </tr>
    <tr>
      <th>597</th>
      <td>YEE</td>
      <td>MARVIN</td>
      <td>75.79</td>
    </tr>
    <tr>
      <th>598</th>
      <td>YOUNG</td>
      <td>CYNTHIA</td>
      <td>111.68</td>
    </tr>
  </tbody>
</table>
<p>599 rows × 3 columns</p>
</div>



### 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. display the titles of movies starting with the letters K and Q whose language is English.



```python
query = ("SELECT f.title\n"
        "FROM film f\n"
        "JOIN language l ON f.language_id = l.language_id AND name = 'English'\n"
        "WHERE f.title ILIKE 'k%' OR f.title ILIKE 'q%';\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KANE EXORCIST</td>
    </tr>
    <tr>
      <th>1</th>
      <td>KARATE MOON</td>
    </tr>
    <tr>
      <th>2</th>
      <td>KENTUCKIAN GIANT</td>
    </tr>
    <tr>
      <th>3</th>
      <td>KICK SAVANNAH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>KILL BROTHERHOOD</td>
    </tr>
    <tr>
      <th>5</th>
      <td>KILLER INNOCENT</td>
    </tr>
    <tr>
      <th>6</th>
      <td>KING EVOLUTION</td>
    </tr>
    <tr>
      <th>7</th>
      <td>KISS GLORY</td>
    </tr>
    <tr>
      <th>8</th>
      <td>KISSING DOLLS</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KNOCK WARLOCK</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KRAMER CHOCOLATE</td>
    </tr>
    <tr>
      <th>11</th>
      <td>KWAI HOMEWARD</td>
    </tr>
    <tr>
      <th>12</th>
      <td>QUEEN LUKE</td>
    </tr>
    <tr>
      <th>13</th>
      <td>QUEST MUSSOLINI</td>
    </tr>
    <tr>
      <th>14</th>
      <td>QUILLS BULL</td>
    </tr>
  </tbody>
</table>
</div>



### 7b. Use subqueries to display all actors who appear in the film Alone Trip.



```python
query = ("SELECT f.title, a.first_name, a.last_name\n"
        "FROM film_actor fa\n"
        "JOIN actor a ON fa.actor_id = a.actor_id\n"
        "JOIN film f ON fa.film_id = f.film_id\n"
        "WHERE title ILIKE \'ALone Trip\';\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ALONE TRIP</td>
      <td>ED</td>
      <td>CHASE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALONE TRIP</td>
      <td>KARL</td>
      <td>BERRY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ALONE TRIP</td>
      <td>UMA</td>
      <td>WOOD</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ALONE TRIP</td>
      <td>WOODY</td>
      <td>JOLIE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ALONE TRIP</td>
      <td>SPENCER</td>
      <td>DEPP</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ALONE TRIP</td>
      <td>CHRIS</td>
      <td>DEPP</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ALONE TRIP</td>
      <td>LAURENCE</td>
      <td>BULLOCK</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ALONE TRIP</td>
      <td>RENEE</td>
      <td>BALL</td>
    </tr>
  </tbody>
</table>
</div>



### 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.



```python
query = ("SELECT c.first_name, c.last_name, ctry.country\n"
        "FROM customer c\n"
        "JOIN address a ON c.address_id = a.address_id\n"
        "JOIN city city ON a.city_id = city.city_id\n"
        "JOIN country ctry ON city.country_id = ctry.country_id\n"
        "WHERE ctry.country ILIKE \'Canada\';\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>DERRICK</td>
      <td>BOURQUE</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DARRELL</td>
      <td>POWER</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LORETTA</td>
      <td>CARPENTER</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CURTIS</td>
      <td>IRBY</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>4</th>
      <td>TROY</td>
      <td>QUIGLEY</td>
      <td>Canada</td>
    </tr>
  </tbody>
</table>
</div>



### 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as a family film.  Now we mentioned family film, but there is no family film category. There’s a category that resembles that. In the real world nothing will be exact.



```python
query = ("SELECT f.title\n"
        "FROM film f\n"
        "JOIN film_category fc on f.film_id = fc.film_id\n"
        "JOIN category c on fc.category_id = c.category_id AND name = 'Family';\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AFRICAN EGG</td>
    </tr>
    <tr>
      <th>1</th>
      <td>APACHE DIVINE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ATLANTIS CAUSE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BAKED CLEOPATRA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BANG KWAI</td>
    </tr>
    <tr>
      <th>5</th>
      <td>BEDAZZLED MARRIED</td>
    </tr>
    <tr>
      <th>6</th>
      <td>BILKO ANONYMOUS</td>
    </tr>
    <tr>
      <th>7</th>
      <td>BLANKET BEVERLY</td>
    </tr>
    <tr>
      <th>8</th>
      <td>BLOOD ARGONAUTS</td>
    </tr>
    <tr>
      <th>9</th>
      <td>BLUES INSTINCT</td>
    </tr>
    <tr>
      <th>10</th>
      <td>BRAVEHEART HUMAN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CHASING FIGHT</td>
    </tr>
    <tr>
      <th>12</th>
      <td>CHISUM BEHAVIOR</td>
    </tr>
    <tr>
      <th>13</th>
      <td>CHOCOLAT HARRY</td>
    </tr>
    <tr>
      <th>14</th>
      <td>CONFUSED CANDLES</td>
    </tr>
    <tr>
      <th>15</th>
      <td>CONVERSATION DOWNHILL</td>
    </tr>
    <tr>
      <th>16</th>
      <td>DATE SPEED</td>
    </tr>
    <tr>
      <th>17</th>
      <td>DINOSAUR SECRETARY</td>
    </tr>
    <tr>
      <th>18</th>
      <td>DUMBO LUST</td>
    </tr>
    <tr>
      <th>19</th>
      <td>EARRING INSTINCT</td>
    </tr>
    <tr>
      <th>20</th>
      <td>EFFECT GLADIATOR</td>
    </tr>
    <tr>
      <th>21</th>
      <td>FEUD FROGMEN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>FINDING ANACONDA</td>
    </tr>
    <tr>
      <th>23</th>
      <td>GABLES METROPOLIS</td>
    </tr>
    <tr>
      <th>24</th>
      <td>GANDHI KWAI</td>
    </tr>
    <tr>
      <th>25</th>
      <td>GLADIATOR WESTWARD</td>
    </tr>
    <tr>
      <th>26</th>
      <td>GREASE YOUTH</td>
    </tr>
    <tr>
      <th>27</th>
      <td>HALF OUTFIELD</td>
    </tr>
    <tr>
      <th>28</th>
      <td>HOCUS FRIDA</td>
    </tr>
    <tr>
      <th>29</th>
      <td>HOMICIDE PEACH</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>39</th>
      <td>MAGUIRE APACHE</td>
    </tr>
    <tr>
      <th>40</th>
      <td>MANCHURIAN CURTAIN</td>
    </tr>
    <tr>
      <th>41</th>
      <td>MOVIE SHAKESPEARE</td>
    </tr>
    <tr>
      <th>42</th>
      <td>MUSIC BOONDOCK</td>
    </tr>
    <tr>
      <th>43</th>
      <td>NATURAL STOCK</td>
    </tr>
    <tr>
      <th>44</th>
      <td>NETWORK PEAK</td>
    </tr>
    <tr>
      <th>45</th>
      <td>ODDS BOOGIE</td>
    </tr>
    <tr>
      <th>46</th>
      <td>OPPOSITE NECKLACE</td>
    </tr>
    <tr>
      <th>47</th>
      <td>PILOT HOOSIERS</td>
    </tr>
    <tr>
      <th>48</th>
      <td>PITTSBURGH HUNCHBACK</td>
    </tr>
    <tr>
      <th>49</th>
      <td>PRESIDENT BANG</td>
    </tr>
    <tr>
      <th>50</th>
      <td>PRIX UNDEFEATED</td>
    </tr>
    <tr>
      <th>51</th>
      <td>RAGE GAMES</td>
    </tr>
    <tr>
      <th>52</th>
      <td>RANGE MOONWALKER</td>
    </tr>
    <tr>
      <th>53</th>
      <td>REMEMBER DIARY</td>
    </tr>
    <tr>
      <th>54</th>
      <td>RESURRECTION SILVERADO</td>
    </tr>
    <tr>
      <th>55</th>
      <td>ROBBERY BRIGHT</td>
    </tr>
    <tr>
      <th>56</th>
      <td>RUSH GOODFELLAS</td>
    </tr>
    <tr>
      <th>57</th>
      <td>SECRETS PARADISE</td>
    </tr>
    <tr>
      <th>58</th>
      <td>SENSIBILITY REAR</td>
    </tr>
    <tr>
      <th>59</th>
      <td>SIEGE MADRE</td>
    </tr>
    <tr>
      <th>60</th>
      <td>SLUMS DUCK</td>
    </tr>
    <tr>
      <th>61</th>
      <td>SOUP WISDOM</td>
    </tr>
    <tr>
      <th>62</th>
      <td>SPARTACUS CHEAPER</td>
    </tr>
    <tr>
      <th>63</th>
      <td>SPINAL ROCKY</td>
    </tr>
    <tr>
      <th>64</th>
      <td>SPLASH GUMP</td>
    </tr>
    <tr>
      <th>65</th>
      <td>SUNSET RACER</td>
    </tr>
    <tr>
      <th>66</th>
      <td>SUPER WYOMING</td>
    </tr>
    <tr>
      <th>67</th>
      <td>VIRTUAL SPOILERS</td>
    </tr>
    <tr>
      <th>68</th>
      <td>WILLOW TRACY</td>
    </tr>
  </tbody>
</table>
<p>69 rows × 1 columns</p>
</div>



### 7e. Display the most frequently rented movies in descending order.



```python
query = ("SELECT f.title, COUNT(*) as rental_cnt\n"
        "FROM rental r\n"
        "JOIN inventory i ON r.inventory_id = i.inventory_id\n"
        "JOIN film f ON i.film_id = f.film_id\n"
        "GROUP BY f.film_id, f.title\n"
        "ORDER BY rental_cnt DESC;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>rental_cnt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BUCKET BROTHERHOOD</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ROCKETEER MOTHER</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>JUGGLER HARDLY</td>
      <td>32</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SCALAWAG DUCK</td>
      <td>32</td>
    </tr>
    <tr>
      <th>4</th>
      <td>FORWARD TEMPLE</td>
      <td>32</td>
    </tr>
    <tr>
      <th>5</th>
      <td>GRIT CLOCKWORK</td>
      <td>32</td>
    </tr>
    <tr>
      <th>6</th>
      <td>RIDGEMONT SUBMARINE</td>
      <td>32</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ROBBERS JOON</td>
      <td>31</td>
    </tr>
    <tr>
      <th>8</th>
      <td>TIMBERLAND SKY</td>
      <td>31</td>
    </tr>
    <tr>
      <th>9</th>
      <td>WIFE TURN</td>
      <td>31</td>
    </tr>
    <tr>
      <th>10</th>
      <td>APACHE DIVINE</td>
      <td>31</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NETWORK PEAK</td>
      <td>31</td>
    </tr>
    <tr>
      <th>12</th>
      <td>RUSH GOODFELLAS</td>
      <td>31</td>
    </tr>
    <tr>
      <th>13</th>
      <td>HOBBIT ALIEN</td>
      <td>31</td>
    </tr>
    <tr>
      <th>14</th>
      <td>GOODFELLAS SALUTE</td>
      <td>31</td>
    </tr>
    <tr>
      <th>15</th>
      <td>ZORRO ARK</td>
      <td>31</td>
    </tr>
    <tr>
      <th>16</th>
      <td>FROST HEAD</td>
      <td>30</td>
    </tr>
    <tr>
      <th>17</th>
      <td>IDOLS SNATCHERS</td>
      <td>30</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PULP BEVERLY</td>
      <td>30</td>
    </tr>
    <tr>
      <th>19</th>
      <td>SUSPECTS QUILLS</td>
      <td>30</td>
    </tr>
    <tr>
      <th>20</th>
      <td>RUGRATS SHAKESPEARE</td>
      <td>30</td>
    </tr>
    <tr>
      <th>21</th>
      <td>ENGLISH BULWORTH</td>
      <td>30</td>
    </tr>
    <tr>
      <th>22</th>
      <td>SHOCK CABIN</td>
      <td>30</td>
    </tr>
    <tr>
      <th>23</th>
      <td>DOGMA FAMILY</td>
      <td>30</td>
    </tr>
    <tr>
      <th>24</th>
      <td>BUTTERFLY CHOCOLAT</td>
      <td>30</td>
    </tr>
    <tr>
      <th>25</th>
      <td>CAT CONEHEADS</td>
      <td>30</td>
    </tr>
    <tr>
      <th>26</th>
      <td>GRAFFITI LOVE</td>
      <td>30</td>
    </tr>
    <tr>
      <th>27</th>
      <td>WITCHES PANIC</td>
      <td>30</td>
    </tr>
    <tr>
      <th>28</th>
      <td>HARRY IDAHO</td>
      <td>30</td>
    </tr>
    <tr>
      <th>29</th>
      <td>MASSACRE USUAL</td>
      <td>30</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>928</th>
      <td>ITALIAN AFRICAN</td>
      <td>6</td>
    </tr>
    <tr>
      <th>929</th>
      <td>RUSHMORE MERMAID</td>
      <td>6</td>
    </tr>
    <tr>
      <th>930</th>
      <td>SCHOOL JACKET</td>
      <td>6</td>
    </tr>
    <tr>
      <th>931</th>
      <td>BED HIGHBALL</td>
      <td>6</td>
    </tr>
    <tr>
      <th>932</th>
      <td>DESPERATE TRAINSPOTTING</td>
      <td>6</td>
    </tr>
    <tr>
      <th>933</th>
      <td>TERMINATOR CLUB</td>
      <td>6</td>
    </tr>
    <tr>
      <th>934</th>
      <td>SLING LUKE</td>
      <td>6</td>
    </tr>
    <tr>
      <th>935</th>
      <td>OKLAHOMA JUMANJI</td>
      <td>6</td>
    </tr>
    <tr>
      <th>936</th>
      <td>SIMON NORTH</td>
      <td>6</td>
    </tr>
    <tr>
      <th>937</th>
      <td>GRACELAND DYNAMITE</td>
      <td>6</td>
    </tr>
    <tr>
      <th>938</th>
      <td>WARLOCK WEREWOLF</td>
      <td>6</td>
    </tr>
    <tr>
      <th>939</th>
      <td>APOCALYPSE FLAMINGOS</td>
      <td>6</td>
    </tr>
    <tr>
      <th>940</th>
      <td>DUCK RACER</td>
      <td>6</td>
    </tr>
    <tr>
      <th>941</th>
      <td>CONSPIRACY SPIRIT</td>
      <td>5</td>
    </tr>
    <tr>
      <th>942</th>
      <td>MANNEQUIN WORST</td>
      <td>5</td>
    </tr>
    <tr>
      <th>943</th>
      <td>HUNTER ALTER</td>
      <td>5</td>
    </tr>
    <tr>
      <th>944</th>
      <td>BRAVEHEART HUMAN</td>
      <td>5</td>
    </tr>
    <tr>
      <th>945</th>
      <td>FEVER EMPIRE</td>
      <td>5</td>
    </tr>
    <tr>
      <th>946</th>
      <td>TRAFFIC HOBBIT</td>
      <td>5</td>
    </tr>
    <tr>
      <th>947</th>
      <td>FULL FLATLINERS</td>
      <td>5</td>
    </tr>
    <tr>
      <th>948</th>
      <td>BUNCH MINDS</td>
      <td>5</td>
    </tr>
    <tr>
      <th>949</th>
      <td>INFORMER DOUBLE</td>
      <td>5</td>
    </tr>
    <tr>
      <th>950</th>
      <td>GLORY TRACY</td>
      <td>5</td>
    </tr>
    <tr>
      <th>951</th>
      <td>FREEDOM CLEOPATRA</td>
      <td>5</td>
    </tr>
    <tr>
      <th>952</th>
      <td>PRIVATE DROP</td>
      <td>5</td>
    </tr>
    <tr>
      <th>953</th>
      <td>SEVEN SWARM</td>
      <td>5</td>
    </tr>
    <tr>
      <th>954</th>
      <td>MUSSOLINI SPOILERS</td>
      <td>5</td>
    </tr>
    <tr>
      <th>955</th>
      <td>TRAIN BUNCH</td>
      <td>4</td>
    </tr>
    <tr>
      <th>956</th>
      <td>MIXED DOORS</td>
      <td>4</td>
    </tr>
    <tr>
      <th>957</th>
      <td>HARDLY ROBBERS</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
<p>958 rows × 2 columns</p>
</div>



### 7f. Write a query to display how much business, in dollars, each store brought in.



```python
query = ("SELECT s.store_id, CAST(SUM(p.amount) AS money) AS store_revenue\n"
        "FROM rental r\n"
        "JOIN payment p ON r.rental_id = p.rental_id\n"
        "JOIN staff s ON r.staff_id = s.staff_id\n"
        "GROUP BY s.store_id;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>store_id</th>
      <th>store_revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>$33,534.57</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>$33,881.94</td>
    </tr>
  </tbody>
</table>
</div>



### 7g. Write a query to display for each store its store ID, city, and country.


```python
query = ("SELECT s.store_id, c.city, ctry.country\n"
        "FROM store s\n"
        "JOIN address a ON a.address_id = s.address_id\n"
        "JOIN city c on a.city_id = c.city_id\n"
        "JOIN country ctry on c.country_id = ctry.country_id;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>store_id</th>
      <th>city</th>
      <th>country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Lethbridge</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Woodridge</td>
      <td>Australia</td>
    </tr>
  </tbody>
</table>
</div>



### 7h. List the top five genres in gross revenue in descending order. 


```python
query = ("SELECT c.name as genre, CAST(SUM(p.amount) AS money) as genre_revenue\n"
        "FROM payment p\n"
        "JOIN rental r ON p.rental_id = r.rental_id\n"
        "JOIN inventory i ON r.inventory_id = i.inventory_id\n"
        "JOIN film_category fc on i.film_id = i.film_id\n"
        "JOIN category c on fc.category_id = c.category_id\n"
        "GROUP BY c.category_id, c.name\n"
        "ORDER BY genre_revenue DESC\n"
        "LIMIT 5;\n")
df = pd.read_sql(query, con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>genre</th>
      <th>genre_revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sports</td>
      <td>$4,988,821.74</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Foreign</td>
      <td>$4,921,405.23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Family</td>
      <td>$4,651,739.19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Documentary</td>
      <td>$4,584,322.68</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Animation</td>
      <td>$4,449,489.66</td>
    </tr>
  </tbody>
</table>
</div>



### 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. 



```python
query1 = ("DROP VIEW IF EXISTS genre_revenue;")
query2 = ("CREATE VIEW genre_revenue AS\n"
    "SELECT c.name as genre, CAST(SUM(p.amount) AS money) as genre_revenue\n"
    "FROM payment p\n"
    "JOIN rental r ON p.rental_id = r.rental_id\n"
    "JOIN inventory i ON r.inventory_id = i.inventory_id\n"
    "JOIN film_category fc on i.film_id = i.film_id\n"
    "JOIN category c on fc.category_id = c.category_id\n"
    "GROUP BY c.category_id, c.name\n"
    "ORDER BY genre_revenue DESC\n"
    "LIMIT 5;\n")

cur = conn.cursor()
cur.execute(query1)
cur.execute(query2)

```

### 8b. How would you display the view that you created in 8a?


```python
df = pd.read_sql('SELECT * FROM genre_revenue', con=conn)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>genre</th>
      <th>genre_revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sports</td>
      <td>$4,988,821.74</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Foreign</td>
      <td>$4,921,405.23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Family</td>
      <td>$4,651,739.19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Documentary</td>
      <td>$4,584,322.68</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Animation</td>
      <td>$4,449,489.66</td>
    </tr>
  </tbody>
</table>
</div>



### 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.


```python
query1 = ("DROP VIEW IF EXISTS genre_revenue;")
cur = conn.cursor()
cur.execute(query1)
```
