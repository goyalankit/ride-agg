import json
import urllib
import webapp2
import yaml
import config
from datetime import datetime
from base_service import BaseService
from google.appengine.api import urlfetch
import helper_functions as hf

class MeruService(BaseService):

    meru_data = None

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
    Method to load data. This only loads the data once and put it into
    the static variable "meru_data". This method is idempotent so thread safe too.
    """
    def load_data(self):
        if not MeruService.meru_data:
            stream = open(self.get_path(), 'r')
            MeruService.meru_data = yaml.load(stream)
        return MeruService.meru_data

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


    """
    Get the rule for given time from the set of rules available
    for meru.
    Input: rules for a service type in a given service
    Example:  rules = (meru -> mumbai -> service_type -> meru_cabs)
    """
    def get_rule_for_given_time(self, rules, time):
        midnight = datetime.strptime('00:00', '%H:%M')
        selected_rule = None
        for rule in rules:
            #rule = rules.get(rule_index)
            time_from   = datetime.strptime(rule.get('time_from'), '%H:%M')
            time_to     = datetime.strptime(rule.get('time_to'), '%H:%M')
            travel_time = datetime.strptime(time.strftime("%H:%M"), '%H:%M')
            if (travel_time > time_from and travel_time < time_to):
                selected_rule = rule
                break
            elif (travel_time > time_from and travel_time > time_to):
                if ((travel_time - time_from).seconds // 3600 < 12):
                    selected_rule = rule
                    break
            elif (travel_time < time_from and travel_time < time_to):
                if ( (time_to - travel_time).seconds // 3600 < 12):
                    selected_rule = rule
                    break

        return selected_rule

    def calculate_fare(self, rules, distance, duration, time=datetime.now()):
        time_charged_for = time + datetime.timedelta(seconds=duration)
        self.get_rule_for_given_time(rules, time)

    """
    Returns fare for various service types/vehicle types based on distance
    and city.
    Input: instance of Route class
    Returns: dict containing fair information

    We pass Route object since we need city and distance information
    """
    def _get_fare_by_distance(self, route):
        mdata = self.load_data()
        city  = hf.find_city(mdata, route)
        if not city:
            return {}

        service_rules_for_city = mdata.get(city).get('service_type')
        distance_in_meters     = route.distance
        dutation               = route.dutation

        for service_type in service_rules_for_city:
            self.calculate_fare(service_rules_for_city.get(service_type),
                    distance_in_meters, duration)
        #TODO(goyalankit) finish this method
        return {}

    def get_fare(self, route):
        return self._get_fare_by_distance(self, route)

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
