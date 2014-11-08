import abc

class BaseService(object):
    __metaclass__ = abc.ABCMeta

    @abstractproperty
    def name(self):
        """Return the name of the API implementing
        the method.
        """
        return

    @abstractproperty
    def has_api(self):
        """Return True if an API is present for
        the service implementing the method. Else
        return False.
        """
        return

    @abc.abstractmethod
    def get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
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
