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
        return {}



