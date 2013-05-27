import webapp2
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))

import templateutil.filters

import miner.handlersapi
import miner.handlers

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

config = {}
config['webapp2_extras.jinja2'] = {
    'template_path': os.path.join(os.path.dirname(__file__), 'miner', 'templates'),
    'filters': {
        'utc14duration': templateutil.filters.utc14duration
    },
    'environment_args': {
        'extensions': ['jinja2.ext.loopcontrols'],
    },
}

app = webapp2.WSGIApplication([
('/', MainPage),
('/api/miner/add/', miner.handlersapi.HeadlineAddRequest),
('/miner/add/', miner.handlersapi.HeadlineAddResponse),
('/api/miner/archive/', miner.handlersapi.ArchiveRequest),
('/miner/archive/', miner.handlersapi.ArchiveResponse),
('/miner/words/', miner.handlersapi.CalculateWords),
('/miner/words/response/', miner.handlersapi.CalculateWordsResponse),
('/miner/l/', miner.handlers.IndexPage),
],
debug=True, config=config)

