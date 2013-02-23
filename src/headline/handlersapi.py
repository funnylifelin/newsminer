import logging

from google.appengine.api import taskqueue

import webapp2

import jsonpickle

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
        data = jsonpickle.decode(self.request.body)

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

class HeadlineCleanRequest(webapp2.RequestHandler):

    def get(self):
        taskqueue.add(queue_name="default", url='/headline/clean/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')

class HeadlineCleanResponse(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        hlapi.cleanData()
        self.response.out.write('Done.')

