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
import os
from contextlib import closing
from time import sleep

import pytest

from cmislib.exceptions import \
    CmisException, \
    NotSupportedException
from .tools import skipIfAlfrescoPubBinding
from .tools import skipIfAlfrescoBrowserBinding
from cmislib import util


@pytest.mark.usefixtures('cmis_env', 'binary_files')
class TestDocument:

    """ Tests for the :class:`Document` class """

    def testCheckout(self):
        """Create a document in a test folder, then check it out"""
        props = {'cmis:objectTypeId': self.versionable_type_id}
        newDoc = self._testFolder.createDocument(
            'testDocument', properties=props)
        if 'canCheckOut' not in newDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwcDoc = newDoc.checkout()
        try:
            assert newDoc.isCheckedOut()
            assert 'cmis:objectId' in newDoc.getProperties()
            assert 'cmis:objectId' in pwcDoc.getProperties()
        finally:
            pwcDoc.delete()

    # CMIS-743
    def testCheckoutAfterFetchByID(self):
        """Create a test doc, fetch it by ID, then check it out"""
        props = {'cmis:objectTypeId': self.versionable_type_id}
        newDoc = self._testFolder.createDocument(
            'testDocument', properties=props)
        if 'canCheckOut' not in newDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        newDocIdStr = str(newDoc.id)
        newDoc = self._repo.getObject(newDocIdStr)
        pwcDoc = newDoc.checkout()
        try:
            assert newDoc.isCheckedOut()
            assert 'cmis:objectId' in newDoc.getProperties()
            assert 'cmis:objectId' in pwcDoc.getProperties()
        finally:
            pwcDoc.delete()

    def testCheckin(self):
        """Create a document in a test folder, check it out, then in"""
        testFilename = self.binary_filename_1

        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            testDoc = self._testFolder.createDocument(
                testFilename, contentFile=f, properties=props)
        assert testFilename == testDoc.getName()
        if 'canCheckOut' not in testDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwcDoc = testDoc.checkout()

        try:
            assert testDoc.isCheckedOut()
            assert 'cmis:objectId' in testDoc.getProperties()
            assert 'cmis:objectId' in pwcDoc.getProperties()
            testDoc = pwcDoc.checkin()
            assert not testDoc.isCheckedOut()
        finally:
            if testDoc.isCheckedOut():
                pwcDoc.delete()

    def testCheckinComment(self):
        """Checkin a document with a comment"""
        testFilename = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            testDoc = self._testFolder.createDocument(
                testFilename, contentFile=f, properties=props)
        assert testFilename == testDoc.getName()
        if 'canCheckOut' not in testDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwcDoc = testDoc.checkout()
        try:
            assert testDoc.isCheckedOut()
            testDoc = pwcDoc.checkin(checkinComment='Just a few changes')
            assert not testDoc.isCheckedOut()
            assert ('Just a few changes' ==
                    testDoc.getProperties()['cmis:checkinComment'])
        finally:
            if testDoc.isCheckedOut():
                pwcDoc.delete()

    @skipIfAlfrescoPubBinding
    def testCheckinContentAndProperties(self):
        """Checkin a document with a new content a modifed properties"""
        testFilename = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            testDoc = self._testFolder.createDocument(
                testFilename, contentFile=f, properties=props)
        assert testFilename == testDoc.getName()
        if 'canCheckOut' not in testDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwcDoc = testDoc.checkout()
        try:
            assert testDoc.isCheckedOut()
            testFile2 = self.binary_file_2
            testFile2Size = os.path.getsize(testFile2)
            exportFile2 = testFile2.replace('.', 'export.')
            contentFile2 = open(testFile2, 'rb')
            props = {'cmis:name': 'testDocument2'}
            testDoc = pwcDoc.checkin(
                contentFile=contentFile2,
                properties=props)
            contentFile2.close()
            assert not testDoc.isCheckedOut()
            assert 'testDocument2' == testDoc.getName()

            # expport the result
            result = testDoc.getContentStream()
            outfile = open(exportFile2, 'wb')
            outfile.write(result.read())
            result.close()
            outfile.close()

            # the file we exported should be the same size as the file we
            # originally created
            assert testFile2Size == os.path.getsize(exportFile2)

        finally:
            if testDoc.isCheckedOut():
                pwcDoc.delete()

    def testCheckinAfterGetPWC(self):
        """Create a document in a test folder, check it out, call getPWC,
        then checkin
        """
        if not self._repo.getCapabilities()['PWCUpdatable']:
            pytest.skip('Repository does not support PWCUpdatable, skipping')
        testFilename = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            testDoc = self._testFolder.createDocument(
                testFilename, contentFile=f, properties=props)
        assert testFilename == testDoc.getName()
        # Alfresco has a bug where if you get the PWC this way
        # the checkin will not be successful
        if 'canCheckOut' not in testDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        testDoc.checkout()
        pwcDoc = testDoc.getPrivateWorkingCopy()
        try:
            assert testDoc.isCheckedOut()
            assert 'cmis:objectId' in testDoc.getProperties()
            assert 'cmis:objectId' in pwcDoc.getProperties()
            testDoc = pwcDoc.checkin()
            assert not testDoc.isCheckedOut()
        finally:
            if testDoc.isCheckedOut():
                pwcDoc.delete()

    def testCancelCheckout(self):
        """Create a document in a test folder, check it out, then cancel
        checkout"""
        props = {'cmis:objectTypeId': self.versionable_type_id}
        newDoc = self._testFolder.createDocument(
            'testDocument', properties=props)
        if 'canCheckOut' not in newDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwcDoc = newDoc.checkout()
        try:
            assert newDoc.isCheckedOut()
            assert 'cmis:objectId' in newDoc.getProperties()
            assert 'cmis:objectId' in pwcDoc.getProperties()
        finally:
            pwcDoc.delete()
        assert not newDoc.isCheckedOut()

    def testDeleteDocument(self):
        """Create a document in a test folder, then delete it"""
        newDoc = self._testFolder.createDocument('testDocument')
        children = self._testFolder.getChildren()
        assert 1 == len(children.getResults())
        newDoc.delete()
        children = self._testFolder.getChildren()
        assert 0 == len(children.getResults())

    def testGetLatestVersion(self):
        """Get latest version of an object"""
        fileName = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            doc10 = self._testFolder.createDocument(
                fileName, contentFile=f, properties=props)
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

        docLatest = doc10.getLatestVersion()
        assert doc21Id == docLatest.getObjectId()

        docLatestMajor = doc10.getLatestVersion(major='true')
        assert doc20Id == docLatestMajor.getObjectId()

    def testGetPropertiesOfLatestVersion(self):
        """Get properties of latest version of an object"""
        fileName = self.binary_filename_1
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            doc10 = self._testFolder.createDocument(
                fileName, contentFile=f, properties=props)
        if 'canCheckOut' not in doc10.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc10.checkout()
        doc11 = pwc.checkin(major='false')  # checkin a minor version, 1.1
        if 'canCheckOut' not in doc11.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc11.checkout()
        doc20 = pwc.checkin()  # checkin a major version, 2.0
        # what comes back from a checkin may not include all props, so reload
        doc20.reload()
        doc20Label = doc20.getProperties()['cmis:versionLabel']
        if 'canCheckOut' not in doc20.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc20.checkout()
        doc21 = pwc.checkin(major='false')  # checkin a minor version, 2.1
        # what comes back from a checkin may not include all props, so reload
        doc21.reload()
        doc21Label = doc21.getProperties()['cmis:versionLabel']

        propsLatest = doc10.getPropertiesOfLatestVersion()
        assert doc21Label == propsLatest['cmis:versionLabel']

        propsLatestMajor = doc10.getPropertiesOfLatestVersion(major='true')
        assert doc20Label == propsLatestMajor['cmis:versionLabel']

    def testGetProperties(self):
        """Create a document in a test folder, then get its properties"""
        newDoc = self._testFolder.createDocument('testDocument')
        assert 'testDocument' == newDoc.getName()
        assert 'cmis:objectTypeId' in newDoc.getProperties()
        assert 'cmis:objectId' in newDoc.getProperties()

    def testAllowableActions(self):
        """Create document in a test folder, then get its allowable actions"""
        newDoc = self._testFolder.createDocument('testDocument')
        actions = newDoc.getAllowableActions()
        assert len(actions) > 0

    def testUpdateProperties(self):
        """Create a document in a test folder, then update its properties"""
        newDoc = self._testFolder.createDocument('testDocument')
        assert 'testDocument' == newDoc.getName()
        props = {'cmis:name': 'testDocument2'}
        newDoc.updateProperties(props)
        assert 'testDocument2' == newDoc.getName()

    def testSetContentStreamPWC(self):
        """Set the content stream on the PWC"""
        if self._repo.getCapabilities()['ContentStreamUpdatability'] == 'none':
            pytest.skip(
                'This repository does not allow content stream updates, '
                'skipping')

        testFile1 = self.binary_file_1
        fileName1 = self.binary_filename_1
        testFile1Size = os.path.getsize(testFile1)
        exportFile1 = testFile1.replace('.', 'export.')
        testFile2 = self.binary_file_2
        testFile2Size = os.path.getsize(testFile2)
        exportFile2 = testFile1.replace('.', 'export.')

        # create a test document
        with open(testFile1, 'rb') as contentFile:
            newDoc = self._testFolder.createDocument(
                fileName1, contentFile=contentFile)

        # export the test document
        result = newDoc.getContentStream()
        with closing(result),  open(exportFile1, 'wb') as outfile:
            outfile.write(result.read())

        # the file we exported should be the same size as the file we
        # originally created
        assert testFile1Size == os.path.getsize(exportFile1)

        # checkout the file
        if newDoc.allowableActions.get('canCheckOut'):
            pass
        else:
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = newDoc.checkout()

        # update the PWC with a new file
        with open(testFile2, 'rb') as f:
            pwc.setContentStream(f)

        # checkin the PWC
        newDoc = pwc.checkin()

        # export the checked in document
        result = newDoc.getContentStream()
        with closing(result), open(exportFile2, 'wb') as outfile:
            outfile.write(result.read())

        # the file we exported should be the same size as the file we
        # checked in after updating the PWC
        assert testFile2Size == os.path.getsize(exportFile2)
        os.remove(exportFile2)

    def testSetContentStreamPWCMimeType(self):
        """Check the mimetype after the PWC checkin"""
        if self._repo.getCapabilities()['ContentStreamUpdatability'] == 'none':
            pytest.skip('This repository does not allow content stream '
                        'updates, skipping')

        testFile1 = self.binary_file_1
        fileName = testFile1.split('/')[-1]

        # create a test document
        props = {'cmis:objectTypeId': self.versionable_type_id}
        with open(self.binary_file_1, 'rb') as f:
            newDoc = self._testFolder.createDocument(
                fileName, contentFile=f, properties=props)
        origMimeType = newDoc.properties['cmis:contentStreamMimeType']

        # checkout the file
        if 'canCheckOut' not in newDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = newDoc.checkout()

        # update the PWC with a new file
        with open(testFile1, 'rb') as f:
            pwc.setContentStream(f)

        # checkin the PWC
        newDoc = pwc.checkin()

        # CMIS-231 the checked in doc should have the same mime type as
        # the original document
        assert (origMimeType ==
                newDoc.properties['cmis:contentStreamMimeType'])

    @skipIfAlfrescoPubBinding
    @skipIfAlfrescoBrowserBinding
    def testSetContentStreamDoc(self):
        """Set the content stream on a doc that's not checked out"""
        if self._repo.getCapabilities()[
                'ContentStreamUpdatability'] != 'anytime':
            pytest.skip('This repository does not allow content stream '
                        'updates on the doc, skipping')

        testFile1 = self.binary_file_1
        testFile1Size = os.path.getsize(testFile1)
        exportFile1 = testFile1.replace('.', 'export.')
        testFile2 = self.binary_file_2
        testFile2Size = os.path.getsize(testFile2)
        exportFile2 = testFile2.replace('.', 'export.')

        # create a test document
        fileName = testFile1.split('/')[-1]
        with open(testFile1, 'rb') as contentFile:
            newDoc = self._testFolder.createDocument(
                fileName, contentFile=contentFile)

        # export the test document
        result = newDoc.getContentStream()
        with closing(result), open(exportFile1, 'wb') as outfile:
            outfile.write(result.read())

        # the file we exported should be the same size as the file we
        # originally created
        assert testFile1Size == os.path.getsize(exportFile1)

        # update the PWC with a new file
        with open(testFile2, 'rb') as f:
            newDoc.setContentStream(f)

        # export the checked in document
        result = newDoc.getContentStream()
        with closing(result),  open(exportFile2, 'wb') as outfile:
            outfile.write(result.read())

        # the file we exported should be the same size as the file we
        # checked in after updating the PWC
        assert testFile2Size == os.path.getsize(exportFile2)
        os.remove(exportFile2)

    def testDeleteContentStreamPWC(self):
        """Delete the content stream of a PWC"""
        if self._repo.getCapabilities()['ContentStreamUpdatability'] == 'none':
            pytest.skip(
                'This repository does not allow content stream updates, '
                'skipping')
        if not self._repo.getCapabilities()['PWCUpdatable']:
            pytest.skip('Repository does not support PWCUpdatable, skipping')

        # create a test document
        props = {'cmis:objectTypeId': self.versionable_type_id}
        fileName = self.binary_filename_1
        with open(self.binary_file_1, 'rb') as f:
            newDoc = self._testFolder.createDocument(
                fileName, contentFile=f, properties=props)
        if 'canCheckOut' not in newDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = newDoc.checkout()
        pwc.deleteContentStream()
        with pytest.raises(CmisException):
            pwc.getContentStream()
        pwc.delete()

    def testCreateDocumentBinary(self):
        """Create a binary document using a file from the file system"""
        testFile = self.binary_file_1
        testFilename = testFile.split('/')[-1]
        with open(testFile, 'rb') as f:
            newDoc = self._testFolder.createDocument(
                testFilename, contentFile=f)
        assert testFilename == newDoc.getName()

        # test to make sure the file we get back is the same length
        # as the file we sent
        result = newDoc.getContentStream()
        exportFilename = testFilename.replace('.', 'export.')
        with closing(result), open(exportFilename, 'wb') as outfile:
            outfile.write(result.read())
        assert (os.path.getsize(testFile) ==
                os.path.getsize(exportFilename))

        # cleanup
        os.remove(exportFilename)

    def testCreateDocumentFromString(self):
        """Create a new document from a string"""
        documentName = 'testDocument'
        contentString = 'Test content string'
        newDoc = self._testFolder.createDocumentFromString(
            documentName,
            contentString=contentString,
            contentType='text/plain')
        assert documentName == newDoc.getName()
        assert util.to_native(
            newDoc.getContentStream().read()) == contentString

    def testCreateDocumentPlain(self):
        """Create a plain document using a file from the file system"""
        testFilename = 'plain.txt'
        with open(testFilename, 'w') as testFile:
            testFile.write('This is a sample text file line 1.\n')
            testFile.write('This is a sample text file line 2.\n')
            testFile.write('This is a sample text file line 3.\n')

        with open(testFilename, 'rb') as contentFile:
            newDoc = self._testFolder.createDocument(
                testFilename, contentFile=contentFile)
        assert testFilename == newDoc.getName()

        # test to make sure the file we get back is the same length as the
        # file we sent
        result = newDoc.getContentStream()
        exportFilename = testFilename.replace('txt', 'export.txt')
        with closing(result), open(exportFilename, 'wb') as outfile:
            outfile.write(result.read())
        assert (os.path.getsize(testFilename) ==
                os.path.getsize(exportFilename))

        # export
        os.remove(exportFilename)
        os.remove(testFilename)

    def testGetAllVersions(self):
        """Get all versions of an object"""
        props = {'cmis:objectTypeId': self.versionable_type_id}
        testDoc = self._testFolder.createDocument('testdoc', properties=props)
        if 'canCheckOut' not in testDoc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = testDoc.checkout()
        doc = pwc.checkin()  # 2.0
        if 'canCheckOut' not in doc.allowableActions.keys():
            pytest.skip('The test doc cannot be checked out...skipping')
        pwc = doc.checkout()
        doc = pwc.checkin()  # 3.0
        # what comes back from a checkin may not include all props, so reload
        doc.reload()
        # InMemory 0.9 is using 'V 3.0' so this test fails with that server
        # self.assertEquals('3.0', doc.getProperties()['cmis:versionLabel'])
        rs = doc.getAllVersions()
        assert 3 == len(rs.getResults())

    def testGetObjectParents(self):
        """Gets all object parents of an CmisObject"""
        childFolder = self._testFolder.createFolder('parentTest')
        parentFolder = childFolder.getObjectParents().getResults()[0]
        assert self._testFolder.getObjectId() == parentFolder.getObjectId()

    def testGetObjectParentsWithinRootFolder(self):
        """Gets all object parents of a root folder"""
        rootFolder = self._repo.getRootFolder()
        with pytest.raises(NotSupportedException):
            rootFolder.getObjectParents()

    def testGetObjectParentsMultiple(self):
        """Gets all parents of a multi-filed object"""
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
        parentNames = ['sub1', 'sub2']
        for parent in doc.getObjectParents():
            parentNames.remove(parent.name)
        assert len(parentNames) == 0

    def testGetPaths(self):
        """Get the paths of a document"""
        testDoc = self._testFolder.createDocument('testdoc')
        # ask the test doc for its paths
        paths = testDoc.getPaths()
        assert len(paths) >= 1

    @skipIfAlfrescoPubBinding
    def testRelationship(self):
        testDoc = self._testFolder.createDocument('testdoc')
        testDoc2 = self._testFolder.createDocument('testdoc2')
        relations = testDoc.getRelationships(relationshipDirection="either")
        assert 0 == len(relations)
        if not testDoc.getAllowableActions().get('canCreateRelationship'):
            pytest.skip('createRelationship not supported, skipping')
        if not self._repo.getTypeDefinition('R:cm:replaces'):
            pytest.skip('createRelationship not supported, skipping')

        relation = testDoc.createRelationship(testDoc2, 'R:cm:replaces')
        assert testDoc.getObjectId() == relation.source.getObjectId()
        assert testDoc2.getObjectId() == relation.target.getObjectId()
        relations = testDoc.getRelationships()
        assert 1 == len(relations)
        relation = relations[0]
        assert testDoc.getObjectId() == relation.source.getObjectId()
        assert testDoc2.getObjectId() == relation.target.getObjectId()

    def testRenditions(self):
        """Get the renditions for a document"""
        if 'Renditions' not in self._repo.getCapabilities():
            pytest.skip('Repo does not support unfiling, skipping')

        testDoc = self._testFolder.createDocumentFromString(
            'testdoc.txt', contentString='test', contentType='text/plain')
        sleep(10)
        if testDoc.getAllowableActions().get('canGetRenditions'):
            rends = testDoc.getRenditions()
            assert len(rends) >= 1
        else:
            pytest.skip('Test doc does not have rendition, skipping')
