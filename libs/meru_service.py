import json
import urllib
import webapp2
import yaml
import config
import math
from datetime import datetime
from datetime import timedelta
from base_service import BaseService
from google.appengine.api import urlfetch
import helper_functions as hf

class MeruService(BaseService):

    meru_data = None

    def __init__(self):
        self.info = {}

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


    def get_rule_for_given_time(self, rules, time):
        selected_rule = None
        for rule in rules:
            time_from   = datetime.strptime(rule.get('time_from'), '%H:%M')
            time_to     = datetime.strptime(rule.get('time_to'), '%H:%M')
            # add 5 minutes if we are on boundary
            if (time_from == time or time_to == time):
                time = time + timedelta(seconds=300)

            if (time > time_from and time < time_to):
                selected_rule = rule
                break
            elif (time >= time_from and time > time_to):
                if ((time - time_from).seconds // 3600 < 12):
                    selected_rule = rule
                    break
            elif (time <= time_from and time < time_to):
                if ( (time_to - time).seconds // 3600 < 12):
                    selected_rule = rule
                    break
        return selected_rule

    """
    Get the rules for given time from the set of rules available
    for meru.
    Input: rules for a service type in a given service
    Example:  rules = (meru -> mumbai -> service_type -> meru_cabs)
    TODO(goyalankit) verify the algorithm again. Though it passes all the
    written test cases.
    """
    def get_rules_for_trip(self, rules, time, duration):
        start_time    = datetime.strptime(time.strftime("%H:%M"), '%H:%M')
        end_time      = time + timedelta(seconds=duration)

        start_rule = self.get_rule_for_given_time(rules, start_time)
        end_rule   = self.get_rule_for_given_time(rules, end_time)

        return start_rule, end_rule

    def __calculate_fare_per_rule(self, rule, distance):
        fare = 0
        dist_in_km = distance / 1000.0
        if 'fixed_fare' in rule:
            fare += rule['fixed_fare']
            dist_in_km -= rule['dist_km_for_fixed_fare']
            if (dist_in_km <= 0):
                return fare

        ceil_distance = math.ceil(dist_in_km)
        fare += ceil_distance * rule['fare_per_km_after_fixed']
        return fare


    def __update_fare_related_info(self, s_rule, s_fare, e_rule, e_fare):
        # wauting charges if present otherwise set to None
        if (s_fare >= e_fare):
            self.info['wait_charge_per_min'] = s_rule.get('wait_charge_per_min', None)
        else:
            self.info['wait_charge_per_min'] = e_rule.get('wait_charge_per_min', None)

        # add info about night charges
        self.info['night_charges_used'] = s_rule.get('night', False) or \
                                          e_rule.get('night', False)

        # add any other information in data like free waiting for first
        # few minutes
        if s_rule.get('night', False) and s_rule.get('info', False):
            self.info['other_info'] = s_rule['info']
        elif e_rule.get('night', False) and e_rule.get('info', False):
            self.info['other_info'] = e_rule['info']
        elif s_fare > e_fare and s_rule.get('info', False):
            self.info['other_info'] = s_rule['info']
        elif s_fare < e_fare and e_rule.get('info', False):
            self.info['other_info'] = e_rule['info']
        elif s_rule.get('info', False):
            self.info['other_info']  = s_rule['info']
        elif e_rule.get('info', False):
            self.info['other_info']  = e_rule['info']


    def _calculate_fare(self, rules, distance, duration, time=datetime.now()):
        s_rule, e_rule = self.get_rules_for_trip(rules, time, duration)
        if (not s_rule) or (not e_rule):
            return None

        s_fare = self.__calculate_fare_per_rule(s_rule, distance)
        e_fare = self.__calculate_fare_per_rule(e_rule, distance)

        self.__update_fare_related_info( s_rule, s_fare, e_rule, e_fare)

        return max(s_fare, e_fare)


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

        distance_in_meters     = route.distance
        duration               = route.duration

        fare = self._calculate_fare(mdata, distance_in_meters, duration)
        return fare

    def get_fare(self, route):
        return self._get_fare_by_distance(self, route)

    """
    This is a method reserved for future use. Just in case we want to pass
    some extra information for any service.

    Return: Empty hash implies no extra information available
    """
    def get_extra_information(self):
        return self.info

    """
    Not available for meru.
    """
    def get_min_response_time(self):
        raise NotImplementedError("Subclasses should implement this!")
