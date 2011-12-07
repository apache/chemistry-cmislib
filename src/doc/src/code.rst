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

Code
====

The :mod:`cmislib.model` Module
-------------------------------

The :mod:`cmislib.model` Module contains all the CMIS domain objects. The ones you will work with are listed as top level package elements. When working with the repository, the first thing you need to do is grab an instance of :class:`cmislib.CmisClient`, passing it the repository endpoint URL, username, and password.

For example, in Alfresco 4 and higher, the repository endpoint is
'http://localhost:8080/alfresco/cmisatom'. In earlier versions of
Alfresco, the endpoint is
'http://localhost:8080/alfresco/s/api/cmis'. In both cases, the
default username and password are 'admin' and 'admin'.

>>> cmisClient = cmislib.CmisClient('http://localhost:8080/alfresco/s/cmis', 'admin', 'admin')

From there you can get the default repository...

>>> repo = cmisClient.defaultRepository

or a specific repository if you know the repository ID.

>>> repo = cmisClient.getRepository('83beb297-a6fa-4ac5-844b-98c871c0eea9')

Once you have that, you're off to the races. Use the :class:`cmislib.Repository` class to create new :class:`cmislib.Folder` and :class:`cmislib.Document` objects, perform searches, etc.

.. automodule:: cmislib.model
   :members:

The :mod:`cmislib.net` Module
-----------------------------

The :mod:`cmislib.net` Module contains the classes used by :mod:`cmislib.model.CmisClient` to communicate with the CMIS repository. The most important of which is :class:`cmislib.net.RESTService`.

.. automodule:: cmislib.net
   :members: RESTService
   
The :mod:`cmislib` Module
-------------------------------

The :mod:`tests.cmislibtest` Module contains unit tests for all classes and methods in :mod:`cmislib.model`. See :ref:`tests` for more information on running tests.

.. automodule:: tests.cmislibtest
   :members:
