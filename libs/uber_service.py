import webapp2
from base_service import BaseService
import requests

class UberService(BaseService):

    # TODO(goyalankit) add error handling code
    def make_request(self, url_type, parameters):
        config = webapp2.get_app().config.get('uber')
        parameters.update({ 'server_token': config.get('server_token')})
        response = requests.get(config.get(url_type), params=parameters)
        return response.json()

    def name(self):
        return "Uber"

    def has_api(self):
        return True

    def get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
        return 12

    def get_fare_by_distance(self, distance):
        params = {
                'latitude': 37.775818,
                'longitude': -122.418028
        }

        result = self.make_request("products_url", params)
        return result

    def get_extra_information(self):
        #self.make_request("product_url", {"col": "yeh"})
        return 43

    def get_min_response_time(self):
        return 23
