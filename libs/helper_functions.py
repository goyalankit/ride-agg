#
# Generic helper functions
#

"""
Get the unique value for a given list
"""
def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

"""
Try to match a city from available cities in service data to the city in the source
address.
"""
def find_city(mdata, route):
    cities = [record['city'].lower() for record in mdata]
    start_address = route.start_address.lower()

    city = [city for city in cities if city in start_address]
    return (city[0] if city else None)

