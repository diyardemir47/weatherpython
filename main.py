import datetime as dt
import pytz
import requests
import matplotlib.pyplot as plt
import pandas as pd

# set the Historical API POST endpoint as the target URL
postHistoricalURL = "https://api.tomorrow.io/v4/timelines"

# get your API key from app.tomorrow.io/development/keys
apikey = "YOUR_API_KEY_HERE"

# pick the location, as a latlong pair
location = [42.63496561409271, -73.68988401705542]

# list the fields
fields = [
    "precipitationIntensity",
    "windSpeed",
    "windDirection",
    "windGust",
    "snowfallIntensity"
]

# choose the unit system, either metric or imperial
units = "imperial"

# set the timesteps, like "current", "1h" and "1d"
timesteps = ["1d"]

# configure the time frame within the historical boundaries
now = dt.datetime.now(pytz.UTC)
startTime = '2020-12-01T12:00:00.000Z'
endTime = '2020-12-20T12:00:00.000Z'

# specify the timezone, using standard IANA timezone format
timezone = "US/Eastern"

# request the historical timelines with all the body parameters as options
body = {
    "location": location,
    "fields": fields,
    "units": units,
    "timesteps": timesteps,
    "startTime": startTime,
    "endTime": endTime,
    "timezone": timezone
}

response = requests.post(f'{postHistoricalURL}?apikey={apikey}', json=body)
data = response.json()
timelines = data["data"]["timelines"][0]["intervals"]

# create a dataframe with the response values
df = pd.DataFrame(timelines)
df.rename(columns={'startTime': 'Date'}, inplace=True)
df.Date = pd.to_datetime(df['Date'], format='%Y-%m-%dT%H:%M:%SZ')

# visualize data
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['values.precipitationIntensity'], label='Precipitation Intensity')
plt.plot(df['Date'], df['values.windSpeed'], label='Wind Speed')
plt.plot(df['Date'], df['values.windDirection'], label='Wind Direction')
plt.plot(df['Date'], df['values.windGust'], label='Wind Gust')
plt.plot(df['Date'], df['values.snowfallIntensity'], label='Snowfall Intensity')

plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Weather Data Over Time')
plt.legend()
plt.grid(True)

plt.show()
print(data)

print('done')
