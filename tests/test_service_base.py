import abc
import unittest
import json
from models.route import Route

class ServiceTester(unittest.TestCase):
    __metaclass__ = abc.ABCMeta

    """
    Check that the distance calculation is not off by much
    """
    @abc.abstractproperty
    def service(self):
        """ Return the service class """

    @staticmethod
    def get_route():
        route_s = open('tests/data/route.json', 'r')
        route_j = json.load(route_s)
        route = Route()
        route.json2Obj(route_j)
        return route

    def setUp(self):
        self.route = self.get_route()
        self.serviceInstance = self.service()

    def __getattr__(self,attr):
        """
        python goes here when an attribute can't be found - so this effectively
        defers all unknown attributes to the service being tested
        """
        return getattr(self.serviceInstance,attr)
