import os,sys
import yaml
import abc
# import config

# template = yaml.load(config.app_config.get('template')['data_file'])
template = yaml.load(open('../data/template.yaml'))
required_keys = set(k for k,v in template.items() if v)

class BaseScraper(object):
    __metaclass__ = abc.ABCMeta

    @property
    def name(self):
        return self.__class__.__name__.rstrip('Scraper').lower()

    @property
    def save_path(self):
        """ where to save data file """
        # return config.app_config.get(cls.name)['data_file']
        return os.path.join('../data', self.name+'.yaml')

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
