import numpy as np
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

_geolocator = Nominatim(user_agent="np-retail-geocoder")

def get_eps_from_miles(miles, reference_latitude):
    origin = (reference_latitude, 0)
    destination = great_circle(miles=miles).destination(origin, bearing=0)
    eps_latitude = abs(destination[0] - origin[0])
    destination = great_circle(miles=miles).destination(origin, bearing=90)
    eps_longitude = abs(destination[1] - origin[1])
    return min(eps_latitude, eps_longitude)

def distance_to_nearest_retail(point, retail_locations):
    return min(great_circle(point, retail_loc).miles for retail_loc in retail_locations)


def geocode_address(address):
    """Lookup latitude and longitude for a given address using Nominatim."""
    try:
        location = _geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except GeocoderServiceError:
        pass
    return None, None
