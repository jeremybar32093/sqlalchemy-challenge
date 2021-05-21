# sqlalchemy-challenge

This repository reads in a dataset surrounding hawaii temperature and precipitation measurements and performs some exploratory data analysis using *jupyter notebook*. Additionally, a quick API was created using *flask*. The source data used is a *sqlite* database that can be found in the **data** folder. 

The jupyter notebooks included are as follows:

**1.) climate_analysis**
This notebook reads in the hawaii.sqlite database using *sqlalchemy* and performs the following:
  * Uses sqlalchemy to read in the last 12 months of precipitation data and produce a bar graph of the result
  * Finds the most active weather station based off of number of measurements, then creates a histogram for that station showing the distribution of temperature measurements

**2.) temp_analysis_1**
This notebook reads in a csv file called hawaii_measuremnts.csv also located in the **data** folder. This notebook performs the following:
  * Identifies average temperatures in June across all weather stations and all years included in the dataset
  * Identifies average temperatures in December across all weather stations and all years included in the dataset
  * Performs an unpaired t-test between the average temperatures in June and December to determine if the difference in means between the two is statistically significant

**3.) temp_analysis_2**
This notebook reas in the hawaii.sqlite database using *sqlalchemy* and performs the following:
  * Calculates the minimum, maximum, and average temperatures during a specified date range
  * Calculates the total rainfall per weather station at a specified date range
  * Calculates 'daily normals' for rainfall and plots in an area chart for a specified date range

In addition to the *jupyter notebooks*, a *flask* API has been created and is located in the **flask** folder. The **app.py** file within this folder creates a simple API with routes that do the following:
  * /api/v1.0/precipitation - returns dates and precipitation values
  * /api/v1.0/stations - returns list of all stations from the dataset
  * /api/v1.0/&lt;start&gt; and /api/v1.0/&lt;start&gt;/&lt;end&gt; - returns minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    * When given the start only, calculates TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    * When given the start and the end date, calculates the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
