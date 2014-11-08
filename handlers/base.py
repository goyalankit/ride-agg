import webapp2
import json
import jinja2
import os

import logging

log = logging.getLogger(__name__)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader((os.path.dirname(__file__) + '/../templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    """BaseHandler which will be inherited all other handlers 
    it should implement the most common functionality
    required by all handlers
    """

    def __init__(self, request, response):
	self.initialize(request, response)

    def render_response(self, _template, context):
        rv = JINJA_ENVIRONMENT.get_template(_template).render(context)
	self.response.write(rv)

    def render_json(self, obj):
	rv = json.dumps(obj)
	self.response.headers.content_type = 'application/json'
	self.response.write(rv)


