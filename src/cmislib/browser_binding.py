#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#
"""
Module containing the browser binding-specific objects used to work with a CMIS
provider.
"""
from cmis_services import RepositoryServiceIfc
from cmis_services import Binding
from net import RESTService as Rest
from urllib2 import HTTPError
from exceptions import CmisException, RuntimeException
from domain import Repository
import json

class BrowserBinding(Binding):
    def __init__(self, **kwargs):
        self.extArgs = kwargs

    def getRepositoryService(self):
        return RepositoryService()

    def get(self, url, username, password, **kwargs):

        """
        Does a get against the CMIS service. More than likely, you will not
        need to call this method. Instead, let the other objects do it for you.

        For example, if you need to get a specific object by object id, try
        :class:`Repository.getObject`. If you have a path instead of an object
        id, use :class:`Repository.getObjectByPath`. Or, you could start with
        the root folder (:class:`Repository.getRootFolder`) and drill down from
        there.
        """

        # merge the cmis client extended args with the ones that got passed in
        if (len(self.extArgs) > 0):
            kwargs.update(self.extArgs)

        result = Rest().get(url,
                            username=username,
                            password=password,
                            **kwargs)
        if type(result) == HTTPError:
            self._processCommonErrors(result)
        else:
            result = json.load(result)
        return result

class RepositoryService(RepositoryServiceIfc):
    def getRepository(self, client, repositoryId):
        #TODO
        pass

    def getRepositories(self, client):
        result = client.binding.get(client.repositoryUrl, client.username, client.password, **client.extArgs)
        if (type(result) == HTTPError):
            raise RuntimeException()

        repositories = []
        for repo in result.itervalues():
            repositories.append({'repositoryId': repo['repositoryId'],
                                 'repositoryName': repo['repositoryName']})
        return repositories

    def getDefaultRepository(self, client):
        result = client.binding.get(client.repositoryUrl, client.username, client.password, **client.extArgs)
        # instantiate a Repository object with the first workspace
        # element we find
        for repo in result.itervalues():
            repository = Repository(client, repo)
        return repository

    def getRepositoryId(self, result):
        return result['repositoryId']

    def getRepositoryName(self, result):
        return result['repositoryName']

    def getRepositoryInfo(self):
        return "Here is your repository info using the browser binding"
