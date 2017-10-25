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

from cmislib import messages


@pytest.mark.usefixtures('cmis_env')
class TestACL:

    """
    Tests related to :class:`ACL` and :class:`ACE`
    """

    def testSupportedPermissions(self):
        """Test the value of supported permissions enum"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        assert self._repo.getSupportedPermissions() in ['basic', 'repository', 'both']

    def testPermissionDefinitions(self):
        """Test the list of permission definitions"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        supportedPerms = self._repo.getPermissionDefinitions()
        assert supportedPerms.has_key('cmis:write')

    def testPermissionMap(self):
        """Test the permission mapping"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        permMap = self._repo.getPermissionMap()
        assert permMap.has_key('canGetProperties.Object')
        assert len(permMap['canGetProperties.Object']) > 0

    def testPropagation(self):
        """Test the propagation setting"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        assert self._repo.getPropagation() in ['objectonly', 'propagate', 'repositorydetermined']

    def testGetObjectACL(self):
        """Test getting an object's ACL"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        acl = self._testFolder.getACL()
        for entry in acl.getEntries().values():
            assert entry.principalId
            assert entry.permissions

    def testApplyACL(self):
        """Test updating an object's ACL"""
        if not self._repo.getCapabilities()['ACL']:
            print messages.NO_ACL_SUPPORT
            return
        if not self._repo.getCapabilities()['ACL'] == 'manage':
            print 'Repository does not support manage ACL'
            return
        if not self._repo.getSupportedPermissions() in ['both', 'basic']:
            print 'Repository needs to support either both or basic permissions for this test'
            return
        acl = self._testFolder.getACL()
        acl.removeEntry(self.acl_principal_id)
        acl.addEntry(self.acl_principal_id, 'cmis:write')
        acl = self._testFolder.applyACL(acl)
        # would be good to check that the permission we get back is what we set
        # but at least one server (Alf) appears to map the basic perm to a
        # repository-specific perm
        assert acl.getEntries().has_key(self.acl_principal_id)
