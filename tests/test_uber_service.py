import unittest
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from libs.uber_service import UberService

class TestUberService(unittest.TestCase):
    """
    Check that the distance calculation is not off by much
    """
    def setUp(self):
        self.uber = UberService()

    def test_calculate_distance(self):
        dst = self.uber.calculate_distance(30.299353, -97.720759, 30.283679, -97.732582)
        self.assertEqual(abs(2.07995170808 - dst) < 0.5, True)
