import copy
import datetime


from commonutil import dateutil
import configmanager.models
from configmanager import cmapi

class DatasourceHistory(configmanager.models.ConfigItem):
    pass

class DatasourceArchive(configmanager.models.ConfigItem):
    pass

cmapi.registerModel(DatasourceHistory)
cmapi.registerModel(DatasourceArchive)

def _getDatasourceHistoryKey():
    return 'list'

def getDatasourceHistory():
    key = _getDatasourceHistoryKey()
    items = cmapi.getItemValue(key, [], modelname=DatasourceHistory)
    return items

def saveDatasourceHistory(datasourceHistory):
    key = _getDatasourceHistoryKey()
    cmapi.saveItem(key, datasourceHistory, modelname=DatasourceHistory)

def saveDatasource(datasource, items):
    data = copy.deepcopy(datasource)
    data['pages'] = copy.deepcopy(items)

    key = _getDatasourceHistoryKey()
    latestItems = getDatasourceHistory()
    latestItems.insert(0, data)
    cmapi.saveItem(key, latestItems, modelname=DatasourceHistory)

def getArchiveConfig():
    return cmapi.getItemValue('archive', {})

def archiveData(key, datasources):
    cmapi.saveItem(key, datasources, modelname=DatasourceArchive)

