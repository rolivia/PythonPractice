import tornado.ioloop
import tornado.web
import datetime, time
import json
import urllib2 
from collections import OrderedDict
from os.path import isfile, getmtime 

##################################
# USAGE: 
# For this week's weather forcast make GET request: http://localhost:3000/api/v1/weather
# For the forcast for a particular day of the week: http://localhost:3000/api/v1/weather/[day of week]
# Response will be JSON formatted string
# When pulling weather data from Dark Sky a file is created to cache the response
# When new requests are made within 5 minutes of a cache update, the cache is used.
# By reducing the number of requests to Dark Sky, latency is significantly reduced, because we are pulling
# from the local file system rather than making a web request.
# Also, Dark Sky charges $0.0001 per api request after the daily allowance (1000 requests) has been exceeded.
# So, reducing the number of requests also reduces the monetary cost of using the Dark Sky api.
##################################

# Arlington, VA coordinates
lat = 38.881622
lon = -77.090981

# My Dark Sky private key
privkey = "a876e56bcc29981b4ec8d722a40bcd09"

# Convert (datetime) weekday int to string: 0 is Monday, 6 is Sunday
def getWeekday(num):
	if num < 0 or num > 6:
		raise ValueError('not a valid weekday number')
	weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	return weekdays[num]

# Returns Ordered Dictionary that maps day of week to low and high for the day; starts with current day
def getWeeklyWeather():
	# RHS is true when it is too soon to update the cache; 
		# i.e. when it has been less than 5 minutes since it was updated
	now = time.mktime(datetime.datetime.now().timetuple())
	if isfile("weather") and (int((now - getmtime("weather")) / 60) <= 5):
		print("Loading weather data from cache")
		# Load content from cache
		f = open("weather", "r")
		content = f.read()
	else: 
		# Pull weekly weather data for week from Dark Sky and parse from json
		print("Pulling weather data from Dark Sky and updating cache")
		urlPrefix = "https://api.darksky.net/forecast/"
		content = urllib2.urlopen(urlPrefix + privkey + "/" + str(lat) + "," + str(lon)).read()
		f = open("weather", "w")
		f.write(content)
		f.close()

	# Parse JSON content to python
	weather = json.loads(content)

	# Pull out weekly weather forcast
	dailyWeather = weather['daily']['data']
	week = []
	# For each day of the week starting with today, get the high and the low
	for i in range(0,7):
		# Get weather forcast for ith day; 0 is current day
		day = dailyWeather[i]
		# Get the name of the ith day of the week
		weekday = getWeekday(datetime.datetime.utcfromtimestamp(day["time"]).weekday())
		low = day["temperatureMin"]
		high = day["temperatureMax"]
		week.append((weekday, {"low": low, "high": high}))
	# Convert to Ordered Dictionary so that order of days is preserved and for convenience for Daily forcast
	return OrderedDict(week)

# Create Request Handlers

# Get weather for whole week including today
class WeeklyWeatherHandler(tornado.web.RequestHandler):
    def get(self):
    	# Get weekly weather forcast
		weather = getWeeklyWeather()
		# Convert to JSON and send response
		self.write(json.dumps(weather, sort_keys=False, indent=4) + "\n")

# Get weather for a single day of the week
class DailyWeatherHandler(tornado.web.RequestHandler):
	def get(self, day):
		# Pull specific day out of weekly forcast
		dailyWeather = getWeeklyWeather()[day]
		# Convert to JSON and send response
		self.write(json.dumps(dailyWeather, sort_keys=False, indent=4) + "\n")

def make_app():
    return tornado.web.Application([
    	(r"/api/v1/weather", WeeklyWeatherHandler),
    	(r"/api/v1/weather/(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", DailyWeatherHandler)
    ])

# Start web app on localhost port 3000
if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()

