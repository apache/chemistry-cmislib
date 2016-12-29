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
   See the wiki for other known CMIS test servers.

If everything goes well, you should see::

   Ran X tests in 3.607s

   OK

.. note::
  Depending on the implementation of the CMIS provider, you may see errors or failures instead of 'OK'.
