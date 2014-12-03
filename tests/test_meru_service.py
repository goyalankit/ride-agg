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
                    {'rule' : 1, 'time_from' : '23:00', 'time_to' : '05:00'},
                    {'rule' : 2, 'time_from' : '05:00', 'time_to' : '23:00'},
                ]

        # greater than all bounds
        time_to_check = datetime.strptime("23:50", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(s_rule, rules[0])

        # between the bound of day time
        time_to_check = datetime.strptime("05:50", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(s_rule, rules[1])

        # smaller than all the bounds
        time_to_check = datetime.strptime("03:00", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(s_rule, rules[0])

    def test_rule_for_given_time_for_day(self):
        rules = [
                    {'rule' : 1, 'time_from' : '23:59', 'time_to' : '05:00'},
                    {'rule' : 2, 'time_from' : '05:00', 'time_to' : '23:59'},
                ]
        time_to_check = datetime.strptime("00:00", '%H:%M')
        s_rule = self.meru.get_rule_for_given_time(rules, time_to_check)
        self.assertEqual(s_rule, rules[0])



    def test_get_fare_by_distance(self):
        """Checks that the fare is calculated correctly"""
#        s_rule = self.meru._get_fare_by_distance(self.route)
        pass



