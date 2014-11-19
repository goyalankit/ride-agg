import re
import urllib
from bs4 import BeautifulSoup


class OlacabsScraper(BaseScraper):

    def standardize_service(self, service):
        if hasattr(service,'__iter__') and not isinstance(service,dict):
            return map(self.standardize_service,service)

        num = lambda x: map(str,re.findall(r'\d+\.?\d*',x))

        std_svc = {}
        std_svc['currency_code'] = u'IND'

        std_svc['city'] = service['city']
        std_svc['service_type'] = unicode(service['service_type'].rstrip('-rate'))
        std_svc['vehicle_type'] = unicode(service['category'])

        min_bill = num(service['minimum_bill'])
        std_svc['fixed_fare'] = min_bill[0]
        if len(min_bill)>1:
          std_svc['fixed_fare_km'] = min_bill[1]

        std_svc['fare_per_km'] = num(service['extra_km_charges'])[0]

        # will have to differentiate these two at some point
        # so that we can display it correctly
        if 'wait_time_charges' in service:  key = 'wait_time_charges'
        else:                               key = 'ride_time_charges'
        std_svc['wait_charge_per_min'] = num(service[key])[0]

        return std_svc

    def scrape_fares(self, cities=None):
        if cities is None:
            soup = BeautifulSoup(urllib.urlopen('http://www.olacabs.com/fares'))
            cityOptions = soup.find('div',attrs={'id':"faresCityList"})
            cities = list(cityOptions.stripped_strings)
        elif not hasattr(cities,'__iter__'):
            cities = [cities]

        # fare-table contains extra information if we need it later
        # fareTables = soup.find_all('div',attrs={'class':"fare-table"})

        services = []
        format = lambda x: re.sub('\s','_', x.get_text().lower().split('(')[0])
        for city in cities:
            svc = {}
            link = os.path.join('http://www.olacabs.com/fares',city.lower())
            soup = BeautifulSoup(urllib.urlopen(link))
            for svctype in ('standard-rate', 'luxury-rate'):
                tablesoup = soup.find('div',attrs={'class':['fare-table',svctype]})
                headers = tablesoup.find_all('th')
                headers = map(format, headers[1:])
                cols = [val.get_text() for val in tablesoup.find_all('td')]

                svc = dict(zip(headers,cols))
                svc['city'] = city
                svc['service_type'] = svctype
                services.append(self.standardize_service(svc))

        return services
