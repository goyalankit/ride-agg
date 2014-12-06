import logging
import json

log = logging.getLogger(__name__)

from base import BaseHandler
from models.route import Route
from models.fare_teller import FareTeller

class MainHandler(BaseHandler):
    def get(self):
	config = self.app.config
        template_values = {}
        self.render_response('default.html',template_values)

    def post(self):
        if not self.request.get('data'):
            self.render_json({error: 'data not present'})
            return
        data = self.request.get('data')
        # TODO(goyalankit) check if we need to handle
        # more than 1 data elements
        first_data  = json.loads(data)[0]
        route       = Route(first_data)
        fare_teller = FareTeller(route)
        fares = fare_teller.get_fares()
        self.render_json({'fares' : fares})

class IndexHandler(BaseHandler):
    def get(self):
        template_values = {}
        template_values["hello"] = "hello"
        self.render_response('index.html',template_values)

