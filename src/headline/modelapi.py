import copy
import datetime


from commonutil import dateutil
import configmanager.models
from configmanager import cmapi

class DatasourceHistory(configmanager.models.ConfigItem):
    pass

cmapi.registerModel(DatasourceHistory)

def _getDatasourceHistoryKey():
    return 'list'

def getDatasourceHistory():
    key = _getDatasourceHistoryKey()
    items = cmapi.getItemValue(key, [], modelname=DatasourceHistory)
    return items

def saveDatasourceHistory(datasource, items):
    data = copy.deepcopy(datasource)
    data['pages'] = copy.deepcopy(items)

    key = _getDatasourceHistoryKey()
    latestItems = getDatasourceHistory()
    latestItems.insert(0, data)
    cmapi.saveItem(key, latestItems, modelname=DatasourceHistory)

