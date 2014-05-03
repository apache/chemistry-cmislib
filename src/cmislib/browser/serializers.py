import json

from cmislib.browser.binding import BrowserFolder


class FolderSerializer(object):
    def toJSON(self, obj):
        pass

    def fromJSON(self, client, repo, jsonString):
        obj = json.loads(jsonString)
        objectId = obj['succinctProperties']['cmis:objectId']
        folder = BrowserFolder(client, repo, objectId, properties=obj['succinctProperties'])
        return folder