import logging

log = logging.getLogger(__name__)

from base import BaseHandler

class MainHandler(BaseHandler):
    def get(self):
	config = self.app.config
        template_values = {}
        template_values["hello"] = "hello"
        self.render_response('default.html',template_values)

class IndexHandler(BaseHandler):
    def get(self)
        template_values = {}
        template_values["hello"] = "hello"
        self.render_response('index.html',template_values)


