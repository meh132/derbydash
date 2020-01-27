#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd;
import numpy as np;
import serial, time 
import json
import matplotlib


# In[ ]:


# connect to Track
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)
print(ser.name)


# In[2]:


# Read from CSV to load Races
races = pd.read_csv('Races.csv')
races = races.set_index('Race Number')


# Read list of racers and cars from CSV

racers = pd.read_csv('Racers.csv')
racers = racers.set_index('Number')
racers.head()


# In[ ]:


# create Race Output for First race
# for race, build details for lane
# get lane 1 car
race = {}
lane = 1


for carNum in races.loc[11]:
    name = racers.loc[carNum,'Name']
    #print(lane, carNum, name)
    details = {'car': str(carNum), 'name': name}
    trackName = 'lane' + str(lane)
    race[trackName] = details
    lane = lane +1

nextup = {'nextUp': race}
with open('src/nextup.json', 'w') as outfile:
    json.dump(nextup, outfile)


# In[ ]:


# Set Race
current_race = 5


# In[ ]:


# resultsdf = pd.DataFrame(columns=["Race","Lane","Car","Time","Scout","Den"])
#resultsdf = pd.DataFrame(columns=["Race","Lane","Car","Time"])

resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])
resultsdf.head()


# # Start of the Race process

# In[ ]:


# show curret race
current_contestants = races.loc[current_race]
print(races.loc[current_race])


# In[ ]:


# Reset Track if needed
#Reset Track
command = 'r'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)


# ## Run Race
# 

# In[ ]:


# set current race if needed
current_race = 10


# ### Call out # of lanes and race number
# 

# In[ ]:


print('In Race ' + str(current_race) + ' the following cars are racing: \n'+ str(races.loc[current_race]))


# In[ ]:


# Turn on all Lanes   om# is used to turn off track
command = 'om0'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
returnmessage = ser.readline()
print(returnmessage.decode())


# In[ ]:


# Turn off tracks that are not being used
# lanesToBlock = [1,4]
lanesToBlock = []

for x in (lanesToBlock):
    #lanenum = (x[4:5])
    #command = 'om' + lanenum +'\r\n'
    command = 'om' + str(x) +'\r\n'
    print(command)
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    returnmessage = ser.readline()
    print(returnmessage.decode())


# In[ ]:



# Get Race Results
# get race results
command = 'rg'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
results = ser.readline()
laneresults = results.decode().split()
print(laneresults)


# confirm Lane Results


# # Force finish race 

# In[ ]:


# force race end
command = 'ra'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
results = ser.readline()


# In[ ]:



# Get Race Results
# get race results
command = 'rp'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
results = ser.readline()
laneresults = results.decode().split()
print(laneresults)


# In[ ]:


#laneresults = ['1=1.1704', '2=5.4159b', '3=3.5462c', '4=3.7246d']
print('Confirm Results: \n' + str(laneresults))


# ## Calculate leaders and publish leaders based on average time

# In[ ]:


race = {}
for laneresult in laneresults:
    lane = laneresult[0]
    car = races.loc[int(current_race),'Lane '+lane]
    time = float(laneresult[2:8])
    name = racers.loc[car,'Name']
    den = racers.loc[car,'Den']
    category = racers.loc[car,'Category']
    place = laneresult[8:9]
    
    # Create results json
    details = {'race' : current_race , 'lane' : int(lane), 'car': str(car), 'name': name, 'time': time, 'place': place, 'den': den, 'category': category} 
    trackName = 'lane' + str(lane)
    race[trackName] = details
    
 
    # add den, category
    resultsdf = resultsdf.append(details, ignore_index=True)
    #print(details)
   
current_race = current_race +1
resultsdf.to_csv('resultsFile.csv')


# In[ ]:


## update or rewrite Json for current race.  
currentRace = {'currentRace': race}
with open('src/current.json', 'w') as outfile:
    json.dump(currentRace, outfile)


## update or rewrite Json for current race.  
avg = resultsdf.groupby(['car','name'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .reset_index()

avgtimes = avg.to_dict(orient='records')
avgTimes = {'averageTimes': avgtimes}
with open('src/avg.json', 'w') as outfile:
    json.dump(avgTimes, outfile)

top = resultsdf.groupby(['car','name'])        .agg({'time':'min'})        .reset_index()

toptimes = top.to_dict(orient='records')

## update or rewrite Json for current race.  
topTimes = {'topSpeeds': toptimes}
with open('src/top.json', 'w') as outfile:
    json.dump(topTimes, outfile)
    
# create Race Output for Upcoming race
# for race, build details for lane
# get lane 1 car
race = {}
lane = 1
for carNum in races.loc[current_race]:
    name = racers.loc[carNum,'Name']
    #print(lane, carNum, name)
    details = {'car': str(carNum), 'name': name}
    trackName = 'lane' + str(lane)
    race[trackName] = details
    lane = lane +1

nextup = {'nextUp': race}
with open('src/nextup.json', 'w') as outfile:
    json.dump(nextup, outfile)


# In[ ]:


## End of Race


# # Final Results

# In[ ]:


## Den Results
den_results = resultsdf.groupby(['den','car','name'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .sort_values(['den','time'], ascending=True)
       #.reset_index()
print(den_results)


# In[ ]:


## Den Results
den_results = resultsdf.groupby(['den','car','name'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .sort_values('time', ascending=True)
       #.reset_index()
print(den_results)


# In[ ]:


## Fastest Lane
lane_results = resultsdf.groupby(['lane'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .sort_values('time', ascending=True)
       #.reset_index()
print(lane_results)


# In[ ]:


# Get top cars after dropping slowest lap
standings = resultsdf.groupby('car')     .apply(lambda x: x.drop([x['time'].idxmax()]))    .rename_axis(['time','time'])    .groupby('car')    .agg({'car':'size', 'time':'mean'})     .rename(columns={'car':'Races Completed','time':'Average Time'})     .sort_values('Average Time', ascending=True)


#standings = standings.sort_values('Average Time', ascending=True)
print(standings.iloc[0:4])


# # Extra commands

# In[ ]:


# Turn on Set Place   indicatorto #
command = 'op2'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
returnmessage = ser.readline()
print(returnmessage.decode())


# In[4]:


backup = pd.read_csv('resultsFile.csv')
backup.head()


# In[5]:


## Den Results
den_results = backup.groupby(['den','car','name'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .sort_values(['den','time'], ascending=True)
       #.reset_index()
print(den_results)


# In[ ]:





# In[6]:


## Den Results
den_results = backup.groupby(['car','name'])        .agg({'car':'size', 'time':'mean'})        .rename(columns={'car':'Races Completed'})        .sort_values('time', ascending=True)
       #.reset_index()
print(den_results)


# In[8]:


den_results.columns


# In[15]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[19]:


den_results.hist(column='time',bins=50)


# In[ ]:


# Find Car by race and lane
car = racedf.loc[1,'lane1']
print (car)


# In[ ]:


results = ser.readline()


# In[ ]:


times = avg.loc[:,['car','name','Average Time']]
times = times.reset_index()
times.head()


# In[ ]:


# delete race result or duplicate race result


# In[ ]:


# write out rsults df and load from csv


# In[ ]:


def serialwrite(code):
    command = code +'\r\n'
    #newcommand = command.encode('ascii')
    #ser.write(newcommand)
    #results = ser.readline()
    #laneresults = results.decode().split()
    #print(laneresults)
    return results

serialwrite('rg')


# In[ ]:


currentrace['currentRace']['lane1']['time'] ='3.012'
lastRace = currentrace['currentRace']
type(lastRace)


# In[ ]:


# Reverse Lane order
command = 'ov1'+'\r\n'
newcommand = command.encode('ascii')
ser.write(newcommand)
results = ser.readline()
print(laneresults)


# confirm Lane Results


# In[ ]:


#races.loc[2,'Lane 2'] = 1
#races.head(15)

