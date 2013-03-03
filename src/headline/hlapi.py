import datetime
import logging

from commonutil import dateutil
import globalconfig
from . import modelapi

def saveItems(datasource, items):
    modelapi.saveDatasource(datasource, items)

def getDatasourceHistory():
    latestHours = globalconfig.getSiteLatestHours()
    startTime = datetime.datetime.utcnow() - datetime.timedelta(hours=latestHours)
    strstart = dateutil.getDateAs14(startTime)
    datasources = modelapi.getDatasourceHistory()
    result = [ item for item in datasources
                if item.get('added', '') >= strstart]
    if not result:
        result = datasources[:100]
    return result

def archiveData():
    config = modelapi.getArchiveConfig()
    timezone = config.get('tiemzone', 0)
    nnow = datetime.datetime.utcnow()
    lend = datetime.datetime(nnow.year, nnow.month, nnow.day, 23, 59, 0)
    nend = lend - datetime.timedelta(hours=timezone)
    if nend > nnow:
        lend -= datetime.timedelta(days=1)
        nend -= datetime.timedelta(days=1)
    topnend = nend
    datasources = modelapi.getDatasourceHistory()
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
            modelapi.archiveData(lend.strftime('%Y%m%d'), matchedSources)
        lend -= datetime.timedelta(days=1)
        nend -= datetime.timedelta(days=1)
    strtopend = dateutil.getDateAs14(topnend)
    datasources = [item for item in datasources
                    if 'added' in item and item['added'] > strtopend]
    modelapi.saveDatasourceHistory(datasources)

