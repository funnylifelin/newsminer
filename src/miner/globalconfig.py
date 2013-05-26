from configmanager import cmapi

def getWordsServerUrls():
    return cmapi.getItemValue('words.server.urls', {})

def getMasterUrls():
    return cmapi.getItemValue('master.urls', [])

def getChannels():
    return cmapi.getItemValue('channels', [])

def getTimezone():
    return cmapi.getItemValue('timezone', 0)

