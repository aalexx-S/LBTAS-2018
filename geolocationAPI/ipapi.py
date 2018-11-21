from .service import Service

import requests
import json
import time

from threading import Lock, Thread

class Ipapi (Service):

    lock = Lock()
    cd = 0.45

    def __init__(self, _):
        pass

    def request(self, ip):
        r = requests.get('http://ip-api.com/json/' + ip)
        r = json.loads(r.text)
        if r['status'] == 'fail':
            return None
        time.sleep(self.cd) # to make sure we don't get banned. I don't want to implement a timeout lock...
        return {'ip': ip, 'country_name': r['country'], 'longitude': r['lon'], 'latitude': r['lat']}
