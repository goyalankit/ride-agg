import unittest
import webapp2
import json
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from models.route import Route
import libs.helper_functions as helper_functions

class TestHelperFunctions(unittest.TestCase):

    def get_route(self):
        route_s = open('tests/data/route.json', 'r')
        route_j = json.load(route_s)
        route = Route()
        route.json2Obj(route_j)
        return route

    def setUp(self):
        self.route = self.get_route()

    def test_find_city_when_present(self):
        """Returns the city when present in cities from meru data"""
        city = helper_functions.find_city([{'city' : 'muMBai'}], self.route)
        self.assertEqual('Mumbai', city.capitalize())

        self.route.start_address = "some place in gurgaon"
        city = helper_functions.find_city([{'city' : 'mumbai'}], self.route)
        self.assertEqual(city, "Delhi")

