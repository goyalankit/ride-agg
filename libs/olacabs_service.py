import os
import json
import yaml
import urllib
import config
import datetime
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
        address = route.start_address.lower().split(',')

        f = lambda s: ((s['city'].lower() in address)
                       and (('time_from' not in s)
                            or (s['time_from'] <= time <= s['time_to'])))

        return filter(f, self.get_data())

    # TODO
    # add ride time rate charge
    def get_fare(self, route):
        services = self.query_services(route)

        for svc in services:
            fare = 0
            distance = route.distance # assuming kilometers
            fare_rate = svc['fare_per_km']

            if 'fixed_fare_dist_km' in svc:
                fixed_fare_dist = min(distance, svc['fixed_fare_dist_km'])
                fare += fixed_fare_dist*svc['fixed_fare_per_km']
                distance -= fixed_fare_dist
            elif 'fixed_fare_per_km' in svc:
                fare_rate = svc['fixed_fare_per_km']

            fare += distance*fare_rate
            svc['fare'] = fare

        return services
