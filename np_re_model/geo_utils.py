import numpy as np
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import pandas as pd
import zipcodes

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


def get_zipcode_coordinates(zip_code):
    """Return latitude and longitude for a US zip code using offline data."""
    result = zipcodes.matching(str(zip_code))
    if result:
        try:
            return float(result[0]['lat']), float(result[0]['long'])
        except (KeyError, TypeError, ValueError):
            return None, None
    return None, None


def load_us_mainland_zipcodes():
    """Return a DataFrame of mainland US zip codes with coordinates."""
    mainland_states = {
        'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN',
        'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
        'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
        'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'DC'
    }
    records = [
        {
            'zip_code': z['zip_code'],
            'latitude': float(z['lat']),
            'longitude': float(z['long'])
        }
        for z in zipcodes.list_all()
        if z.get('state') in mainland_states
    ]
    return pd.DataFrame(records)
