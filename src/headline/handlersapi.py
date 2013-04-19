import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import networkutil

from . import hlapi

class HeadlineAddRequest(webapp2.RequestHandler):

    def post(self):
        rawdata = self.request.body
        taskqueue.add(queue_name="default", payload=rawdata, url='/headline/add/')
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
        hlapi.saveItems(datasource, items)
        self.response.out.write('Done.')

class ArchiveRequest(webapp2.RequestHandler):

    def get(self):
        taskqueue.add(queue_name="default", url='/headline/archive/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')

class ArchiveResponse(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        hlapi.archiveData()
        self.response.out.write('Done.')

