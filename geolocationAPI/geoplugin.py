from .service import Service

import requests
import json
import time

from threading import Lock, Thread

class Geoplugin (Service):

    lock = Lock()
    cd = 0.51

    def __init__(self, _):
        pass

    def request(self, ip):
        r = requests.get('http://www.geoplugin.net/json.gp?ip=' + ip)
        r = json.loads(r.text)
        if r['geoplugin_status'] != 200:
            return None
        time.sleep(self.cd) # to make sure we don't get banned. I don't want to implement a timeout lock...
        return {'ip': ip, 'country_name': r['geoplugin_countryName'], 'longitude': r['geoplugin_longitude'], 'latitude': r['geoplugin_latitude']}
