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
    ObjectNotFoundException
from cmislib import util


@pytest.mark.usefixtures('cmis_env', 'binary_files')
class TestRepository:

    """ Tests for the :class:`Repository` class. """

    def testRepositoryInfo(self):
        """Retrieve repository info"""
        repoInfo = self._repo.getRepositoryInfo()
        assert 'repositoryId' in repoInfo
        assert 'repositoryName' in repoInfo
        assert 'repositoryDescription' in repoInfo
        assert 'vendorName' in repoInfo
        assert 'productName' in repoInfo
        assert 'productVersion' in repoInfo
        assert 'rootFolderId' in repoInfo
        assert 'cmisVersionSupported' in repoInfo

    def testRepositoryCapabilities(self):
        """Retrieve repository capabilities"""
        caps = self._repo.getCapabilities()
        assert 'ACL' in caps
        assert 'AllVersionsSearchable' in caps
        assert 'Changes' in caps
        assert 'ContentStreamUpdatability' in caps
        assert 'GetDescendants' in caps
        assert 'GetFolderTree' in caps
        assert 'Multifiling' in caps
        assert 'PWCSearchable' in caps
        assert 'PWCUpdatable' in caps
        assert 'Query' in caps
        assert 'Renditions' in caps
        assert 'Unfiling' in caps
        assert 'VersionSpecificFiling' in caps
        assert 'Join' in caps

    def testGetRootFolder(self):
        """Get the root folder of the repository"""
        rootFolder = self._repo.getRootFolder()
        assert rootFolder is not None
        assert rootFolder.getObjectId() is not None

    def testCreateFolder(self):
        """Create a new folder in the root folder"""
        folderName = 'testCreateFolder folder'
        newFolder = self._repo.createFolder(self._rootFolder, folderName)
        assert folderName == newFolder.getName()
        newFolder.delete()

    def testCreateDocument(self):
        """Create a new 'content-less' document"""
        documentName = 'testDocument'
        newDoc = self._repo.createDocument(
            documentName, parentFolder=self._testFolder)
        assert documentName == newDoc.getName()

    def testCreateDocumentFromString(self):
        """Create a new document from a string"""
        documentName = 'testDocument'
        contentString = 'Test content string'
        newDoc = self._repo.createDocumentFromString(
            documentName,
            parentFolder=self._testFolder,
            contentString=contentString,
            contentType='text/plain')
        assert documentName == newDoc.getName()
        assert util.to_native(
            newDoc.getContentStream().read()) == contentString

    # CMIS-279
    def testCreateDocumentUnicode(self):
        """Create a new doc with unicode characters in the name"""
        documentName = u'abc cdeöäüß%§-_caféè.txt'
        newDoc = self._repo.createDocument(
            documentName, parentFolder=self._testFolder)
        assert documentName == newDoc.getName()

    def testGetObject(self):
        """Create a test folder then attempt to retrieve it as a
        :class:`CmisObject` object using its object ID"""
        folderName = 'testGetObject folder'
        newFolder = self._repo.createFolder(self._testFolder, folderName)
        objectId = newFolder.getObjectId()
        someObject = self._repo.getObject(objectId)
        assert folderName == someObject.getName()
        newFolder.delete()

    def testReturnVersion(self):
        """Get latest and latestmajor versions of an object"""
        fileName = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            doc10 = self._testFolder.createDocument(
                fileName, contentFile=f, properties=props)
        doc10Id = doc10.getObjectId()
        if 'canCheckOut' not in doc10.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc10.checkout()
        doc11 = pwc.checkin(major='false')  # checkin a minor version, 1.1
        if 'canCheckOut' not in doc11.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc11.checkout()
        doc20 = pwc.checkin()  # checkin a major version, 2.0
        doc20Id = doc20.getObjectId()
        if 'canCheckOut' not in doc20.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc20.checkout()
        doc21 = pwc.checkin(major='false')  # checkin a minor version, 2.1
        doc21Id = doc21.getObjectId()

        docLatest = self._repo.getObject(doc10Id, returnVersion='latest')
        assert doc21Id == docLatest.getObjectId()

        docLatestMajor = self._repo.getObject(
            doc10Id, returnVersion='latestmajor')
        assert doc20Id == docLatestMajor.getObjectId()

    def testGetFolder(self):
        """Create a test folder then attempt to retrieve the Folder object
        using its object ID"""
        folderName = 'testGetFolder folder'
        newFolder = self._repo.createFolder(self._testFolder, folderName)
        objectId = newFolder.getObjectId()
        someFolder = self._repo.getFolder(objectId)
        assert folderName == someFolder.getName()
        newFolder.delete()

    def testGetObjectByPath(self):
        """Create test objects (one folder, one document) then try to get
        them by path"""
        # names of folders and test docs (without and with unicode char)
        for suffix in ['', u'_éà€$', ' +']:
            if '+' in suffix and self._productVersion < '6.0.0':
                print('+ not supported in alfresco < 6.0.0')
                continue
            parentFolderName = 'testGetObjectByPath folder' + suffix
            subFolderName = 'subfolder' + suffix
            docName = 'testdoc' + suffix

            # create the folder structure
            parentFolder = self._testFolder.createFolder(parentFolderName)
            subFolder = parentFolder.createFolder(subFolderName)
            # use the subfolder path to get the folder by path
            subFolderPath = subFolder.getProperties().get("cmis:path")
            searchFolder = self._repo.getObjectByPath(subFolderPath)
            assert subFolder.getObjectId() == searchFolder.getObjectId()

            # create a test doc
            doc = subFolder.createDocument(docName)
            # ask the doc for its paths
            searchDocPaths = doc.getPaths()
            # for each path in the list, try to get the object by path
            # this is better than building a path with the doc's name b/c
            # the name isn't guaranteed to be used as the path segment
            # (see CMIS-232)
            for path in searchDocPaths:
                searchDoc = self._repo.getObjectByPath(path)
                assert doc.getObjectId() == searchDoc.getObjectId()

            # get the subfolder by path, then ask for its children
            subFolder = self._repo.getObjectByPath(subFolderPath)
            assert len(subFolder.getChildren().getResults()) == 1

    # Create document without a parent folder is not yet implemented
    # def testCreateUnfiledDocument(self):
    #     '''Create a new unfiled document'''
    #     if self._repo.getCapabilities()['Unfiling'] != True:
    #         print ('Repo does not support unfiling, skipping')
    #         return
    #     documentName = 'testDocument'
    #     newDoc = self._repo.createDocument(documentName)
    #     self.assertEquals(documentName, newDoc.getName())

    def testMoveDocument(self):
        """Move a Document from one folder to another folder"""
        subFolder1 = self._testFolder.createFolder('sub1')
        doc = subFolder1.createDocument('testdoc1')
        assert len(subFolder1.getChildren()) == 1
        subFolder2 = self._testFolder.createFolder('sub2')
        assert len(subFolder2.getChildren()) == 0
        doc.move(subFolder1, subFolder2)
        assert len(subFolder1.getChildren()) == 0
        assert len(subFolder2.getChildren()) == 1
        assert doc.name == subFolder2.getChildren()[0].name

    # Exceptions

    def testGetObjectBadId(self):
        """Attempt to get an object using a known bad ID"""
        # this object ID is implementation specific (Alfresco) but is
        # universally bad so it should work for all repositories
        with pytest.raises(ObjectNotFoundException):
            self._repo.getObject(self._testFolder.getObjectId()[:-5] + 'BADID')

    def testGetObjectBadPath(self):
        """Attempt to get an object using a known bad path"""
        with pytest.raises(ObjectNotFoundException):
            self._repo.getObjectByPath('/123foo/BAR.jtp')
