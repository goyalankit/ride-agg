import unittest
import webapp2
import os
import json
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from libs.olacabs_service import OlacabsService
from models.route import Route
import libs.helper_functions as helper_functions

class TestOlacabsService(unittest.TestCase):

    # TODO(goyalankit) move this method to common module
    def get_route(self):
        route_s = open('tests/data/route.json', 'r')
        route_j = json.load(route_s)
        route = Route()
        route.json2Obj(route_j)
        return route

    def setUp(self):
        self.olacab = OlacabsService()
        self.route  = self.get_route()

    def test_name(self):
        self.assertEqual(self.olacab.name, "olacabs")
