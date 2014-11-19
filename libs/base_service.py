import abc
import math

class BaseService:
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        """Return the name of the API implementing
        the method.
        """
        return

    @abc.abstractproperty
    def has_api(self):
        """Return True if an API is present for
        the service implementing the method. Else
        return False.
        """
        return

    def get_fare(self, route):
        """
        Method used to get fare information for a given service.
        This method internally calls private methods _get_fare_by_distance
        or _get_fare_by_lat_long based on implementation.
        """
        return

    @abc.abstractmethod
    def _get_fare_by_lat_lang(self, src_lat, src_long, dst_lat, dst_long):
        """Returns fare if latitude and longitude of
        source and destination are given.
        This is a private method called by get_fare
        """
        return

    @abc.abstractmethod
    def _get_fare_by_distance(self, route):
        """Returns fare if the total distance
        is given between source and destination
        This is a private method called by get_fare
        """
        return

    @abc.abstractmethod
    def get_extra_information(self):
        """Any other information related to a
        particular service implementing the method
        """
        return

    @abc.abstractmethod
    def get_min_response_time(self):
        """If available give minimum response time.
        Otherwise return -1
        """
        return

    """
    Try to match a city from available cities in meru data in the source
    address.
    """
    def find_city(self, mdata, route):
        meru_cities = mdata.keys()
        start_address = route.start_address.lower()

        city = [city for city in meru_cities if city in start_address]
        return (city[0] if city else None)


    def calculate_distance(self, src_lat, src_long, dst_lat, dst_long):
        """Method to calculate Distance between two sets of Lat/Lon."""
        earth = 6371 #Earth's Radius in Kms.

        #Calculate Distance based in Haversine Formula
        dlat = math.radians(dst_lat-src_lat)
        dlon = math.radians(dst_long-src_long)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(src_lat)) * math.cos(math.radians(dst_lat)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = earth * c
        return d
