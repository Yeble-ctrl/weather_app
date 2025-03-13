from django.shortcuts import render
from datetime import datetime, date
from requests import get
from requests import exceptions
from weather_app.vmo_description_data import VMO_DESCRIPTION_DATA

def index(request):
    """ View function for returning the home/index page"""
    try:
        data = getWeatherData()
        current_data = data["current"]
        daily_data = data["daily"]
        hourly_data = zip(
            data["hourly"]["time"], 
            data["hourly"]["temperature_2m"], 
            data["hourly"]["cloud_cover_low"]
        )
        date_time_data = getCurrDateAndTime()
        loc_data = getLocation()

        print(current_data)

        context = {"current": current_data, "daily": daily_data, 
        "hourly": hourly_data, "date_time": date_time_data, "location": loc_data}

    except exceptions.ConnectionError:
        data = "Connection Error"

    return render(request, 'weather_app/index.html', context=context)

def weekly_forecast(request):
    """View function to get weeky weather forecast"""
    try:
        data = getWeatherData()["daily"]

        # Change the date from isoformat
        for i in range(0, len(data["time"])):
            data["time"][i] = changeDateFormat(data["time"][i])

        weekly_data = zip(
            data["time"],
            data["temperature_2m_max"],
            data["temperature_2m_min"]
        )
        context = {"weekly_data": weekly_data}

    except exceptions.ConnectionError:
        data = "connection error"
    
    return render(request, 'weather_app/weekly_forecast.html', context=context)

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
            "current": ["is_day", "temperature_2m", "cloud_cover_low", "weather_code"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "sunset", "sunrise"],
            "hourly": ["temperature_2m", "cloud_cover_low"]
        })

    wtr_data_dic = wtr_data.json() # Convert the Json response to a dictionary
    wtr_data_dic["hourly"]["temperature_2m"][0] = wtr_data_dic["current"]["temperature_2m"] # Update the current hour temp with the current real time temp
    wtr_data_dic["hourly"]["cloud_cover_low"][0] = wtr_data_dic["current"]["cloud_cover_low"] # Update the curremt hour cloud cover %ge with the current real time cloud cover %ge
    wtr_data_dic["hourly"]["time"][0] = getCurrDateAndTime()["time"] # Update the current hour value with a more accurate value
    wtr_data_dic["current"].update({"weather_desc": VMO_DESCRIPTION_DATA[str(wtr_data_dic["current"]["weather_code"])]})
    return wtr_data_dic

def changeDateFormat(isoformat_date):
    """Method for changing the isodate format to a more readable one"""
    new_date = date.fromisoformat(isoformat_date)
    date_dic = {
        "week_day": new_date.strftime('%A'),
        "day": new_date.strftime('%d'),
        "month": new_date.strftime('%B'),
        "year": new_date.strftime('%Y'),
    }
    return date_dic

def getLocation():
    """Functin for getting the requested location"""
    url = "http://ip-api.com/json/" # API call URL
    location = get(url=url, params={ "fields": "lat,lon,country,city" })
    loc_dic = location.json()
    return loc_dic

def getCurrDateAndTime():
    """Function for getting the current time and date"""
    curr_date = datetime.today()
    date_dic = {
        "week_day": curr_date.strftime('%A'),
        "day": curr_date.strftime('%d'),
        "month": curr_date.strftime('%B'),
        "year": curr_date.strftime('%Y'),
        "time": curr_date.isoformat(timespec='minutes')
    }
    return date_dic