import datetime

from commonutil import dateutil
import globalconfig
from . import modelapi

def saveItems(datasource, items):
    modelapi.saveDatasourceHistory(datasource, items)

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

