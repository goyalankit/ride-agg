import json
import sys
import re
import urllib
import collections
import cgi
import time
from datetime import datetime
from time import mktime
from bs4 import BeautifulSoup

SDK_PATH = "/usr/local/google_appengine"
sys.path.insert(0, SDK_PATH)
import dev_appserver
dev_appserver.fix_sys_path()

from models.uber import UberData
"""
Meru's webpage is very poorly written and written scrapper
for it is more tedious that manually entering the rates
"""

ag = sys.argv

def populate_data(*ag):
    uber_data = UberData(
                      service_type   = ag[1],
                      fare_per_km = float(ag[2]),
                      fare_fixed_for_km = float(ag[3]),
                      fixed_fare = float(ag[4]),
                      waiting_charges = float(ag[5]),
                      service_tax = float(ag[6]),
                      city = ag[7],
                      from_time = ag[8],
                      to_time = ag[9]
                    )
    uber_data.put()


#python -m scripts.meru_scrapper "Meru Cabs" 20.0 1.0 27.0 2.0 4.94 "Mumbai"
populate_data("dummy","Meru Cabs", 20.0, 1.0, 27.0, 2.0, 4.94, "Mumbai", "5:00AM", "midnight")
