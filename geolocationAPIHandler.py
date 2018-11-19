invalid_longitude = float('inf')
invalid_latitude = float('inf')
invalide_name = 'dummy'

def geolocation_API_handler (ip):
    res = {'longitude': invalid_longitude, 'latitude': invalid_latitude, 'country_name': invalide_name, 'region_name': invalide_name, 'city_name': invalide_name}

    return res
