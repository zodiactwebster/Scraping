#!/usr/bin/env python
# coding: utf-8

# # Web Crawling Assignment



import pprint
import requests
import numpy as np
import pandas as pd
api_key = 'you need one'


# ## Locations defined here - note is a list of strings, not a list of lists


locations = ['Bengaluru, India',
'Glasgow, Scotland',
'Gumi, South Korea',
'Lagos, Nigeria',
'Nanaimo, Canada',
"Niskayuna, New York", # ,USA
'Nizhny Novgorod, Russia',
'Olongapo, Phillipines',
'Peshawar, Pakistan',
'Peterhead, Scotland',
 'Quito, Ecuador',
'Simmern, Germany',
'Tainan, Taiwan',
'Tbilisi, Georgia',
'Vinh Long, Vietnam',
"Xi'an, China"]



# ## Get the weather data into a data frame from the API calls. 
# Keep all of it in this version of code. Create a dictionary linked to the city name. Loop through locations. 

#set up an empty space for the information
dataplace = {} 
for loc in locations: # loop through locations  
    # build up request url with the location information and key and units as celsius
    URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    URL = URL + 'q='+ loc +'&appid=' + api_key +'&units=metric' # use indexing on list item to get only the text 
    response = requests.get( URL )
    if response.status_code == 200:      # Success
      data = response.json()  # now have results in big dictionary for one city
    else:                                # Failure
      print( 'Error:', response.status_code )
    dataplace[loc] = data # put the weather data, all of it, into the dataplace. 
#-------------------------------------------------------  #
# # initialize variables
# Need to start at "midnight" UTC and do full day from there. 
# OpenWeatherMap always returns dates and times in UTC (Coordinated Universal Time or Greenwich Mean Time.)
# 
# First set up all the variables you will need. 
# This will allow some edits so is not fixed by certain number of locations. 
# get size of locations - that is number of rows you need
ncities = len(locations)
# number of items in the 'list' part of the data is the number of temperatures
ndata = len(data['list']) # this is for whichever city was last
days = 4 # 4 days of weather
starttime = '00' # need to find 00:00
intervals = 8 # 8 intervals of 3 hours each in a day # could automate this later for other api products
minTemp = np.zeros([ncities,ndata],float) # set up some empty arrays for temperatures
maxTemp = np.zeros([ncities,ndata],float)
temperature = np.zeros([ncities,2*days+2]) # set up temperature array to be for each day plus overall averages
times = [] # create an empty list for the times 

# ## Extract temperature data and calculate averages per day and over 4 day range
# loop over cities and set a counter to access the rows/cities
rownum=0
for city in dataplace:
   for i in range(0,ndata): # loop over the number of temperatures
       minTemp[rownum][i]=dataplace[city]['list'][i]['main']['temp_min']
       maxTemp[rownum][i] = dataplace[city]['list'][i]['main']['temp_max']
       times.append(dataplace[city]['list'][i]['dt_txt'][11:13]) # all the cities have same times - so just need one list
# use time to figure out when to start
### to do... start here. 
   begin = times.index(starttime) 
   for day in range(days):
       start = begin+(day*intervals)  # initialize the start and end columns
       end = start+intervals #increment the end
       #print("day =", day,"start=",start, "end=", end, day*intervals+1)
       # get the minimum and maximum for the day - between start and end
       temperature[rownum][2*day] = '{:.2f}'.format(np.min(minTemp[rownum][start:end]))
       temperature[rownum][2*(day)+1] = '{:.2f}'.format(np.max(maxTemp[rownum][start:end]))
       # this format statement does not pad with zeros after. 
   # calculate the overall temperature average for the city, min and max for only those 4 days
   # but not overall mean - need the mean only of the 4 minima or maxima. 
   # put mean of minima in 2nd to last column
   temperature[rownum][-2] = '{:.2f}'.format(round(np.mean(temperature[rownum][:-2:2]),2)) # minima are every other one
   # put mean of maxima in the last column
   temperature[rownum][-1] = '{:.2f}'.format(round(np.mean(temperature[rownum][1:-2:2]),2))# maxima are every other one starting with 1 
   rownum+=1 # increment the rownumber for each city
# -------------------------------------------
#    convert floats to strings so can get zeros to fill
# -----------------------------
a_str=[] # create an empty list
for x in np.nditer(temperature):
    a_str = a_str + ["%.2f" % x]

# need # cities rows
# need  temperature 2 min max per day and overall avg per day (max/min)
# convert/reshape list to np array of strings!
new_str = np.array(a_str).reshape(ncities,(days+1)*2) 

# ## create a dataframe with headings and export
headings = ['Min 1','Max 1', 'Min 2','Max 2','Min 3','Max 3', 'Min 4','Max 4','Min Avg','Max Avg' ] 
df=pd.DataFrame(new_str)
#tmp = df.round(2) # this is a rounding function for pandas dataframe. rounds all columns. similar func avail numpy.
#df = tmp #cannot operate on a dataframe in place... 
df.columns=headings
df.insert(0,"City",locations)
# default is to write to current directory
df.to_csv('temp.csv', index=False) 
