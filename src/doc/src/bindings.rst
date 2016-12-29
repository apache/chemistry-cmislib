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

Bindings
========

The CMIS specification supports multiple bindings. You can think of a binding as
a communication protocol. The specification provides for three bindings:

 * Atom Pub
 * Browser (JSON)
 * Web Services (SOAP)

Although the spec supports three, cmislib supports only two of these bindings:
Atom Pub and Browser.

When instantiating a :class:`CmisClient`, if you do not specify a binding, cmislib
will use the Atom Pub binding, by default.

To use a different binding, such as the Browser binding, import it, then pass it
to the CmisClient constructor, like this:

    >>> from cmislib.browser.binding import BrowserBinding
    >>> client = CmisClient('http://localhost:8080/alfresco/api/-default-/cmis/versions/1.1/browser', 'admin', 'admin', binding=BrowserBinding())

Make sure you specify the appropriate service URL for the binding you've chosen,
otherwise cmislib will be unable to parse the response appropriately.

Each of the two bindings modules contain implementations of the classes defined
in :mod:`cmislib.domain`. So, for example, if you execute a query that returns
documents and you are using the Atom Pub binding, what you'll get back are instances
of :class:`cmislib.atompub.AtomPubDocument` which implements :class:`cmislib.domain.Document`.

The :mod:`cmislib.atompub` Module
---------------------------------

.. automodule:: cmislib.atompub
   :members:

The :mod:`cmislib.browser` Module
---------------------------------

.. automodule:: cmislib.browser
   :members:
