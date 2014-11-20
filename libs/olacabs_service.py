# import config
import os
import json
import urllib
import yaml
from base_service import BaseService
import datetime


class OlacabsService(BaseService):
    @property
    def name(self):
        return "olacabs"

    @property
    def has_api(self):
        return False

    def get_data(self):
        with open(os.path.join('../data', self.name+'.yaml'),'r') as df:
        # with open(config.app_config.get(self.name)['data_file'],'r') as df:
            data = yaml.load(df)
        return data

    def query_services(self,route,time=datetime.datetime.now()):
        city = route.start_address.split(',')[0].lower()

        f = lambda s: ((city == s['city'].lower())
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
