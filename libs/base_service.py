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

    @abc.abstractmethod
    def get_fare_by_lat_lang(self, src_lat, src_long, dst_lat, dst_long):
        """Returns fare if latitude and longitude of
        source and destination are given."""
        return

    @abc.abstractmethod
    def get_fare_by_distance(self, distance):
        """Returns fare if the total distance
        is given between source and destination
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
