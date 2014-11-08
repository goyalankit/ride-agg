
import logging

log = logging.getLogger(__name__)

from base import BaseHandler

class HelloHandler(BaseHandler):
    def get(self):
	config = self.app.config
	self.render_response('hello.html')


class DefaultHandler(BaseHandler):
    def get(self):
	config = self.app.config
        template_values = {}
        template_values["cool"] = "hello"
        self.render_response('default.html',template_values)
