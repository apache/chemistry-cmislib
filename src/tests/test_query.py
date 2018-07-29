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
from time import sleep

import pytest

from .tools import isInResultSet
from .tools import skipIfAlfrescoBrowserBinding
from .tools import skipIfAlfrescoPubBinding


@pytest.mark.usefixtures('cmis_env')
class TestQuery:
    """ Tests related to running CMIS queries. """

    @pytest.fixture(autouse=True)
    def sampleContent(self, binary_files, cmis_env):
        """
        Creating a couple of test docs.
        """
        # I think this may be an Alfresco bug. The CMIS query results contain
        # 1 less entry element than the number of search results. So this test
        # will create two documents and search for the second one which should
        # work in all repositories.
        testFileName = self.binary_filename_2
        with open(self.binary_file_2, 'rb') as f:
            self._testContent = self._testFolder.createDocument(
                testFileName, contentFile=f)
        with open(self.binary_file_2, 'rb') as f:
            self._testContent2 = self._testFolder.createDocument(
                testFileName.replace('.', '2.'), contentFile=f)

    def testSimpleSelect(self):
        """Execute simple select star from cmis:document"""
        querySimpleSelect = "SELECT * FROM cmis:document"
        resultSet = self._repo.query(querySimpleSelect)
        assert isInResultSet(resultSet, self._testContent)

    def testWildcardPropertyMatch(self):
        """Find content w/wildcard match on cmis:name property"""
        name = self._testContent.getProperties()['cmis:name']
        querySimpleSelect = "SELECT * FROM cmis:document where " \
                            "cmis:name like '" + name[:7] + "%'"
        resultSet = self._repo.query(querySimpleSelect)
        assert isInResultSet(resultSet, self._testContent)

    def testPropertyMatch(self):
        """Find content matching cmis:name property"""
        name = self._testContent2.getProperties()['cmis:name']
        querySimpleSelect = "SELECT * FROM cmis:document where " \
                            "cmis:name = '" + name + "'"
        resultSet = self._repo.query(querySimpleSelect)
        assert isInResultSet(resultSet, self._testContent2)

    def testPropertyWithAccent(self):
        """Find content matching cmis:name property"""
        name = self._testContent2.getProperties()['cmis:name']
        new_name = u'éà€ô' + name
        self._testContent2.updateProperties({'cmis:name': new_name})
        querySimpleSelect = "SELECT * FROM cmis:document where " \
                            "cmis:name = '" + new_name + "'"
        resultSet = self._repo.query(querySimpleSelect)
        assert isInResultSet(resultSet, self._testContent2)

    @skipIfAlfrescoBrowserBinding
    def testFullText(self):
        """Find content using a full-text query"""
        queryFullText = "SELECT cmis:objectId, cmis:name FROM cmis:document " \
                        "WHERE contains('whitepaper')"
        # on the first full text search the indexer may need a chance to
        # do its thing
        found = False
        maxTries = self.max_full_text_tries
        while not found and (maxTries > 0):
            resultSet = self._repo.query(queryFullText)
            found = isInResultSet(resultSet, self._testContent2)
            if not found:
                maxTries -= 1
                print(
                    'Not found...sleeping for 10 secs. Remaining tries:%d'
                    % maxTries)
                sleep(10)
        assert found

    @skipIfAlfrescoPubBinding
    @skipIfAlfrescoBrowserBinding
    def testScore(self):
        """Find content using FT, sorted by relevance score"""
        queryScore = "SELECT cmis:objectId, cmis:name, Score() as relevance " \
                     "FROM cmis:document WHERE contains('sample') " \
                     "order by relevance DESC"

        # on the first full text search the indexer may need a chance to
        # do its thing
        found = False
        maxTries = self.max_full_text_tries
        while not found and (maxTries > 0):
            resultSet = self._repo.query(queryScore)
            found = isInResultSet(resultSet, self._testContent2)
            if not found:
                maxTries -= 1
                print('Not found...sleeping for 10 secs. Remaining tries:%d'
                      % maxTries)
                sleep(10)
        assert found
