##to use google geoservices to geocode an address 
import googlemaps
import numpy as np

KEY = "<<KEY>>"

gmaps = googlemaps.Client(key=KEY)

bounds = {
        'southwest': [52.9736687, -4.0191978],
        'northeast': [53.3505406,-3.4648583]
    }

#try a point
xbounds = {
        'southwest': [53.247139 , -3.7559509],
        'northeast': [53.247139 , -3.7559509]
    }

def get_coordinates(address):
    #geocode_result = gmaps.geocode(str(address),region='GB',bounds=bounds)
    geocode_result = gmaps.geocode(str(address),region='GB')
    if len(geocode_result) > 0:
        print('check')
        return list(geocode_result[0]['geometry']['location'].values())
    else:
        return [np.NaN, np.NaN]

# def get_rev_coordinates(long,lat):
#
#     reverse_geocode_result = gmaps.reverse_geocode((long, lat))
#     if len(reverse_geocode_result) > 0:
#         return list(reverse_geocode_result[0]['geometry']['location'].values())
#     else:
#         return [np.NaN]

