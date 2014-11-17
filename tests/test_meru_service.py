import unittest
import webapp2
import os
import json
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from libs.meru_service import MeruService
from models.route import Route

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
        self.assertEqual(data.get('meru') == None, False)
        self.assertEqual(data.get('meru').get('mumbai') == None, False)

    def test_find_city_when_present(self):
        """Returns the city when present in cities from meru data"""
        city = self.meru.find_city(self.meru.load_data().get('meru'), self.route)
        self.assertEqual('mumbai', city)

    def test_find_city_when_not_present(self):
        """Returns None when city is not present"""
        route_temp = Route()
        route_temp.start_address = "i live in austin"
        city_n_p = self.meru.find_city(self.meru.load_data().get('meru'), route_temp)
        self.assertEqual(None, city_n_p)

    def test_get_fare_by_distance(self):
        """Checks that the fare is calculated correctly"""
        self.meru.get_fare_by_distance(self.route)



