import re
import urllib
from bs4 import BeautifulSoup
import httplib
from itertools import imap,ifilter

numparse = lambda x: map(float,re.findall(r'\d+\.?\d*',x))

class OlacabsScraper(BaseScraper):
    service_types = ("standard-rate","luxury-rate")
    _table_types = map(lambda s: s+" fare-table", service_types)

    @classmethod
    def map_to_template(cls, service):
        if not isinstance(service,dict) and hasattr(service,'__iter__'):
            return imap(cls.map_to_template, service)

        std_svc = {}
        std_svc['currency_code'] = u'IND'
        std_svc['city'] = unicode(service['city'])
        std_svc['service_type'] = unicode(service['service_type'].rstrip('-rate').capitalize())
        std_svc['vehicle_type'] = unicode(service['category'])

        min_bill = numparse(service['minimum_bill'])
        std_svc['fixed_fare_per_km'] = min_bill[0]
        if len(min_bill)>1:
          std_svc['fixed_fare_dist_km'] = min_bill[1]
        std_svc['fare_per_km'] = numparse(service['extra_km_charges'])[0]

        if 'wait_time_charges' in service:
            std_svc['wait_charge_per_min'] = numparse(service['wait_time_charges'])[0]

        if 'ride_time_charges' in service:
            std_svc['fare_per_min'] = numparse(service['ride_time_charges'])[0]

        return std_svc

    @staticmethod
    def get_cities(conn=None):
        if conn is None:
            conn = httplib.HTTPConnection("www.olacabs.com")
        conn.request("GET", "/fares")
        soup = BeautifulSoup(conn.getresponse().read())
        cities = soup.find('div',attrs={'id':"faresCityList"})

        return cities.stripped_strings

    # TODO
    # add extra charges information
    @classmethod
    def scrape_fares(cls, cities=None):
        conn = httplib.HTTPConnection("www.olacabs.com")


        if cities is None:
            cities = cls.get_cities(conn)
        elif not hasattr(cities,'__iter__'):
            cities = [cities]

        format = lambda x: re.sub('\s','_', x.get_text().lower().split('(')[0])

        for city in cities:
            conn.request("GET", "/fares" + '/' + city.lower())

            soup = BeautifulSoup(conn.getresponse().read())
            tables = imap(lambda x: soup.find('div', class_=x), cls._table_types)
            for i,tablesoup in enumerate(ifilter(None,tables)):
                soup_ptr = tablesoup.find('tr')
                if not soup_ptr: continue

                ncols = int(soup_ptr.th['colspan'])
                soup_ptr = soup_ptr.find_next('tr')
                headers = map(format, soup_ptr.find_all('th'))
                
                content = tablesoup.find_all('td')
                nrows = len(content)/ncols
                for cols in (content[i*ncols:(i+1)*ncols] for i in range(nrows)):
                    svc = dict(zip(headers, [c.get_text() for c in cols]))
                    svc['city'] = city
                    svc['service_type'] = cls.service_types[i]
                    yield cls.map_to_template(svc)
