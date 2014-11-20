import os,sys
import yaml
import abc


class BaseScraper(object):
    __metaclass__ = abc.ABCMeta
    __keys = yaml.load(open('../data/template.yaml'))
    __required_keys = set(k for k,v in BaseScraper.__keys.items() if v)

    def assertValidService(self, service):
        missing = self.__required_keys.difference(service.keys())
        if missing:
          raise ValueError("Missing required fields: %s" % missing)
        return True

    @abc.abstractmethod
    def scrape_fares(self, **kwargs):
        raise NotImplementedError

    def update(self):
        services = filter(self.assertValidService, self.scrape_fares())

        name = self.__class__.__name__.rstrip('Scraper').lower()
        with open(os.path.join('../data',name)+'.yaml','w') as fh:
            yaml.dump(services,stream=fh,default_flow_style=False)
