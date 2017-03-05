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
Unit tests for logic unique to the Browser binding
"""

import unittest
from unittest import TestSuite, TestLoader
from cmislib.browser.binding import BrowserACE
from cmislib.browser.binding import BrowserACL


class BrowserACLTest(unittest.TestCase):

    def setUp(self):
        self.aceUser1 = BrowserACE(
            principalId='user1',permissions='cmis:read', direct=True)
        self.aceUser2 = BrowserACE(
            principalId='user2', permissions=['cmis:read', 'cmis:write'],
            direct=False)
        self.acl = BrowserACL(aceList=[self.aceUser1, self.aceUser2])

    def test_original_entries(self):
        originalEntries = self.acl.originalEntries
        for entry in [self.aceUser1, self.aceUser2]:
            copy = originalEntries.get(entry.principalId)
            self.assertTrue(copy)
            # check we have 2 different instances of the same object
            self.assertNotEquals(id(entry), id(copy))
            self.assertEqual(entry, copy)

    def test_get_removed_aces(self):
        # test the complete removal of an alc entry
        self.acl.removeEntry(self.aceUser1.principalId)
        removedAces = self.acl.getRemovedAces()
        self.assertEqual(len(removedAces), 1)
        self.assertEqual(removedAces[0], self.aceUser1)
        # test partial removal of an entry (delete all + add an existing one
        #  with same direct)
        self.acl.removeEntry(self.aceUser2.principalId)
        self.acl.addEntry(self.aceUser2.principalId, 'cmis:write',
                          direct=False)
        removedAces = self.acl.getRemovedAces()
        self.assertEqual(len(removedAces), 2)
        toCheck = None
        for removedAce in removedAces:
            if removedAce.principalId == self.aceUser2.principalId:
                toCheck = removedAce
        self.assertTrue(toCheck)
        self.assertEqual(toCheck.principalId, self.aceUser2.principalId)
        self.assertListEqual(toCheck.permissions, ['cmis:read'])

    def test_get_added_aces(self):
        # add new entry for a new princpal
        self.acl.addEntry('user3', 'cmis:all')
        addedAces = self.acl.getAddedAces()
        self.assertEqual(len(addedAces), 1)
        self.assertEqual(addedAces[0], BrowserACE('user3', 'cmis:all', True))
        # add a new entry for the same principal
        self.acl.addEntry(
            'user3', ['cmis:all', 'cmis:write'])
        addedAces = self.acl.getAddedAces()
        self.assertEqual(len(addedAces), 1)
        self.assertEqual(
            addedAces[0],
            BrowserACE('user3', ['cmis:all', 'cmis:write'], True))
        # add a new entry for an exising principal
        self.acl.addEntry(
            self.aceUser1.principalId, ['cmis:read','cmis:write'])
        addedAces = self.acl.getAddedAces()
        self.assertEqual(len(addedAces), 2)
        toCheck = None
        for addedAce in addedAces:
            if addedAce.principalId == self.aceUser1.principalId:
                toCheck = addedAce
        self.assertTrue(toCheck)
        self.assertEqual(
            toCheck,
            BrowserACE(self.aceUser1.principalId, ['cmis:write'], True))

if __name__ == "__main__":
    tts = TestSuite()
    tts.addTests(TestLoader().loadTestsFromTestCase(BrowserACLTest))
    unittest.TextTestRunner().run(tts)
