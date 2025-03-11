from django.shortcuts import render
from django.http import Http404
from datetime import datetime
from requests import get
from requests import exceptions

def index(request):
    """ View function for returning the home/index page"""
    try:
        data = getWeatherData()
    except exceptions.ConnectionError:
        data = "Connection Error"

    return render(request, 'weather_app/index.html', context={"data": data})

def getWeatherData():
    """ Function for getting weather data"""

    url = 'https://api.open-meteo.com/v1/forecast' # API call URL
    lat = getLocation().get('lat') # Get latitude value
    lon = getLocation().get('lon') # get longitude value

    wtr_data = get(url=url, 
        params={
            # Make and API call with the given parameters
            "latitude": lat,
            "longitude": lon,
            "timezone": "auto",
            "forecast_hours": 12,
            "current": ["is_day", "temperature_2m", "cloud_cover"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "sunset", "sunrise"],
            "hourly": ["temperature_2m", "cloud_cover"]
        })

    wtr_data_dic = wtr_data.json() # Convert the Json response to a dictionary

    # Update the weather data of the current hour with real time weather data
    wtr_data_dic["hourly"]["temperature_2m"][0] = wtr_data_dic["current"]["temperature_2m"]
    wtr_data_dic["hourly"]["cloud_cover"][0] = wtr_data_dic["current"]["cloud_cover"]
    wtr_data_dic["hourly"]["time"][0] = getDateAndTime()["time"]
    wtr_data_dic = wtr_data_dic | getLocation() | getDateAndTime() # Add location and local date and time dictionaries
    return wtr_data_dic

def getLocation():
    """Functin for getting the requested location"""
    url = "http://ip-api.com/json/" # API call URL
    location = get(url=url, params={ "fields": "lat,lon,country,city" })
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