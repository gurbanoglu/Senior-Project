from django.shortcuts import render, redirect
from .models import MapDatabase, Video
from .forms import MapDataForm
import folium
import geocoder
import pandas as panda

# The view functions in this file handle the POST
# and GET requests for the "map_app" application.

"""
SearchMap()

NAME

    SearchMap - handles the HttpRequest to the 'search-map/' address.

SYNOPSIS

    def SearchMap(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will either accept a POST request or a GET request. Upon a
    POST request, the view will grab the data that was submitted along with
    the "MapDataForm". If it is valid, the view will save it, and redirect
    the user back to the 'search-map' address.
    
    In the case of receiving a GET request, it means that the user has simply
    requested the web page in contrast to the POST request where they have
    entered data that is submitted with a form. As a consequence of not submitting
    any data to the "MapDataForm", what will be displayed is the last "MapDataBase"
    object that was searched for.

    Lastly, this view provides each location searched for with a marker on the
    map. When hovering over the marker, there will be text stating "Click For 
    Description". After clicking on the marker, the name of the city in the 
    native language of the country is revealed to the user.

RETURNS

    If the user has entered an invalid location, the 'invalid_map_location.html'
    HTML template is returned.

    Otherwise, an HttpResponse object will direct the user to the 'search_map.html'
    template located inside the "map_app" application.

"""


def SearchMap(request):
    if request.method == 'POST':
        mapForm = MapDataForm(request.POST)

        # Having a nested if statement is necessary here because an object
        # of the "MapDataForm" class must be verified as valid before being
        # saved, and saving a "MapDataForm" object is only applicable if
        # this view function has received a POST request.
        if mapForm.is_valid():
            mapForm.save()
            # return redirect('/') will redirect the user back to
            # 127.0.0.1:8000/ which is the homepage of the application.
            # Instead the user must be redirected back to the page that
            # is loaded with the 'display-map' URL path name.
            return redirect('search-map')
    else:
        mapForm = MapDataForm()

    m_address = MapDatabase.objects.last()
    location = geocoder.osm(m_address)

    latitude = location.lat
    longitude = location.lng

    country = location.country
    city = location.city

    print("country: ", country)
    print("city: ", city)

    if latitude == None or longitude == None:
        m_address.delete()
        return render(request, 'map_app/invalid_map_location.html')

    # Here the map object is being created.
    # The following line of code will center the map and zoom in at
    # an appropriate distance.
    mapObject = folium.Map(location=[19, -12], zoom_start=2)

    # After searching for a city or country, this marker will appear on the map.

    if city == None:
        folium.Marker([latitude, longitude], tooltip='Click For Description',
                      popup=country).add_to(mapObject)
    else:
        folium.Marker([latitude, longitude], tooltip='Click For Description',
                      popup=city).add_to(mapObject)

    mapObject = mapObject._repr_html_()

    context = {
        'mapObject': mapObject,
        'mapForm': mapForm,
    }

    return render(request, 'map_app/search_map.html', context)
# def SearchMap(request):


"""
DisplayCities()

NAME

    DisplayCities - handles the HttpRequest to the 'display-cities/' address.

SYNOPSIS

    def DisplayCities(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will either accept a POST request or a GET request. Upon a
    POST request, the view will grab the data that was submitted along with
    the "MapDataForm". If it is valid, the view will save it, and redirect
    the user back to the 'display-cities' address.
    
    In the case of receiving a GET request, it means that the user has simply
    requested the web page in contrast to the POST request where they have
    entered data that is submitted with a form. As a consequence of not submitting
    any data to the "MapDataForm", what will be displayed is the last "MapDataBase"
    object that was searched for. Additionally, the cities with details for
    tourists are shown likewise.

    This view shows each location that was searched for, together with the cities 
    that contain tourist information. A marker is presented with each city.
    
    When hovering over a marker, there will be text stating "Click For 
    Description". After clicking on the marker, the name of the city in the 
    native language of the country is revealed to the user.

    However, if the city is one for a tourist to view, the user can also click
    on the name of the city and then will be taken to a web page with useful
    knowledge about the city. City names that act as a link will have a blue
    colour.

RETURNS

    If the user has entered an invalid location, the 'invalid_map_location.html'
    HTML template is returned.

    Otherwise, an HttpResponse object will direct the user to the 'display_cities.html'
    template located inside the "map_app" application.

"""


def DisplayCities(request):
    if request.method == 'POST':
        mapForm = MapDataForm(request.POST)

        # Having a nested if statement is necessary here because an object
        # of the "MapDataForm" class must be verified as valid before being
        # saved, and saving a "MapDataForm" object is only applicable if
        # this view function has received a POST request.

        # "MapDataForm" was created as a form class based off the model
        # "MapDatabase" because I needed to check whether the data inputted
        # into the form class was valid for the "address" attribute which
        # was declared as a CharField.
        if mapForm.is_valid():
            mapForm.save()

            return redirect('display-cities')
    else:
        mapForm = MapDataForm()

    # For the following line to work, there must be at least one "MapDatabase" object.
    m_address = MapDatabase.objects.last()
    location = geocoder.osm(m_address)

    latitude = location.lat
    longitude = location.lng

    country = location.country
    city = location.city
    print("country: ", country)
    print("city: ", city)

    if latitude == None or longitude == None:
        m_address.delete()

        return render(request, 'map_app/invalid_city_map_location.html')

    mapObject = folium.Map(location=[19, -2], zoom_start=1.5)

    if city == None:
        folium.Marker([latitude, longitude], tooltip='Click For Description',
                      popup=country).add_to(mapObject)
    else:
        folium.Marker([latitude, longitude], tooltip='Click For Description',
                      popup=city).add_to(mapObject)

    # The following is a data frame with dots to display on the map.
    data = panda.DataFrame({
        'longitude': [-58.3816, 30.3609, 28.9784],
        'latitude': [-34.6037, 59.9311, 41.0082],
        'name': ['Buenos Aires', 'Saint Petersburg', 'İstanbul'],
    }, dtype=str)

    pk = 1
    for city in range(0, len(data)):
        folium.Marker(
            location=[data.iloc[city]['latitude'],
                      data.iloc[city]['longitude']],
            popup=f"<a href=http://127.0.0.1:8000/display-city/{pk} target='_top'>{ data.iloc[city]['name'] }</a>",
        ).add_to(mapObject)
        pk += 1

    mapObject = mapObject._repr_html_()

    content = {
        'mapObject': mapObject,
        'mapForm': mapForm,
    }

    return render(request, 'map_app/display_cities.html', content)
# def DisplayCities(request):


"""
DisplayCityInfo():

NAME

    DisplayCityInfo - handles the HttpRequests to the multiple 'display-city/pk/'
    addresses.

SYNOPSIS

    def DisplayCityInfo(request, pk):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

        pk             --> the primary key which Django is using in this case
        to have multiple web pages which only differ by one character in their
        URLs, be rendered by one view function.

DESCRIPTION

    This function will accept a web request, and will then return a web response.
    It takes an HttpRequest object and a primary key called "pk" as its parameters.
    
    It returns the HttpRequest object while simultaneously rendering an HTML
    template whose title f'display_city{pk}.html' is determined by the value
    of "pk".

RETURNS

    Returns an HttpResponse object while directing the user to the 
    f'display_city{pk}.html' template located inside the "map_app"
    application.

"""


def DisplayCityInfo(request, pk=None):
    if pk:
        return render(request, f'map_app/display_city{pk}.html')
# def DisplayCityInfo(request, pk=None):


"""
PlazaDeMayo():

NAME

    PlazaDeMayo - handles the HttpRequest to the 'plaza-de-mayo/' address.

SYNOPSIS

    def PlazaDeMayo(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'plaza_de_mayo.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 'plaza_de_mayo.html'
    template located inside the "map_app" application.

"""


def PlazaDeMayo(request):
    return render(request, 'map_app/plaza_de_mayo.html')
# def PlazaDeMayo(request):


"""
Caminito()

NAME

    Caminito - handles the HttpRequest to the 'caminito/' address.

SYNOPSIS

    def Caminito(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'caminito.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 'caminito.html'
    template located inside the "map_app" application.

"""


def Caminito(request):
    return render(request, 'map_app/caminito.html')
# def Caminito(request):


"""
BuenosAiresVideos()

NAME

    BuenosAiresVideos - handles the HttpRequest to the 'buenos-aires-videos/'
    address.

SYNOPSIS

    def BuenosAiresVideos(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and grab all of the "Video"
    objects that are related to the city of Buenos Aires, by filtering the 
    results to only include the names of specific videos in a Python list.
    The "Video" objects are then assigned to a variable called "videos".

    The variable "videos" is put inside a Python dictionary called "context",
    and finally, the HTML template titled 'buenos_aires_videos.html' is 
    rendered while the dictionary is passed to the template as well.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'buenos_aires_videos.html' template located inside the "map_app"
    application. A Python dictionary is returned as well, so that it
    can be accessed inside the HTML template.

"""


def BuenosAiresVideos(request):
    videoList = ["Buenos Aires Travel", "5 Famous Tombs In Recoleta Cemetery",
                 "La Boca", "Love & Hates of Visiting Buenos Aires"]

    videos = Video.objects.filter(m_title__in=videoList)

    context = {
        'videos': videos,
    }

    return render(request, 'map_app/buenos_aires_videos.html', context)
# def BuenosAiresVideos(request):


"""
RecoletaCemetery()

NAME

    RecoletaCemetery - handles the HttpRequest to the 'recoleta-cemetery/' address.

SYNOPSIS

    def RecoletaCemetery(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'recoleta_cemetery.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 'recoleta_cemetery.html'
    template located inside the "map_app" application.

"""


def RecoletaCemetery(request):
    return render(request, 'map_app/recoleta_cemetery.html')
# def RecoletaCemetery(request):


"""
BuenosAiresDetails()

NAME

    BuenosAiresDetails - handles the HttpRequest to the 'buenos-aires-details/'
    address.

SYNOPSIS

    def BuenosAiresDetails(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'buenos_aires_details.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'buenos_aires_details.html' template located inside the "map_app"
    application.

"""


def BuenosAiresDetails(request):
    return render(request, 'map_app/buenos_aires_details.html')
# def BuenosAiresDetails(request):


"""
BuenosAiresEnglishAndTransportation()

NAME

    BuenosAiresEnglishAndTransportation - handles the HttpRequest to the
    'buenos-aires-english-and-transportation/' address.

SYNOPSIS

    def BuenosAiresEnglishAndTransportation(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'buenos_aires_english_and_transportation.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'buenos_aires_english_and_transportation.html' template located
    inside the "map_app" application.

"""


def BuenosAiresEnglishAndTransportation(request):
    return render(request, 'map_app/buenos_aires_english_and_transportation.html')
# def BuenosAiresEnglishAndTransportation(request):


"""
BuenosAiresHistory()

NAME

    BuenosAiresHistory - handles the HttpRequest to the 'buenos-aires-history/'
    address.

SYNOPSIS

    def BuenosAiresHistory(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'buenos_aires_history.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'buenos_aires_history.html' template located inside the "map_app"
    application.

"""


def BuenosAiresHistory(request):
    return render(request, 'map_app/buenos_aires_history.html')
# def BuenosAiresHistory(request):


"""
SaintPetersburgHistory()

NAME

    SaintPetersburgHistory - handles the HttpRequest to the 'saint-petersburg-history/'
    address.

SYNOPSIS

    def SaintPetersburgHistory(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'saint_petersburg_history.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'saint_petersburg_history.html' template located inside the "map_app"
    application.

"""


def SaintPetersburgHistory(request):
    return render(request, 'map_app/saint_petersburg_history.html')
# def SaintPetersburgHistory(request):


"""
DvortsovayaPloshchad()

NAME

    DvortsovayaPloshchad - handles the HttpRequest to the 'dvortsovaya-ploshchad/'
    address.

SYNOPSIS

    def DvortsovayaPloshchad(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'dvortsovaya_ploshchad.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'dvortsovaya_ploshchad.html' template located inside the "map_app"
    application.

"""


def DvortsovayaPloshchad(request):
    return render(request, 'map_app/dvortsovaya_ploshchad.html')
# def DvortsovayaPloshchad(request):


"""
HermitageMuseum()

NAME

    HermitageMuseum - handles the HttpRequest to the 'hermitage-museum/' address.

SYNOPSIS

    def HermitageMuseum(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'hermitage_museum.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'hermitage_museum.html' template located inside the "map_app"
    application.

"""


def HermitageMuseum(request):
    return render(request, 'map_app/hermitage_museum.html')
# def HermitageMuseum(request):


"""
ChurchofTheSaviourOnBlood()

NAME

    ChurchofTheSaviourOnBlood - handles the HttpRequest to the
    'church-of-the-saviour-on-blood/' address.

SYNOPSIS

    def ChurchofTheSaviourOnBlood(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'church_of_the_saviour_on_blood.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'church_of_the_saviour_on_blood.html' template located inside
    the "map_app" application.

"""


def ChurchofTheSaviourOnBlood(request):
    return render(request, 'map_app/church_of_the_saviour_on_blood.html')
# def ChurchofTheSaviourOnBlood(request):


"""
SaintPetersburgDetails()

NAME

    SaintPetersburgDetails - handles the HttpRequest to the 'saint-petersburg-details/'
    address.

SYNOPSIS

    def SaintPetersburgDetails(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'saint_petersburg_details.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'saint_petersburg_details.html' template located inside the
    "map_app" application.

"""


def SaintPetersburgDetails(request):
    return render(request, 'map_app/saint_petersburg_details.html')
# def SaintPetersburgDetails(request):


"""
SaintPetersburgEnglishAndTransportation()

NAME

    SaintPetersburgEnglishAndTransportation - handles the HttpRequest to the
    'saint-petersburg-english-and-transportation/' address.

SYNOPSIS

    def SaintPetersburgEnglishAndTransportation(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'saint_petersburg_english_and_transportation.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'saint_petersburg_english_and_transportation.html' template 
    located inside the "map_app" application.

"""


def SaintPetersburgEnglishAndTransportation(request):
    return render(request, 'map_app/saint_petersburg_english_and_transportation.html')
# def SaintPetersburgEnglishAndTransportation(request):


"""
SaintPetersburgVideos()

NAME

    SaintPetersburgVideos - handles the HttpRequest to the 'saint-petersburg-videos/'
    address.

SYNOPSIS

    def SaintPetersburgVideos(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and grab all of the "Video"
    objects that are related to the city of Saint Petersburg, by filtering
    the results to only include the names of specific videos in a Python
    list. The "Video" objects are then assigned to a variable called "videos".

    The variable "videos" is put inside a Python dictionary called "context",
    and finally, the HTML template titled 'saint_petersburg_videos.html' is 
    rendered while the dictionary is passed to the template as well.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'saint_petersburg_videos.html' template located inside the "map_app"
    application. A Python dictionary is returned as well, so that it
    can be accessed inside the HTML template.

"""


def SaintPetersburgVideos(request):
    videoList = ["St. Petersburg Travel Guide", "St. Petersburg's Famous Attractions",
                 "St. Petersburg Boat Tour", "Peterhof Palace"]

    videos = Video.objects.filter(m_title__in=videoList)

    context = {
        'videos': videos,
    }

    return render(request, 'map_app/saint_petersburg_videos.html', context)
# def SaintPetersburgVideos(request):


"""
TopkapiPalace()

NAME

    TopkapiPalace - handles the HttpRequest to the 'topkapi-palace/' address.

SYNOPSIS

    def TopkapiPalace(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'topkapi_palace.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'topkapi_palace.html' template 
    located inside the "map_app" application.

"""


def TopkapiPalace(request):
    return render(request, 'map_app/topkapi_palace.html')
# def TopkapiPalace(request):


"""
SultanahmetMosque()

NAME

    SultanahmetMosque - handles the HttpRequest to the 'sultanahmet-mosque/' address.

SYNOPSIS

    def SultanahmetMosque(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'sultanahmet_mosque.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'sultanahmet_mosque.html' template 
    located inside the "map_app" application.

"""


def SultanahmetMosque(request):
    return render(request, 'map_app/sultanahmet_mosque.html')
# def SultanahmetMosque(request):


"""
GrandBazaar()

NAME

    GrandBazaar - handles the HttpRequest to the 'grand-bazaar/' address.

SYNOPSIS

    def GrandBazaar(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'grand_bazaar.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'grand_bazaar.html' template 
    located inside the "map_app" application.

"""


def GrandBazaar(request):
    return render(request, 'map_app/grand_bazaar.html')
# def GrandBazaar(request):


"""
IstanbulVideos()

NAME

    IstanbulVideos - handles the HttpRequest to the 'istanbul-videos/'
    address.

SYNOPSIS

    def IstanbulVideos(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and grab all of the "Video"
    objects that are related to the city of İstanbul, by filtering the 
    results to only include the names of specific videos in a Python list.
    The "Video" objects are then assigned to a variable called "videos".

    The variable "videos" is put inside a Python dictionary called "context",
    and finally, the HTML template titled 'istanbul_videos.html' is rendered
    while the dictionary is passed to the template as well.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'istanbul_videos.html' template located inside the "map_app"
    application. A Python dictionary is returned as well, so that
    it can be accessed inside the HTML template.

"""


def IstanbulVideos(request):
    videoList = ["Topkapı Palace", "Hagia Sophia",
                 "İstanbul Grand Bazaar", "İstanbul Drone View"]

    videos = Video.objects.filter(m_title__in=videoList)

    context = {
        'videos': videos,
    }

    return render(request, 'map_app/istanbul_videos.html', context)
# def IstanbulVideos(request):


"""
IstanbulHistory()

NAME

    IstanbulHistory - handles the HttpRequest to the 'grand-bazaar/' address.

SYNOPSIS

    def IstanbulHistory(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'istanbul_history.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'istanbul_history.html' template located inside the "map_app"
    application.

"""


def IstanbulHistory(request):
    return render(request, 'map_app/istanbul_history.html')
# def IstanbulHistory(request):


"""
IstanbulEnglishAndTransportation()

NAME

    IstanbulEnglishAndTransportation - handles the HttpRequest to the
    'istanbul-english-and-transportation/' address.

SYNOPSIS

    def IstanbulEnglishAndTransportation(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'istanbul_english_and_transportation.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'istanbul_english_and_transportation.html' template located 
    inside the "map_app" application.

"""


def IstanbulEnglishAndTransportation(request):
    return render(request, 'map_app/istanbul_english_and_transportation.html')
# def IstanbulEnglishAndTransportation(request):


"""
IstanbulDetails()

NAME

    IstanbulDetails - handles the HttpRequest to the 'istanbul-details/' address.

SYNOPSIS

    def IstanbulDetails(request):
        request        --> the HttpRequest object which Django uses to pass
        state through the system.

DESCRIPTION

    This function will accept a web request, and then will return a web response.
    It takes the HttpRequest object which is its parameter, and returns it while
    rendering the HTML template titled 'istanbul_details.html'.

RETURNS

    Returns an HttpResponse object while directing the user to the 
    'istanbul_details.html' template located inside the "map_app"
    application.

"""


def IstanbulDetails(request):
    return render(request, 'map_app/istanbul_details.html')
# def IstanbulDetails(request):

# 153
