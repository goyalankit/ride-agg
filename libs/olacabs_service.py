import os
import json
import yaml
import urllib
import config
import datetime
import helper_functions as hf
from base_service import BaseService


class OlacabsService(BaseService):
    fare_data = None

    @property
    def has_api(self):
        return False

    def get_data(self):
        if OlacabsService.fare_data is None:
            dpath = config.app_config.get(self.name.lower()).get('data_file')
            with open(dpath,'r') as dfile:
                self.__class__.fare_data = yaml.load(dfile)
        return self.__class__.fare_data

    def query_services(self,route,time=datetime.datetime.now()):
        address = route.start_address.lower()

        city = hf.find_city(self.get_data(), route)
        if city: city = city.lower()

        f = lambda s: ((s['city'].lower() in city)
                       and (('time_from' not in s)
                            or (s['time_from'] <= time <= s['time_to'])))

        return filter(f, self.get_data())

    # TODO
    # add ride time rate charge
    def get_fare(self, route):
        services = self.query_services(route)

        for svc in services:
            distance = route.distance

            # initial fare is the minimum fare if there is one
            svc['fare'] = 0

            # subtract the distance that minimum payment covers
            if 'fixed_fare_dist_km' in svc:
                svc['fare'] += svc['fixed_fare']
                distance -= min(distance, svc['fixed_fare_dist_km']*1000)

            # the rest of the ride is charged at the regular rate
            svc['fare'] += distance*svc['fare_per_km']/1000.

            svc['fare'] = max(svc['fixed_fare'], svc['fare'])

            # in case of charging by ride time
            if 'fare_per_min' in svc:
                rate_by_time = round(route.duration*svc['fare_per_min']/60.)
                svc['fare'] += rate_by_time

            svc['fare'] += svc.get('service_tax',0)
        return sorted(services, key=lambda k: k['fare'])
