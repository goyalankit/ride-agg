from google.appengine.ext import ndb

"""
Data from Uber service.

Fare is fixed for first 8km and is Rs 200, so
fare_fixed_for_km = 8
fixed_fare = 200

service type can be different type of vehicles
or different range.

meru doesn't mention vehicle type.
"""
class UberData(ndb.Model):
    service_type = ndb.StringProperty()
    fare_per_km  = ndb.FloatProperty()
    fare_fixed_for_km   = ndb.FloatProperty()
    fixed_fare = ndb.FloatProperty()
    waiting_charges = ndb.FloatProperty()
    service_tax = ndb.FloatProperty()
    city = ndb.StringProperty()
    from_time = ndb.TimeProperty()
    to_time = ndb.TimeProperty()
