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
    CmisException
from .tools import isInResultSet


@pytest.mark.usefixtures('cmis_env')
class TestFolder:

    """ Tests for the :class:`Folder` class """

    def testGetChildren(self):
        """Get the children of the test folder"""
        childFolderName1 = 'testchild1'
        childFolderName2 = 'testchild2'
        grandChildFolderName = 'testgrandchild'
        childFolder1 = self._testFolder.createFolder(childFolderName1)
        childFolder2 = self._testFolder.createFolder(childFolderName2)
        grandChild = childFolder2.createFolder(grandChildFolderName)
        resultSet = self._testFolder.getChildren()
        assert resultSet is not None
        assert 2 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert not isInResultSet(resultSet, grandChild)

    def testGetDescendants(self):
        """Get the descendants of the root folder"""
        childFolderName1 = 'testchild1'
        childFolderName2 = 'testchild2'
        grandChildFolderName1 = 'testgrandchild'
        childFolder1 = self._testFolder.createFolder(childFolderName1)
        childFolder2 = self._testFolder.createFolder(childFolderName2)
        grandChild = childFolder1.createFolder(grandChildFolderName1)

        # test getting descendants with depth=1
        resultSet = self._testFolder.getDescendants(depth=1)
        assert resultSet is not None
        assert 2 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert not isInResultSet(resultSet, grandChild)

        # test getting descendants with depth=2
        resultSet = self._testFolder.getDescendants(depth=2)
        assert resultSet is not None
        assert 3 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert isInResultSet(resultSet, grandChild)

        # test getting descendants with depth=-1
        # -1 is the default depth
        resultSet = self._testFolder.getDescendants()
        assert resultSet is not None
        assert 3 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert isInResultSet(resultSet, grandChild)

    def testGetTree(self):
        """Get the folder tree of the test folder"""
        childFolderName1 = 'testchild1'
        childFolderName2 = 'testchild2'
        grandChildFolderName1 = 'testgrandchild'
        childFolder1 = self._testFolder.createFolder(childFolderName1)
        childFolder1.createDocument('testdoc1')
        childFolder2 = self._testFolder.createFolder(childFolderName2)
        childFolder2.createDocument('testdoc2')
        grandChild = childFolder1.createFolder(grandChildFolderName1)
        grandChild.createDocument('testdoc3')

        # test getting tree with depth=1
        resultSet = self._testFolder.getTree(depth=1)
        assert resultSet is not None
        assert 2 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert not isInResultSet(resultSet, grandChild)

        # test getting tree with depth=2
        resultSet = self._testFolder.getTree(depth=2)
        assert resultSet is not None
        assert 3 == len(resultSet.getResults())
        assert isInResultSet(resultSet, childFolder1)
        assert isInResultSet(resultSet, childFolder2)
        assert isInResultSet(resultSet, grandChild)

    def testDeleteEmptyFolder(self):
        """Create a test folder, then delete it"""
        folderName = 'testDeleteEmptyFolder folder'
        testFolder = self._testFolder.createFolder(folderName)
        assert folderName == testFolder.getName()
        newFolder = testFolder.createFolder('testFolder')
        testFolderChildren = testFolder.getChildren()
        assert 1 == len(testFolderChildren.getResults())
        newFolder.delete()
        testFolderChildren = testFolder.getChildren()
        assert 0 == len(testFolderChildren.getResults())

    def testDeleteNonEmptyFolder(self):
        """Create a test folder with something in it, then delete it"""
        folderName = 'testDeleteNonEmptyFolder folder'
        testFolder = self._testFolder.createFolder(folderName)
        assert folderName == testFolder.getName()
        newFolder = testFolder.createFolder('testFolder')
        testFolderChildren = testFolder.getChildren()
        assert 1 == len(testFolderChildren.getResults())
        newFolder.createDocument('testDoc')
        assert 1 == len(newFolder.getChildren().getResults())
        newFolder.deleteTree()
        testFolderChildren = testFolder.getChildren()
        assert 0 == len(testFolderChildren.getResults())

    def testGetProperties(self):
        """Get the root folder, then get its properties"""
        props = self._testFolder.getProperties()
        assert props is not None
        assert 'cmis:objectId' in props
        assert props['cmis:objectId'] is not None
        assert 'cmis:objectTypeId' in props
        assert props['cmis:objectTypeId'] is not None
        assert 'cmis:name' in props
        assert props['cmis:name'] is not None

    def testPropertyFilter(self):
        """Test the properties filter"""
        # names of folders and test docs
        parentFolderName = 'testGetObjectByPath folder'
        subFolderName = 'subfolder'

        # create the folder structure
        parentFolder = self._testFolder.createFolder(parentFolderName)
        subFolder = parentFolder.createFolder(subFolderName)
        subFolderPath = subFolder.getProperties().get("cmis:path")

        # Per CMIS-170, CMIS providers are not required to filter the
        # properties returned. So these tests will check only for the presence
        # of the properties asked for, not the absence of properties that
        # should be filtered if the server chooses to do so.

        # test when used with getObjectByPath
        searchFolder = self._repo.getObjectByPath(
            subFolderPath,
            filter='cmis:objectId,cmis:objectTypeId,cmis:baseTypeId')
        assert subFolder.getObjectId() == searchFolder.getObjectId()
        assert 'cmis:objectId' in searchFolder.getProperties()
        assert 'cmis:objectTypeId' in searchFolder.getProperties()
        assert 'cmis:baseTypeId' in searchFolder.getProperties()

        # test when used with getObjectByPath + reload
        searchFolder = self._repo.getObjectByPath(
            subFolderPath,
            filter='cmis:objectId,cmis:objectTypeId,cmis:baseTypeId')
        searchFolder.reload()
        assert subFolder.getObjectId() == searchFolder.getObjectId()
        assert 'cmis:objectId' in searchFolder.getProperties()
        assert 'cmis:objectTypeId' in searchFolder.getProperties()
        assert 'cmis:baseTypeId' in searchFolder.getProperties()

        # test when used with getObject
        searchFolder = self._repo.getObject(
            subFolder.getObjectId(),
            filter='cmis:objectId,cmis:objectTypeId,cmis:baseTypeId')
        assert subFolder.getObjectId() == searchFolder.getObjectId()
        assert 'cmis:objectId' in searchFolder.getProperties()
        assert 'cmis:objectTypeId' in searchFolder.getProperties()
        assert 'cmis:baseTypeId' in searchFolder.getProperties()

        # test when used with getObject + reload
        searchFolder = self._repo.getObject(
            subFolder.getObjectId(),
            filter='cmis:objectId,cmis:objectTypeId,cmis:baseTypeId')
        searchFolder.reload()
        assert subFolder.getObjectId() == searchFolder.getObjectId()
        assert 'cmis:objectId' in searchFolder.getProperties()
        assert 'cmis:objectTypeId' in searchFolder.getProperties()
        assert 'cmis:baseTypeId' in searchFolder.getProperties()

        # test that you can do a reload with a reset filter
        searchFolder.reload(filter='*')
        assert 'cmis:objectId' in searchFolder.getProperties()
        assert 'cmis:objectTypeId' in searchFolder.getProperties()
        assert 'cmis:baseTypeId' in searchFolder.getProperties()
        assert 'cmis:name' in searchFolder.getProperties()

    def testUpdateProperties(self):
        """Create a test folder, then update its properties"""
        folderName = 'testUpdateProperties folder'
        newFolder = self._testFolder.createFolder(folderName)
        assert folderName == newFolder.getName()
        folderName2 = 'testUpdateProperties folder2'
        props = {'cmis:name': folderName2}
        newFolder.updateProperties(props)
        assert folderName2 == newFolder.getName()

    def testSubFolder(self):
        """Create a test folder, then create a test folder within that."""
        parentFolder = self._testFolder.createFolder('testSubFolder folder')
        assert 'cmis:objectId' in parentFolder.getProperties()
        childFolder = parentFolder.createFolder('child folder')
        assert 'cmis:objectId' in childFolder.getProperties()
        assert childFolder.getProperties()['cmis:objectId'] is not None

    def testAllowableActions(self):
        """Create a test folder, then get its allowable actions"""
        actions = self._testFolder.getAllowableActions()
        assert len(actions) > 0

    def testGetParent(self):
        """Get a folder's parent using the getParent call"""
        childFolder = self._testFolder.createFolder('parentTest')
        parentFolder = childFolder.getParent()
        assert self._testFolder.getObjectId() == parentFolder.getObjectId()

    def testAddObject(self):
        """Add an existing object to another folder"""
        if not self._repo.getCapabilities()['Multifiling']:
            pytest.skip('This repository does not allow multifiling, skipping')

        subFolder1 = self._testFolder.createFolder('sub1')
        doc = subFolder1.createDocument('testdoc1')
        assert len(subFolder1.getChildren()) == 1
        subFolder2 = self._testFolder.createFolder('sub2')
        assert len(subFolder2.getChildren()) == 0
        subFolder2.addObject(doc)
        assert len(subFolder2.getChildren()) == 1
        assert (
            subFolder1.getChildren()[0].name ==
            subFolder2.getChildren()[0].name)

    def testRemoveObject(self):
        """Remove an existing object from a secondary folder"""
        if not self._repo.getCapabilities()['Unfiling']:
            pytest.skip('This repository does not allow unfiling, skipping')

        subFolder1 = self._testFolder.createFolder('sub1')
        doc = subFolder1.createDocument('testdoc1')
        assert len(subFolder1.getChildren()) == 1
        subFolder2 = self._testFolder.createFolder('sub2')
        assert len(subFolder2.getChildren()) == 0
        subFolder2.addObject(doc)
        assert len(subFolder2.getChildren()) == 1
        assert (
            subFolder1.getChildren()[0].name ==
            subFolder2.getChildren()[0].name)
        subFolder2.removeObject(doc)
        assert len(subFolder2.getChildren()) == 0
        assert len(subFolder1.getChildren()) == 1
        assert doc.name == subFolder1.getChildren()[0].name

    def testGetPaths(self):
        """Get a folder's paths"""
        # ask the root for its path
        root = self._repo.getRootFolder()
        paths = root.getPaths()
        assert len(paths) == 1
        assert paths[0] == '/'
        # ask the test folder for its paths
        paths = self._testFolder.getPaths()
        assert len(paths) == 1

    # Exceptions

    def testBadParentFolder(self):
        """Try to create a folder on a bad/bogus/deleted parent
        folder object"""
        firstFolder = self._testFolder.createFolder(
            'testBadParentFolder folder')
        assert 'cmis:objectId' in firstFolder.getProperties()
        firstFolder.delete()
        # folder isn't in the repo anymore, but I still have the object
        # really, this seems like it ought to be an ObjectNotFoundException but
        # not all CMIS providers report it as such
        with pytest.raises(CmisException):
            firstFolder.createFolder('bad parent')
