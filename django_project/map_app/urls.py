from django.urls import path

# All URL patterns related to the "map_app"
# app are defined in this file.

from .views import (
	SearchMap, DisplayCities, DisplayBuenos, DisplayPeter,
	DisplayIstanbul, PlazaDeMayo, Caminito, BuenosAiresVideos,
	RecoletaCemetery, BuenosAiresDetails,
	BuenosAiresEnglishAndTransportation, BuenosAiresHistory,
	SaintPetersburgHistory, DvortsovayaPloshchad, HermitageMuseum,
	ChurchofTheSaviourOnBlood, SaintPetersburgDetails,
	SaintPetersburgEnglishAndTransportation, SaintPetersburgVideos,
	TopkapiPalace, SultanahmetMosque, GrandBazaar, IstanbulVideos,
	IstanbulHistory, IstanbulEnglishAndTransportation,
	IstanbulDetails
)

urlpatterns = [
	path('search-map/', SearchMap, name='search-map'),

	path('display-cities/', DisplayCities,
    name='display-cities'),

	path('display-buenos/', DisplayBuenos),

	path('display-peter/', DisplayPeter),

	path('display-istanbul/', DisplayIstanbul),

	# Buenos Aires
	path('plaza-de-mayo/', PlazaDeMayo, name='plaza-de-mayo'),

	path('caminito/', Caminito, name='caminito'),

	path(
    'buenos-aires-videos/', BuenosAiresVideos,
    name='buenos-aires-videos'),

	path('recoleta-cemetery/', RecoletaCemetery,
    name='recoleta-cemetery'),

	path('buenos-aires-details/', BuenosAiresDetails,
		name='buenos-aires-details'),

	path('buenos-aires-english-and-transportation/',
		BuenosAiresEnglishAndTransportation,
    name='buenos-aires-english-and-transportation'),

	path('buenos-aires-history/', BuenosAiresHistory,
		name='buenos-aires-history'),

	# Saint Petersburg
	path('saint-petersburg-history/', SaintPetersburgHistory,
		name='saint-petersburg-history'),

	path('dvortsovaya-ploshchad/', DvortsovayaPloshchad,
		name='dvortsovaya-ploshchad'),

	path('hermitage-museum/', HermitageMuseum,
    name='hermitage-museum'),

	path('church-of-the-saviour-on-blood/',
    ChurchofTheSaviourOnBlood,
		name='church-of-the-saviour-on-blood'),

	path('saint-petersburg-details/', SaintPetersburgDetails,
		name='saint-petersburg-details'),

	path('saint-petersburg-english-and-transportation/',
		SaintPetersburgEnglishAndTransportation,
    name='saint-petersburg-english-and-transportation'),

	path('saint-petersburg-videos/', SaintPetersburgVideos,
		name='saint-petersburg-videos'),

	# İstanbul
	path('topkapi-palace/', TopkapiPalace,
    name='topkapi-palace'),

	path('sultanahmet-mosque/', SultanahmetMosque,
    name='sultanahmet-mosque'),

	path('grand-bazaar/', GrandBazaar,
    name='grand-bazaar'),

	path('istanbul-history/', IstanbulHistory,
    name='istanbul-history'),

	path('istanbul-english-and-transportation/',
    IstanbulEnglishAndTransportation,
		name='istanbul-english-and-transportation'),

	path('istanbul-details/', IstanbulDetails,
    name='istanbul-details'),

	path('istanbul-videos/', IstanbulVideos,
    name='istanbul-videos')
]

# 46