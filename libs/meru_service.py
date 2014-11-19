import json
import urllib
import webapp2
import yaml
import config
from datetime import datetime
from base_service import BaseService
from google.appengine.api import urlfetch

class MeruService(BaseService):

    @property
    def name(self):
        return "Meru"

    @property
    def has_api(self):
        return False

    def get_path(self):
        meru_config = config.app_config.get('meru')
        return meru_config.get('data_file')

    """
    File path can be obtained from config. However it is also provided as an
    argument to facilitate testing. Since get_app is not available in unittests or
    maybe there's a better way of doing it.
    """
    def load_data(self):
        stream = open(self.get_path(), 'r')
        return yaml.load(stream)

    """
    AVOID using this method. This method calls the get_fare_by_distance
    to calculate fare. Distance is calculated by method in base service and it's
    an approximation since it doesn't account the variation due to the nature of roads

    Only use this method if you have no other option
    """
    def _get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
        approx_distance = self.calculate_distance(src_lat, src_long,
                dst_lat, dst_long)
        result = get_fare_by_distance(approx_distance)
        return result


    def get_rule_for_given_time(self, rules, time):
        midnight = datetime.strptime('00:00', '%H:%M')
        for rule_index in rules:
            rule = rules.get(rule_index)
            import pdb; pdb.set_trace()
            time_from   = datetime.strptime(rule.get('time_from'), '%H:%M')
            time_to     = datetime.strptime(rule.get('time_to'), '%H:%M')
            travel_time = datetime.strptime(datetime.strptime(time, '%H:%M'))
        datetime.strptime('', '%H:%M').time()


    def calculate_fare(self, rules, distance, time=datetime.now()):
        self.get_rule_for_given_time(rules, time)

    """
    Returns fare for various service types/vehicle types based on distance
    and city.
    Input: instance of Route class
    Returns: dict containing fair information

    We pass Route object since we need city and distance information
    """
    def _get_fare_by_distance(self, route):
        mdata = self.load_data().get('meru')
        city  = self.find_city(mdata, route)
        if not city:
            return {}

        service_rules_for_city = mdata.get(city).get('service_type')
        distance_in_meters = route.distance

        for service_type in service_rules_for_city:
            self.calculate_fare(service_rules_for_city.get(service_type),
                    distance_in_meters)


    """
    This is a method reserved for future use. Just in case we want to pass
    some extra information for any service.

    Return: Empty hash implies no extra information available
    """
    def get_extra_information(self):
        return {}

    """
    Not available for meru.
    """
    def get_min_response_time(self):
        raise NotImplementedError("Subclasses should implement this!")
