from commonutil import dateutil
import configmanager.models
from configmanager import cmapi

class DatasourceHistory(configmanager.models.ConfigItem):
    pass

class DatasourceArchive(configmanager.models.ConfigItem):
    pass

class LatestItem(configmanager.models.ConfigItem):
    pass

cmapi.registerModel(DatasourceHistory)
cmapi.registerModel(DatasourceArchive)
cmapi.registerModel(LatestItem)

def _getDatasourceHistoryKey():
    return 'list'

def getDatasourceHistory():
    key = _getDatasourceHistoryKey()
    items = cmapi.getItemValue(key, [], modelname=DatasourceHistory)
    return items

def saveDatasourceHistory(datasourceHistory):
    key = _getDatasourceHistoryKey()
    cmapi.saveItem(key, datasourceHistory, modelname=DatasourceHistory)

def _saveHistory(datasource, items):
    sourceadded = datasource.get('added')
    if not sourceadded:
        return
    key = _getDatasourceHistoryKey()
    latestItems = getDatasourceHistory()
    for item in items:
        itemadded = item.get('added')
        if not itemadded:
            continue
        # An item only need archive the first time it appears.
        if itemadded < sourceadded:
            continue
        item['source'] = datasource
        latestItems.insert(0, item)
    latestItems.sort(key=lambda item: item.get('added'), reverse=True)
    cmapi.saveItem(key, latestItems, modelname=DatasourceHistory)


def _saveNow(datasource, items, keyname):
    datasources = cmapi.getItemValue(keyname, [], modelname=LatestItem)

    days = 7
    strStart = dateutil.getHoursAs14(days * 24)
    datasources = [child for child in datasources
                    if child['source']['added'] >= strStart]

    data = {
        'source': datasource,
        'pages': items,
    }

    foundIndex = -1
    for i in range(len(datasources)):
        item = datasources[i]
        if item['source'].get('slug') == datasource.get('slug'):
            foundIndex = i
            break
    if foundIndex >= 0:
        datasources[foundIndex] = data
    else:
        datasources.append(data)
    cmapi.saveItem(keyname, datasources, modelname=LatestItem)


def saveDatasource(datasource, items):
    # charts refresh operation does not need archive.
    if 'refreshing' not in datasource:
        _saveHistory(datasource, items)

    if datasource.get('charts'):
        keyname = 'chartses'
    else:
        keyname = 'sites'
    _saveNow(datasource, items, keyname)

def getArchiveConfig():
    return cmapi.getItemValue('archive', {})

def archiveData(key, datasources):
    oldValue = cmapi.getItemValue(key, [], modelname=DatasourceArchive)
    if oldValue:
        oldValue.extend(datasources)
    else:
        oldValue = datasources
    cmapi.saveItem(key, oldValue, modelname=DatasourceArchive)

def getPages(datasources=None, keyname=None):
    if keyname:
        datasources = cmapi.getItemValue(keyname, [], modelname=LatestItem)
    pages = []
    for datasource in datasources:
        for childPage in datasource['pages']:
            childPage['source'] = datasource['source']
            pages.append(childPage)
    return pages

