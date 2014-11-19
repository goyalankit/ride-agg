import json
import urllib
import webapp2
import yaml
from base_service import BaseService
from google.appengine.api import urlfetch

class Olacabsservice(BaseService):
    _data = None

    @property
    def name(self):
        return "olacabs"

    @property
    def has_api(self):
        return False

    def get_data(self):
        if self._data is None:
            stream = open(os.path.join('../data',self.name+'.yaml'))
            self._data = yaml.load(stream)
        return self._data

    """
    AVOID using this method. This method calls the get_fare_by_distance to
    calculate fare. Distance is calculated by method in base service and it's an
    approximation since it doesn't account the variation due to the nature of
    roads

    Only use this method if you have no other option
    """
    def get_fare_by_lat_lang(self, src_lat, src_long, dst_lat, dst_long):
        approx_distance = self.calculate_distance(src_lat, src_long,
                dst_lat, dst_long)
        result = get_fare_by_distance(approx_distance)
        return result

    # todo
    # - include time of day pricing in calculation
    # - include city in pricing
    # - include currency in pricing (?)
    def get_fare_by_distance(self, route):
        ds = self.get_data()
        distance = route.distance

        fare = 0
        if 'fixed_fare_km' in mdata:
            fare += ds['fixed_fare']*ds['fixed_fare_km']
            distance -= ds['fixed_fare_km']
        fare += distance*ds['fare_per_km']

        return fare

    """
    This is a method reserved for future use. Just in case we want to pass
    some extra information for any service.

    Return: Empty hash implies no extra information available
    """
    def get_extra_information(self):
        return {}

    def get_min_response_time(self):
        """If available give minimum response time.
        Otherwise return -1
        """
        return
        
