from .service import Service
from .ipapi import Ipapi
from .geoplugin import Geoplugin

import sys
import time
import random
from bisect import bisect


class GeolocationAPIHandler (Service):
    '''
    The facade of all the geolocation api services classes.
    '''

    dummy_res = {'ip':'0.0.0.0', 'country_name':'invalid', 'longitude':float('inf'), 'latitude':float('inf')}
    config = None

    def __init__(self, keyfile_path):
        self.services = {}
        self.service_count = 0
        self.service_name_map = {
        'ipapi': Ipapi,
        'geoplugin': Geoplugin
        }
        try:
            with open(keyfile_path) as kf:
                for line in kf:
                    token = line.strip().split(' ')
                    if len(token) == 0:
                        continue
                    self.add_service(token[0], token[1:])
        except FileNotFoundError:
            print("[Error] Cannot find {0}, it is required for using geolocation API.".format(keyfile_path), file = self.config.stderr)
            exit(1)

        # compute probability for each service by their cd time
        self.acd = 0
        self.p = [0]
        for service in self.services.values():
            self.acd += 1 / service.cd
            self.p.append(self.acd)

    def add_service(self, name, argv):
        if not name in self.service_name_map:
            print("[Warning] Unknown geolocation API service name: {0}. Ignored.".format(name), file = self.config.stderr)
            return
        self.services[self.service_count] = (self.service_name_map[name](argv))
        self.service_count += 1

    def request(self, ip):
        re = []
        i = 0
        while i < self.config.qt:
            # random select a service based on their cd time
            c = bisect(self.p, random.uniform(0, self.acd)) - 1
            b = self.services[c].lock.acquire(timeout = self.acd)
            if b: # lock acquired
                g = self.services[c].request(ip)
                if g == None: # something went wrong
                    print("[Error] Something went wrong when querying ip {0} with {1}. Return: {2}".format(ip, self.services[c], g), file = self.config.stderr)
                    exit(1)
                re.append(g)
                self.services[c].lock.release()
                i += 1
            else: # failed to acquired lock
                continue
        # average
        # Since all the locations is inside Taiwan (or should be), just compute lon's and lat's average
        lon = 0
        lat = 0
        for i in range(self.config.qt):
            if re[i]['ip'] != ip or 'Taiwan' not in re[i]['country_name']: # this really shouldn'y happens
                print("[Error] service return incorrect. ip: {0}, country: {1}.".format(re[i]['ip'], re[i]['country_name']), file = self.config.stderr)
                continue
            lon += float(re[i]['longitude'])
            lat += float(re[i]['latitude'])
        return {'ip': ip, 'country_name': 'Taiwan', 'longitude': lon / self.config.qt, 'latitude': lat / self.config.qt}

