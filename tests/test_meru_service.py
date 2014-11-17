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

        # mock the get path method
        def mock_get_path(self):
            return os.path.abspath('data/meru.yaml')
        self.orig_get_path = MeruService.get_path
        MeruService.get_path = mock_get_path

    def tearDown(self):
        # unmock the get path method
        MeruService.get_path = self.orig_get_path



    """
    Simple test case to check that we are able to load and
    parse meru.yaml file
    """
    def test_load_data(self):
        data = self.meru.load_data()
        self.assertEqual(data.get('meru') == None, False)
        self.assertEqual(data.get('meru').get('mumbai') == None, False)

    """
    This method is to test the stub of get_path method used in
    other tests.
    """
    def test_get_path_stub(self):
        def mock_get_path(self):
            return "some random string"
        orig_get_path = MeruService.get_path
        try:
            MeruService.get_path = mock_get_path
            meru_obj = MeruService()
            self.assertEqual(meru_obj.get_path(), "some random string")
        finally:
            MeruService.get_path = orig_get_path

    def test_get_fare_by_distance(self):
        self.meru.get_fare_by_distance(23)

