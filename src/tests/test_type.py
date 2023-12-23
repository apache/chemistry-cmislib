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

from cmislib.model import CmisClient


@pytest.mark.usefixtures('cmis_conf')
class TestType:

    """
    Tests for the :class:`ObjectType` class (and related methods in the
    :class:`Repository` class.
    """

    def testTypeDescendants(self):
        """Get the descendant types of the repository."""

        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        typeDefs = repo.getTypeDescendants()
        folderDef = None
        for typeDef in typeDefs:
            if typeDef.getTypeId() == 'cmis:folder':
                folderDef = typeDef
                break
        assert folderDef
        assert folderDef.baseId

    def testTypeChildren(self):
        """Get the child types for this repository and make sure cmis:folder
        is in the list."""

        # This test would be more interesting if there was a standard way to
        # deploy a custom model. Then we could look for custom types.

        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        typeDefs = repo.getTypeChildren()
        folderDef = None
        for typeDef in typeDefs:
            if typeDef.getTypeId() == 'cmis:folder':
                folderDef = typeDef
                break
        assert folderDef
        assert folderDef.baseId

    def testTypeDefinition(self):
        """Get the cmis:document type and test a few props of the type."""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        docTypeDef = repo.getTypeDefinition('cmis:document')
        assert 'cmis:document' == docTypeDef.getTypeId()
        assert docTypeDef.baseId

    def testTypeProperties(self):
        """Get the properties for a type."""
        cmisClient = CmisClient(self.url, self.user, self.pwd,
                                binding=self.binding,
                                **self.ext_args)
        repo = cmisClient.getDefaultRepository()
        docTypeDef = repo.getTypeDefinition('cmis:document')
        assert 'cmis:document' == docTypeDef.getTypeId()
        props = docTypeDef.getProperties().values()
        assert len(props) > 0
        for prop in props:
            if prop.queryable:
                assert prop.queryName
            assert prop.propertyType
