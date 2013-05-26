import datetime
import logging
import time

from commonutil import collectionutil, dateutil, networkutil
from . import models

_URL_TIMEOUT = 30
_CALLBACK_TRYCOUNT = 3
_REQUEST_INTERVAL = 5

def saveItems(datasource, items):
    models.saveDatasource(datasource, items)

def archiveData(timezone):
    nnow = datetime.datetime.utcnow()
    lend = datetime.datetime(nnow.year, nnow.month, nnow.day, 23, 59, 0)
    nend = lend - datetime.timedelta(hours=timezone)
    if nend > nnow:
        lend -= datetime.timedelta(days=1)
        nend -= datetime.timedelta(days=1)
    topnend = nend
    datasources = models.getDatasourceHistory()
    leftSources = datasources
    while True:
        strend = dateutil.getDateAs14(nend)
        leftSources = [item for item in leftSources
                    if 'added' in item and item['added'] <= strend]
        if not leftSources:
            break
        nend2 = nend - datetime.timedelta(days=1)
        strend2 = dateutil.getDateAs14(nend2)
        matchedSources = [item for item in leftSources
                    if 'added' in item and item['added'] > strend2]
        if matchedSources:
            models.archiveData(lend.strftime('%Y%m%d'), matchedSources)
        lend -= datetime.timedelta(days=1)
        nend -= datetime.timedelta(days=1)
    strtopend = dateutil.getDateAs14(topnend)
    datasources = [item for item in datasources
                    if 'added' in item and item['added'] > strtopend]
    models.saveDatasourceHistory(datasources)

def _isPageMatched(pageTags, tags):
    matched = False
    for tag in tags:
        if collectionutil.fullContains(pageTags, tag.split('+')):
            matched = True
            break
    return matched

def getPagesByTags(pages, tags, returnMatched=True):
    result = []
    for page in pages:
        pageTags = page['source']['tags']
        matched = _isPageMatched(pageTags, tags)
        if (returnMatched and matched) or (not returnMatched and not matched):
            result.append(page)
    return result

def _sendHotWordsRequest(serverUrl, masterUrls, masterKeyname, pages):
    if not pages:
        logging.warn('No pages is available for %s' % (masterKeyname, ))
        return
    titles = [ page['title'] for page in pages if page.get('title') ]
    data = {
        'masters': masterUrls,
        'key': masterKeyname,
        'titles': titles,
    }
    success = networkutil.postData(serverUrl, data, tag=masterKeyname,
                trycount=_CALLBACK_TRYCOUNT, timeout=_URL_TIMEOUT)
    if success:
        message = 'Send words request for %s successfully.' % (masterKeyname, )
    else:
        message = 'Failed to send words request for %s.' % (masterKeyname, )
    logging.info(message)

def calculateHotWords(wordsServerUrl, masterUrls, channels):
    sitePages = models.getPages(keyname='sites')
    _sendHotWordsRequest(wordsServerUrl, masterUrls, 'sites', sitePages)

    chartsPages = models.getPages(keyname='chartses')
    time.sleep(_REQUEST_INTERVAL)
    _sendHotWordsRequest(wordsServerUrl, masterUrls, 'chartses', chartsPages)

    channelsWords = {}
    for channel in channels:
        slug = channel.get('slug')
        if not slug:
            continue
        tags = channel.get('tags')
        if not tags:
            continue
        channelPages = getPagesByTags(sitePages, tags)
        if not channelPages:
            continue
        time.sleep(_REQUEST_INTERVAL)
        _sendHotWordsRequest(wordsServerUrl, masterUrls, slug, channelPages)

