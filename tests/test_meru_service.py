import unittest
import webapp2
import os
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from libs.meru_service import MeruService

class TestMeruService(unittest.TestCase):
    """
    Check that the distance calculation is not off by much
    """
    def setUp(self):
        self.meru = MeruService()

    """
    Simple test case to check that we are able to load and
    parse meru.yaml file
    """
    def test_load_data(self):
        data = self.meru.load_data()
        self.assertEqual(data.get('meru') == None, False)
        self.assertEqual(data.get('meru').get('mumbai') == None, False)

    def test_get_fare_by_distance(self):
        self.meru.get_fare_by_distance(23)

