import datetime
import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import networkutil

from . import bs
from . import globalconfig

class HeadlineAddRequest(webapp2.RequestHandler):

    def post(self):
        rawdata = self.request.body
        taskqueue.add(queue_name="default", payload=rawdata, url='/miner/add/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')

class HeadlineAddResponse(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        data = json.loads(self.request.body)

        uuid = data.get('uuid')
        if networkutil.isUuidHandled(uuid):
            message = 'HeadlineAddResponse: %s is already handled.' % (uuid, )
            logging.warn(message)
            self.response.out.write(message)
            return
        networkutil.updateUuids(uuid)

        datasource = data['datasource']
        items = data['items']
        bs.saveItems(datasource, items)
        self.response.out.write('Done.')

class ArchiveRequest(webapp2.RequestHandler):

    def get(self):
        taskqueue.add(queue_name="default", url='/miner/archive/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')

class ArchiveResponse(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        bs.archiveData(globalconfig.getTimezone())
        self.response.out.write('Done.')


def _getWordsServerUrl(timezone):
    urlConfig = globalconfig.getWordsServerUrls()
    key = (datetime.datetime.utcnow() + datetime.timedelta(hours=timezone)).hour
    while True:
        key = str(key)
        if not key in urlConfig:
            return None
        value = urlConfig[key]
        if isinstance(value, basestring):
            return value
        key = value
    return None

class CalculateWords(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        masterUrls = globalconfig.getMasterUrls()
        if not masterUrls:
            logging.warn('Master urls is required.')
            return

        wordsServerUrl = _getWordsServerUrl(globalconfig.getTimezone())
        if not wordsServerUrl:
            logging.warn('Words server urls is required.')
            return
        channels = globalconfig.getChannels()
        bs.calculateHotWords(wordsServerUrl, masterUrls, channels)
        self.response.out.write('Done.')

