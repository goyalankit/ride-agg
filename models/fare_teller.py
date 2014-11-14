from libs.uber_service import UberService

class FareTeller:

    # all these services will be used to
    # fetch results
    services = [
            UberService
        ]

    def __init__(self, _route):
        self.route = _route

    def get_fares(self):
        fares = {}
        for service in FareTeller.services:
            s_l = self.route.start_location
            e_l = self.route.end_location
            service_obj = service()
            if service_obj.has_api:
                fares[service_obj.name] = service_obj.get_fare_by_lat_lang(
                        s_l['lat'], s_l['lon'], e_l['lat'], e_l['lon'])

        return fares



