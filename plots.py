import json
import openai
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
from matplotlib.ticker import (MultipleLocator, MaxNLocator)

# Get openai API key
with open('GPT_API_KEY.json') as f:
	data = json.load(f)

openai.api_key = data["API_KEY"]

#Start a GPT instance
from gpt import GPT
from gpt import Example

gpt = GPT (engine ="davinci", temperature=0.5, max_tokens=200)

#Declare static varbiablees
missing_values = ["MM"]

#Grab Buoy Data from Northwestern Hawaii Buoy 1
df = pd.read_csv('https://www.ndbc.noaa.gov/data/5day2/51001_5day.txt', sep ='\s+', engine='python', parse_dates=True, skiprows=[1], na_values = missing_values)

#Convert strings representing numbers into float. Create a timestamp column for labeling
df = df.astype(float)
df["DATE"] = df["#YY"].astype(str)+'/'+df["MM"].astype(str)+'/'+df["DD"].astype(str)+'/'+df["hh"].astype(str)+'/'+df["mm"].astype(str)

#Add samples to the gpt instance
gpt.add_example(Example('Plot a line plot of pressure',"ax.plot(df['DATE'],df['PRES'])#ax.set(ylabel='pressure',xlabel='date')"))
gpt.add_example(Example('Plot a line plot of wind speed',"ax.plot(df['DATE'],df['WSPD'])#ax.set(ylabel='wind speed',xlabel='date')"))
gpt.add_example(Example('Show me the histogram of wind speed with labels', "df['WSPD'].hist()#ax.set(ylabel='wind speed')"))
gpt.add_example(Example('Show me a scatter plot between air temperature and pressure', "plt.scatter(df['ATMP']), df['PRES'])#ax.set(xlabel='air temperature',ylabel='pressure')"))
gpt.add_example(Example('Plot scatter plot between wind speed and water temperature', "plt.scatter(df['WSPD']), df['WTMP'])#ax.set(xlabel='wind speed',ylabel='water temperature')"))


prompt = "show me a plot of air temperature"
response = gpt.get_top_reply(prompt)
modified_response = response.split("output: ")[-1].strip('\n').split('#')
print(modified_response)

#Create static parts of the figure
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(MaxNLocator())
#Execute the commands from the modified response
for command in modified_response:
	exec(command)
plt.show()

