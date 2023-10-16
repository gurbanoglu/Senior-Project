from django.shortcuts import render
import requests
import datetime


"""
SearchWeather()

NAME

    SearchWeather - handles an HttpRequest to the 'search-weather/' address.

SYNOPSIS

    def SearchWeather(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    If there was a 'city' key inside the dictionary sent from the POST request
    this function received, the value of "request.POST['city']" will be grabbed.

    Otherwise, the default city is Athens, Greece.

    The current date of the city is found, and used to obtain the accurate
    weather forecast which will then be stored in a dictionary named "context".

    If the name of a country is stored inside "request.POST['city']", this
    function will still operate without any errors.

    If an invalid location is entered, the user is informed of this with an
    error page.

RETURNS

    Returns an HttpResponse object containing a Python dictionary that holds
    weather data for the location searched for, while at the same time rendering
    the 'SearchWeather.html' template located inside the "weather" application.

"""


def SearchWeather(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Athens'
        print("request.POST: ", request.POST)

    appid = 'dabd371890ebe424778b3aa4bf14ddbb'

    URL = 'http://api.openweathermap.org/data/2.5/weather'

    PARAMS = {
        'q': city, 'appid': appid, 'units': 'imperial'
    }

    responseStream = requests.get(url=URL, params=PARAMS)

    JSONResponse = responseStream.json()

    if JSONResponse['cod'] == '404':
        print("Error! An unknown location was entered into the weather application search bar.")
        return render(request, 'weather/UnknownLocation.html')

    description = JSONResponse['weather'][0]['description']

    icon = JSONResponse['weather'][0]['icon']
    temp = JSONResponse['main']['temp']

    day = datetime.date.today()
    oneDay = datetime.timedelta(1)

    day = day - oneDay

    context = {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
    }

    # Pass the variable "context" to the "SearchCityWeather.html"
    # file, so that it can be accessed inside that template.
    return render(request, 'weather/SearchWeather.html', context)
# def SearchWeather(request):

# 32
