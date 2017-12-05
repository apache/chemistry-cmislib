# -*- coding: utf-8 -*-
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
This module contains the base Binding class and other service objects.
"""
from cmislib.exceptions import CmisException, RuntimeException, \
    ObjectNotFoundException, InvalidArgumentException, \
    PermissionDeniedException, NotSupportedException, \
    UpdateConflictException


class Binding(object):

    """
    Represents the binding used to communicate with the CMIS server.
    """

    def getRepositoryService(self):

        """
        Returns the repository service specific to this binding.
        """

        pass

    def _processCommonErrors(self, response):

        """
        Maps HTTPErrors that are common to all to exceptions. Only errors
        that are truly global, like 401 not authorized, should be handled
        here. Callers should handle the rest.
        """
        status_code = response.status_code
        url = response.url
        if status_code == 401:
            raise PermissionDeniedException(status_code, url, response.text)
        elif status_code == 400:
            raise InvalidArgumentException(status_code, url, response.text)
        elif status_code == 404:
            raise ObjectNotFoundException(status_code, url, response.text)
        elif status_code == 403:
            raise PermissionDeniedException(status_code, url, response.text)
        elif status_code == 405:
            raise NotSupportedException(status_code, url, response.text)
        elif status_code == 409:
            raise UpdateConflictException(status_code, url, response.text)
        elif status_code == 500:
            raise RuntimeException(status_code, url, response.text)
        else:
            raise CmisException(status_code, url, response.text)


class RepositoryServiceIfc(object):

    """
    Defines the interface for the repository service.
    """

    def getRepositories(self, client):

        """
        Returns a list of repositories for this server.
        """

        pass

    def getRepositoryInfo(self):

        """
        Returns the repository information for this server.
        """

        pass
