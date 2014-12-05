from libs.uber_service import UberService
from libs.meru_service import MeruService
from libs.olacabs_service import OlacabsService

class FareTeller:

    # all these services will be used to
    # fetch results
    services = [
            UberService,
            OlacabsService,
            MeruService
        ]

    def __init__(self, _route):
        self.route = _route

    def get_fares(self):
        fares = {}
        for service in FareTeller.services:
            service_obj = service()
            fares[service_obj.name] = service_obj.get_fare(self.route)
        return fares



