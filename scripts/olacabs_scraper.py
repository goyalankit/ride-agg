import re
import urllib
from bs4 import BeautifulSoup
import httplib

numparse = lambda x: map(float,re.findall(r'\d+\.?\d*',x))

class OlacabsScraper(BaseScraper):

    @staticmethod
    def map_to_template(service):
        if not isinstance(service,dict) and hasattr(service,'__iter__'):
            return map(OlacabsScraper.map_to_template, service)

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

    # TODO
    # add extra charges information
    @staticmethod
    def scrape_fares(cities=None):
        conn = httplib.HTTPConnection("www.olacabs.com")

        if cities is None:
            conn.request("GET", "/fares")
            soup = BeautifulSoup(conn.getresponse().read())
            cityOptions = soup.find('div',attrs={'id':"faresCityList"})
            cities = list(cityOptions.stripped_strings)
        elif not hasattr(cities,'__iter__'):
            cities = [cities]

        # fare-table contains extra information if we need it later
        # fareTables = soup.find_all('div',attrs={'class':"fare-table"})

        services = []
        format = lambda x: re.sub('\s','_', x.get_text().lower().split('(')[0])
        for city in cities:
            conn.request("GET", "/fares" + '/' + city.lower())

            svc = {}
            soup = BeautifulSoup(conn.getresponse().read())
            for svctype in ('standard-rate', 'luxury-rate'):
                tablesoup = soup.find('div',attrs={'class':['fare-table',svctype]})
                headers = tablesoup.find_all('th')
                headers = map(format, headers[1:])
                cols = [val.get_text() for val in tablesoup.find_all('td')]

                svc = dict(zip(headers,cols))
                svc['city'] = city
                svc['service_type'] = svctype
                services.append(OlacabsScraper.map_to_template(svc))

        return services
