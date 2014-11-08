import abc

class BaseService(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
        return

    @abc.abstractmethod
    def get_fare_by_distance(self, distance):
        return

    @abc.abstractmethod
    def get_extra_information(self):
        return

    @abc.abstractmethod
    def get_min_response_time(self):
        return
