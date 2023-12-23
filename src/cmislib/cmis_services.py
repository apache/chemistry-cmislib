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

    def __init__(self, **kwargs):
        self.extArgs = kwargs
        self.user_agent = 'cmislib +http://chemistry.apache.org/'

    def getRepositoryService(self):

        """
        Returns the repository service specific to this binding.
        """

        pass

    def _get_http_headers(self, **kwargs):
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
        headers['User-Agent'] = self.user_agent
        return headers

    def get(self, url, session, **kwargs):

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
        if len(self.extArgs) > 0:
            kwargs.update(self.extArgs)

        headers = self._get_http_headers(**kwargs)
        return session.get(url, params=kwargs, headers=headers)

    def post(self, url, session, payload, contentType, **kwargs):

        """
        Does a post against the CMIS service. More than likely, you will not
        need to call this method. Instead, let the other objects do it for you.

        For example, to update the properties on an object, you'd call
        :class:`CmisObject.updateProperties`. Or, to check in a document that's
        been checked out, you'd call :class:`Document.checkin` on the PWC.
        """

        # merge the cmis client extended args with the ones that got passed in
        if len(self.extArgs) > 0:
            kwargs.update(self.extArgs)
        headers = self._get_http_headers(**kwargs)
        headers['Content-Type'] = contentType
        return session.post(
            url, params=kwargs, data=payload, headers=headers)

    def delete(self, url, session, **kwargs):

        """
        Does a delete against the CMIS service. More than likely, you will not
        need to call this method. Instead, let the other objects do it for you.

        For example, to delete a folder you'd call :class:`Folder.delete` and
        to delete a document you'd call :class:`Document.delete`.
        """

        # merge the cmis client extended args with the ones that got passed in
        if len(self.extArgs) > 0:
            kwargs.update(self.extArgs)

        headers = self._get_http_headers(**kwargs)
        response = session.delete(url, params=kwargs, headers=headers)
        return response

    def put(self, url, session, payload, contentType, **kwargs):

        """
        Does a put against the CMIS service. More than likely, you will not
        need to call this method. Instead, let the other objects do it for you.

        For example, to update the properties on an object, you'd call
        :class:`CmisObject.updateProperties`. Or, to check in a document that's
        been checked out, you'd call :class:`Document.checkin` on the PWC.
        """

        # merge the cmis client extended args with the ones that got passed in
        if len(self.extArgs) > 0:
            kwargs.update(self.extArgs)

        headers = self._get_http_headers(**kwargs)
        headers['Content-Type'] = contentType
        return session.put(url, data=payload, params=kwargs, headers=headers)

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
