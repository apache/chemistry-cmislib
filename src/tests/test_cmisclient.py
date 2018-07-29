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
import pytest

from cmislib.exceptions import \
    ObjectNotFoundException, \
    CmisException
from cmislib.model import CmisClient


@pytest.mark.usefixtures('cmis_conf')
class TestCmisClient:

    """ Tests for the :class:`CmisClient` class. """

    def testCmisClient(self):
        """Instantiate a CmisClient object"""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        assert cmisClient is not None

    def testGetRepositories(self):
        """Call getRepositories and make sure at least one comes back with
        an ID and a name
        """
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repoInfo = cmisClient.getRepositories()
        assert len(repoInfo) >= 1
        assert 'repositoryId' in repoInfo[0]
        assert 'repositoryName' in repoInfo[0]

    def testDefaultRepository(self):
        """Get the default repository by calling the repo's service URL"""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        assert repo is not None
        assert repo.getRepositoryId() is not None

    def testGetRepository(self):
        """Get a repository by repository ID"""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        defaultRepoId = repo.getRepositoryId()
        defaultRepoName = repo.getRepositoryName()
        repo = cmisClient.getRepository(defaultRepoId)
        assert defaultRepoId == repo.getRepositoryId()
        assert defaultRepoName == repo.getRepositoryName()

    # Error conditions
    def testCmisClientBadUrl(self):
        """Try to instantiate a CmisClient object with a known bad URL"""
        cmisClient = CmisClient(self.url + 'foobar', self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        with pytest.raises(CmisException):
            cmisClient.getRepositories()

    def testGetRepositoryBadId(self):
        """Try to get a repository with a bad repo ID"""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        with pytest.raises(ObjectNotFoundException):
            cmisClient.getRepository('123FOO')
