import json
import urllib
import webapp2
import yaml
import config
import math
import operator
import datetime as dt
from base_service import BaseService
from google.appengine.api import urlfetch
import helper_functions as hf

class MeruService(BaseService):

    meru_data = None

    def __init__(self):
        self.info = {}

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
    This method returns the rule based on time of travel.
    if the time of travel coincides with the boundary of fare intervals
    we simply add 5 minutes delay to avoid any weird results.
    """
    def get_rule_for_given_time(self, rules, _time):
        selected_rules = []
        for rule in rules:
            _time_from   = dt.datetime.strptime(rule.get('time_from'), '%H:%M')
            _time_to     = dt.datetime.strptime(rule.get('time_to'), '%H:%M')
            # add 5 minutes if we are on boundary
            time_from = _time_from.time()
            time_to   = _time_to.time()
            time      = _time.time()
            if (time_from == time or time_to == time):
                _time = _time + dt.timedelta(seconds=300)
                time = _time.time()

            if (time > time_from and time < time_to):
                selected_rules.append(rule)
                continue
            elif (time >= time_from and time > time_to):
                if (hf.sub_time(time, time_from).hour < 12):
                #if ((time - time_from).seconds // 3600 < 12):
                    selected_rules.append(rule)
                    continue
            elif (time <= time_from and time < time_to):
                if ( hf.sub_time(time_to, time).hour < 12):
                #if ( (time_to - time).seconds // 3600 < 12):
                    selected_rules.append(rule)
                    continue
        return selected_rules

    """
    Get the rules for given time from the set of rules available
    for meru.
    Input: rules for a service type in a given service
    Example:  rules = (meru -> mumbai -> service_type -> meru_cabs)
    TODO(goyalankit) verify the algorithm again. Though it passes all the
    written test cases.
    """
    def get_rules_for_trip(self, rules, time, duration, city):
        start_time    = dt.datetime.strptime(time.strftime("%H:%M"), '%H:%M')
        end_time      = time + dt.timedelta(seconds=duration)

        city_filter = lambda x: x['city'].lower() == city.lower()
        start_rules = filter (city_filter, self.get_rule_for_given_time(rules, start_time))
        end_rules   = filter (city_filter, self.get_rule_for_given_time(rules, end_time))
        start_rules.extend(end_rules)
        return start_rules

    """
    This method calculates fare based on the given rule.
    Algorithm:
    1. Apply the fix fare for given number of kms
    2. Apply the rs/km to the remaining distance in kms
    """
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


    """
    This private method, updates the extra info with waiting charges,
    boolean showing if night charges were applied.
    """
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
            self.info['other_info'] = s_rule['info']
        elif e_rule.get('info', False):
            self.info['other_info'] = e_rule['info']

    """
    Helper method to get fares for both the start time rule and end time
    rule.
    Start and End time may overlap with two different intervals of fares.
    We calculate for both the intervals and then show the higher of the two
    intervals.
    This method also calls the method to update extra information
    """
    def _calculate_fare(self, service_rules, distance, duration, city, time=dt.datetime.now()):
        rules = self.get_rules_for_trip(service_rules, time, duration, city)
        if not rules:
            return None

        rules_by_service = {}
        for rule in rules:
            if rule['service_type'] in rules_by_service:
                rules_by_service[rule['service_type']].append(rule)
            else:
                rules_by_service[rule['service_type']] = [rule]

        fares_by_service = {}
        for service_type in rules_by_service:
            fares_by_service[service_type] = {}
            for rule in rules_by_service[service_type]:
                _rule_fare = self.__calculate_fare_per_rule(rule, distance)
                if fares_by_service[service_type].get('fare', 0) < _rule_fare:
                    fares_by_service[service_type]['fare'] = _rule_fare
                    fares_by_service[service_type]['rule'] = rule
        return fares_by_service


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
        if not city: return {}
        distance_in_meters     = route.distance
        duration               = route.duration
        fare = self._calculate_fare(mdata, distance_in_meters, duration, city)
        return fare

    def get_fare(self, route):
        return self._get_fare_by_distance(route)

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
