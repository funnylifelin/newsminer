
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
    # charts refresh operation does not need archive.
    if 'refreshing' in datasource:
        return

    sourceadded = datasource.get('added')
    if not sourceadded:
        return
    key = _getDatasourceHistoryKey()
    latestItems = getDatasourceHistory()
    for item in items:
        # An item only need archive the first time it appears.
        itemadded = item.get('added')
        if not itemadded:
            continue
        if itemadded < sourceadded:
            continue

        item['source'] = datasource
        latestItems.insert(0, item)
    cmapi.saveItem(key, latestItems, modelname=DatasourceHistory)

def getArchiveConfig():
    return cmapi.getItemValue('archive', {})

def archiveData(key, datasources):
    oldValue = cmapi.getItemValue(key, [], modelname=DatasourceArchive)
    if oldValue:
        oldValue.extend(datasources)
    else:
        oldValue = datasources
    cmapi.saveItem(key, oldValue, modelname=DatasourceArchive)

