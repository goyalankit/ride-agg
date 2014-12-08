import os,sys
import yaml
import abc
import config

dpath = config.app_config.get('template').get('data_file')
with open(dpath,'r') as dfile:
    template = yaml.load(dfile)
required_keys = set(k for k,v in template.items() if v)

class BaseScraper(object):
    __metaclass__ = abc.ABCMeta

    @property
    def name(self):
        return self.__class__.__name__.split('Scraper')[0]

    @property
    def save_path(self):
        """ where to save data file """
        return config.app_config.get(self.name.lower()).get('data_file')

    @classmethod
    def assertValidService(cls, service):
        if not service:
          return True

        missing = required_keys.difference(service.keys())
        if missing:
          raise ValueError("Missing required fields: %s" % missing)
        return True

    @abc.abstractmethod
    def scrape_fares(self):
        raise NotImplementedError

    def update(self):
        services = filter(self.assertValidService, self.scrape_fares())

        with open(self.save_path, 'w') as fh:
            yaml.dump(services,stream=fh,default_flow_style=False)
