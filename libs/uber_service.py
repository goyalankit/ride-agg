import json
import urllib
import webapp2
from base_service import BaseService
from google.appengine.api import urlfetch

class UberService(BaseService):

    """
    Method to make request to Uber Servers using their API. This method
    autofills the server token and gets the url based on the url_type defined
    in config.py
    Possible url types: products_url, time_url, products_url

    Returns: status code and parsed json response
    """
    # TODO(goyalankit) add error handling code
    def make_request(self, url_type, parameters):
        config = webapp2.get_app().config.get('uber')
        parameters.update({ 'server_token': config.get('server_token')})
        url_with_params = config.get(url_type) + '?' + urllib.urlencode(parameters)
        response = urlfetch.fetch(url_with_params, method=urlfetch.GET)
        json_response = json.loads(response.content)
        return response.status_code, json_response

    @property
    def name(self):
        return "Uber"

    @property
    def has_api(self):
        return True

    def get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
        params = {
                'start_latitude': src_lat,
                'start_longitude': src_long,
                'end_latitude': dst_lat,
                'end_longitude': dst_long
                }

        status, result = self.make_request("price_url", params)
        return result

    def get_fare_by_distance(self, distance):
        raise NotImplementedError("Method not supported by this service")

    """
    This is a method reserved for future use. Just in case we want to pass
    some extra information for any service.

    Return: Empty hash implies no extra information available
    """
    def get_extra_information(self):
        return {}

    """
    Only available for uber api. Not implemented yet (depends if we'd want to
    display it on the UI.)
    """
    def get_min_response_time(self):
        raise NotImplementedError("Subclasses should implement this!")
