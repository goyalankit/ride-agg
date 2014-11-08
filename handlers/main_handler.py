import logging

log = logging.getLogger(__name__)

from base import BaseHandler
from uber_service import UberService

class MainHandler(BaseHandler):
    def get(self):
	config = self.app.config
        uber = UberService()
        uber.get_extra_information()
        template_values = {}
        template_values["hello"] = uber.get_min_response_time()
        self.render_response('default.html',template_values)

class IndexHandler(BaseHandler):
    def get(self):
        template_values = {}
        template_values["hello"] = "hello"
        self.render_response('index.html',template_values)


