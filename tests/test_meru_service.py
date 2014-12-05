import unittest
import webapp2
import json
import os
from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.ext import db
from datetime import datetime

from libs.meru_service import MeruService
from models.route import Route
import libs.helper_functions as helper_functions

class TestMeruService(unittest.TestCase):

    def get_route(self):
        route_s = open('tests/data/route.json', 'r')
        route_j = json.load(route_s)
        route = Route()
        route.json2Obj(route_j)
        return route


    """
    Check that the distance calculation is not off by much
    """
    def setUp(self):
        self.meru = MeruService()
        self.route = self.get_route()

    """
    Simple test case to check that we are able to load and
    parse meru.yaml file
    """
    def test_load_data(self):
        data = self.meru.load_data()
        self.assertEqual(data[0] is not None, True)
        self.assertEqual(data[0]['city'] is not None, True)

    def test_find_city_when_not_present(self):
        """Returns None when city is not present"""
        route_temp = Route()
        route_temp.start_address = "i live in austin"
        city_n_p = helper_functions.find_city(self.meru.load_data(), route_temp)
        self.assertEqual(None, city_n_p)

    """
    Test for night time
    """
    def test_rule_for_given_time(self):
        rules = [
                {'rule' : 1, 'time_from' : '23:00', 'time_to' : '05:00', 'service_type' : 'Meru Cabs'},
                {'rule' : 2, 'time_from' : '05:00', 'time_to' : '23:00', 'service_type' : 'Meru Cabs'},
                {'rule' : 3, 'time_from' : '23:00', 'time_to' : '05:00', 'service_type' : 'Meru Flexi'},
                {'rule' : 4, 'time_from' : '05:00', 'time_to' : '23:00', 'service_type' : 'Meru Flexi'},
                ]

        # greater than all bounds
        time_to_check = datetime.strptime("23:50", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(rules[0] in s_rule, True)
        self.assertEqual(rules[2] in s_rule, True)

        # between the bound of day time
        time_to_check = datetime.strptime("05:50", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(rules[1] in s_rule, True)
        self.assertEqual(rules[3] in s_rule, True)

        # smaller than all the bounds
        time_to_check = datetime.strptime("03:00", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(rules[0] in s_rule, True)
        self.assertEqual(rules[2] in s_rule, True)

    def test_rule_for_given_time_for_day(self):
        rules = [
                    {'rule' : 1, 'time_from' : '23:59', 'time_to' : '05:00'},
                    {'rule' : 2, 'time_from' : '05:00', 'time_to' : '23:59'},
                ]
        time_to_check = datetime.strptime("00:00", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(s_rule, [rules[0]])

    def test_calculate_fare(self):
        """Checks that the fare is calculated correctly"""
        # TODO(goyalankit) Pending test case
        mdata = [
                    {
                      'rule'       : 1,
                      'time_from'  : '23:59',
                      'time_to'    : '05:00',
                      'fixed_fare' : 20,
                      'night'      : True,
                      'dist_km_for_fixed_fare'  : 1,
                      'fare_per_km_after_fixed' : 20.0,
                      'info'       : 'some info',
                      'city'       : 'Mumbai',
                      'service_type' : 'Meru Cabs'


                    },
                    {
                      'rule'       : 1,
                      'time_from'  : '05:00',
                      'time_to'    : '23:59',
                      'fixed_fare' : 10,
                      'night'      : False,
                      'dist_km_for_fixed_fare'  : 1,
                      'fare_per_km_after_fixed' : 20.0,
                      'city'       : 'Mumbai',
                      'service_type' : 'Meru Cabs'
                    },
                    {
                      'rule'       : 1,
                      'time_from'  : '23:59',
                      'time_to'    : '05:00',
                      'fixed_fare' : 20,
                      'night'      : True,
                      'dist_km_for_fixed_fare'  : 1,
                      'fare_per_km_after_fixed' : 23.0,
                      'info'       : 'some info',
                      'city'       : 'Mumbai',
                      'service_type' : 'Meru Flexi'


                    },
                    {
                      'rule'       : 1,
                      'time_from'  : '05:00',
                      'time_to'    : '23:59',
                      'fixed_fare' : 10,
                      'night'      : False,
                      'dist_km_for_fixed_fare'  : 1,
                      'fare_per_km_after_fixed' : 23.0,
                      'city'       : 'Mumbai',
                      'service_type' : 'Meru Flexi'
                    }
                ]
        s_rule = self.meru._get_fare_by_distance(self.route)
        self.route.duration = 2 * 3600 # 2 hours
        distance = 100 * 1000 # 100KM
        time = datetime.strptime("02:00", '%H:%M')
        fare = self.meru._calculate_fare(mdata, distance, self.route.duration, 'Mumbai', time)
        # 20 + 99 * 20 = 2000
        self.assertEqual(fare['Meru Cabs']['fare'], 2000)
        # 20 + 99 * 23 = 2297.0
        self.assertEqual(fare['Meru Flexi']['fare'], 2297.0)
        info = self.meru.get_extra_information()
        #self.assertEqual(info['night_charges_used'], True)
        #self.assertEqual(info['other_info'], 'some info')

        self.meru = MeruService()
        # duration at border. but we add 5 minutes so lower one should be
        # charged
        time = datetime.strptime("05:00", '%H:%M')
        fare = self.meru._calculate_fare(mdata, distance, self.route.duration, 'Mumbai', time)
        self.assertEqual(fare['Meru Cabs']['fare'], 1990.0)
        self.assertEqual(fare['Meru Flexi']['fare'], 2287.0)
        info = self.meru.get_extra_information()
        #self.assertEqual(info['night_charges_used'], False)

    def test_get_fare_by_distance(self):
        """Checks that the fare is never {}. Uses real time for journey"""
        s_rule = self.meru._get_fare_by_distance(self.route)
        self.assertEqual(s_rule == {}, False)


