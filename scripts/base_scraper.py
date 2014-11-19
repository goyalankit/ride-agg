import os,sys
import yaml
import abc

class BaseScraper(object):
    __metaclass__ = abc.ABCMeta
    __keys = yaml.load(open('../data/template.yaml'))

    @staticmethod
    def assertValidService(service):
        required_fields = set(k for k,v in BaseScraper.__keys.items() if v)
        missing = required_fields - set(service.keys())
        if missing:
          raise ValueError("Missing required fields: %s" % missing)

    @abc.abstractmethod
    def scrape_fares(self, **kwargs):
        return NotImplemented

    def update(self):
        services = []
        for svc in self.scrape_fares():
            self.assertValidService(svc)
            services.append(svc)
`
        name = self.__class__.__name__.rstrip('Scraper').lower()
        with open(os.path.join('../data',name)+'.yaml','w') as fh:
            yaml.dump(services,stream=fh,default_flow_style=False)
