
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
class TestChangeEntry:

    """ Tests for the :class:`ChangeEntry` class """

    def testGetContentChanges(self):

        """Get the content changes and inspect Change Entry props"""

        # need to check changes capability
        changeCap = self._repo.capabilities['Changes']
        if changeCap is None or changeCap == 'none':
            pytest.skip(messages.NO_CHANGE_LOG_SUPPORT)

        # at least one change should have been made due to the creation of the
        # test documents
        rs = self._repo.getContentChanges()
        assert len(rs) > 0
        changeEntry = rs[0]
        assert changeEntry.objectId
        assert changeEntry.changeType in [
            'created', 'updated', 'deleted', 'security']
        assert changeEntry.changeTime

    def testGetACL(self):

        """Gets the ACL that is included with a Change Entry."""

        # need to check changes capability
        changeCap = self._repo.capabilities['Changes']
        if changeCap is None or changeCap == 'none':
            pytest.skip(messages.NO_CHANGE_LOG_SUPPORT)

        if changeCap == 'objectidsonly':
            pytest.skip(messages.NO_CHANGE_OBJECT_SUPPORT)

        # need to check ACL capability
        if not self._repo.capabilities['ACL']:
            pytest.skip(messages.NO_ACL_SUPPORT)

        # need to test once with includeACL set to true
        rs = self._repo.getContentChanges(includeACL='true')
        assert len(rs) > 0
        changeEntry = rs[0]
        acl = changeEntry.getACL()
        assert acl
        for entry in acl.getEntries().values():
            assert entry.principalId
            assert entry.permissions

        # need to test once without includeACL set
        rs = self._repo.getContentChanges()
        assert len(rs) > 0
        changeEntry = rs[0]
        acl = changeEntry.getACL()
        assert acl
        for entry in acl.getEntries().values():
            assert entry.principalId
            assert entry.permissions

    def testGetProperties(self):

        """Gets the properties of an object included with a Change Entry."""

        # need to check changes capability
        changeCap = self._repo.capabilities['Changes']
        if changeCap is None or changeCap == 'none':
            pytest.skip(messages.NO_CHANGE_LOG_SUPPORT)

        if changeCap == 'objectidsonly':
            pytest.skip(messages.NO_CHANGE_OBJECT_SUPPORT)

        # need to test once without includeProperties set. the objectID
        # should be there
        rs = self._repo.getContentChanges()
        assert len(rs) > 0
        changeEntry = rs[0]
        assert changeEntry.properties['cmis:objectId']

        # need to test once with includeProperties set. the objectID
        # should be there plus object props
        if changeCap in ['properties', 'all']:
            rs = self._repo.getContentChanges(includeProperties='true')
            assert len(rs) > 0
            changeEntry = rs[0]
            assert changeEntry.properties['cmis:objectId']
            assert changeEntry.properties['cmis:name']
