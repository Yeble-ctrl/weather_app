from django.shortcuts import render
from django.http import HttpResponseServerError
from datetime import datetime
import requests

def index(request):
    """ View function for returning the home/index page"""
    data = getWeatherData()
    return render(request, 'weather_app/index.html', context={"data": data})

def getWeatherData():
    """ Function for getting weather data"""

    url = 'https://api.open-meteo.com/v1/forecast' # API call URL
    lat = getLocation().get('lat') # Get latitude value
    lon = getLocation().get('lon') # get longitude value

    try:
        wtr_data = requests.get(url=url, 
        params={
            # Make and API call with the given parameters
            "latitude": lat,
            "longitude": lon,
            "timezone": "auto",
            "current": ["is_day", "temperature_2m", "cloud_cover"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "sunset", "sunrise"]
        })

        wtr_data_dic = wtr_data.json() # Convert the Json response to a dictionary
        wtr_data_dic = wtr_data_dic | getLocation() | getDateAndTime() # Add location and local date and time dictionaries
        return wtr_data_dic
        
    except:
        raise HttpResponseServerError

def getLocation():
    """Functin for getting the requested location"""
    url = "http://ip-api.com/json/" # API call URL
    location = requests.get(url=url, params={ "fields": "lat,lon,country,city" })
    loc_dic = location.json()
    return loc_dic

def getDateAndTime():
    """ Function for getting the current time and date"""
    curr_date = datetime.today()
    date_dic = {
        "week_day": curr_date.strftime('%A'),
        "day": curr_date.strftime('%d'),
        "month": curr_date.strftime('%B'),
        "year": curr_date.strftime('%Y'),
        "time": curr_date.isoformat(timespec='minutes')
    }

    return date_dic