#
# Generic helper functions
#
import datetime 
from operator import itemgetter
from itertools import imap


cities_near_by = {
            "Bangalore" : ["bengaluru", "bangalore"],
            "Delhi" : ["gurgaon", "noida", "delhi"]
        }

"""
Get the unique value for a given list
"""
def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    # return set(seq)?

"""
Try to match a city from available cities in service data to the city in the source
address.
"""
def find_city(mdata, route):
    start_address = route.start_address.lower()

    for city in imap(itemgetter('city'), mdata):
        if city.lower() in start_address: return city

    for main_city in cities_near_by:
        for city in cities_near_by.get(main_city, []):
            if city.lower() in start_address:
                return main_city

    return None

def sub_time(time1, time2):
    time1_in_minutes = time1.hour * 60 + time1.minute
    time2_in_minutes = time2.hour * 60 + time2.minute
    diff = time1_in_minutes - time2_in_minutes
    hours = diff / 60
    minutes  = diff % 60
    return datetime.time(hours, minutes)

"""
Get a dictionary representation of a generic object's attributes+attribute values
(really useful 
"""
def dump(obj):
    return dict((attr,getattr(obj,attr)) for attr in dir(obj)
                if not attr.startswith('_') and not callable(getattr(obj,attr)))
