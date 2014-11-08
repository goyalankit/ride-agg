from base_service import BaseService

class UberService(BaseService):

    def get_fare_by_lat_lang(self, src_lat, src_long,
            dst_lat, dst_long):
        return 12

    def get_fare_by_distance(self, distance):
        return 32

    def get_extra_information(self):
        return 43

    def get_min_response_time(self):
        return 23
