from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

def findGeocode(country):
    try:
        geolocator = Nominatim(user_agent="himalayas_analytics")
        return geolocator.geocode(country)
      
    except GeocoderTimedOut:
        return findGeocode(country)