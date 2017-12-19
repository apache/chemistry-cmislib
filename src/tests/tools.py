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


def isInCollection(collection, targetDoc):
    """
    Util function that searches a list of objects for a matching target
    object.
    """
    for doc in collection:
        # hacking around a bizarre thing in Alfresco which is that when the
        # PWC comes back it has an object ID of say 123ABC but when you look
        # in the checked out collection the object ID of the PWC is now
        # 123ABC;1.0. What is that ;1.0? I don't know, but object IDs are
        # supposed to be immutable so I'm not sure what's going on there.
        if doc.getObjectId().startswith(targetDoc.getObjectId()):
            return True
    return False


def isInResultSet(resultSet, targetDoc):
    """
    Util function that searches a :class:`ResultSet` for a specified target
    object. Note that this function will do a getNext on every page of the
    result set until it finds what it is looking for or reaches the end of
    the result set. For every item in the result set, the properties
    are retrieved. Long story short: this could be an expensive call.
    """
    done = False
    while not done:
        if resultSet.hasObject(targetDoc.getObjectId()):
            return True
        if resultSet.hasNext():
            resultSet.getNext()
        else:
            done = True


def skipIf(fixtureIds):
    def skipIf_decorator(func):
        def func_wrap(self):
            if self.fixture_id in fixtureIds:
                pytest.skip(
                    "%s not supported in %s" % (func, self.fixture_id)
                )
            func(self)
        return func_wrap
    return skipIf_decorator


def skipIfAlfrescoBrowserBinding(func):
    return skipIf(['alfresco-BrowserBinding'])(func)


def skipIfAlfrescoPubBinding(func):
    return skipIf(['alfresco-AtomPubBinding'])(func)
