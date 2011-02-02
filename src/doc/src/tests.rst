..
   Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

.. _tests:

=====
Tests
=====

This code includes unit tests. To run the tests::

   cd /path/to/cmislib/tests
   Edit settings.py
   Set REPOSITORY_URL, USERNAME, PASSWORD
   Optionally, set TEST_ROOT_PATH and other settings to meet your needs
   python cmislibtest.py

.. note::
   http://cmis.alfresco.com is a freely-available, hosted CMIS service. If you want to use that for testing, the URL is http://cmis.alfresco.com/s/cmis and the username and password are admin/admin. See the wiki for other known CMIS test servers.

If everything goes well, you should see::

   Ran X tests in 3.607s

   OK

.. note::
   Until the CMIS specification is ratified, and depending on the implementation of the CMIS provider, you may see errors or failures instead of 'OK'. See the `Known Issues <http://code.google.com/p/cmislib/wiki/KnownIssues>`_ page on the cmislib wiki for a list of known test failures by CMIS provider.
