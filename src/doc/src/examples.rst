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

.. _examples:

========
Examples
========
There's nothing in cmislib that is specific to any particular vendor. Once you give it your CMIS provider's service URL and some credentials, it figures out where to go from there.

Let's look at some examples using a local install of Alfresco Community Edition.

-----------------------
Get a Repository object
-----------------------

 #. From the command-line, start the Python shell by typing `python` then hit enter.
 #. Import the CmisClient:

    >>> from cmislib import CmisClient

 #. Point the CmisClient at the repository's service URL

    >>> client = CmisClient('http://localhost:8080/alfresco/api/-default-/public/cmis/versions/1.1/atom', 'admin', 'admin')

 #. Get the default repository for the service

    >>> repo = client.defaultRepository
    >>> repo.id
    u'-default-'

 #. Get the repository's properties. This for-loop spits out everything cmislib knows about the repo.

    >>> repo.name
    u''
    >>> info = repo.info
    >>> for k,v in info.items():
        ...     print "%s:%s" % (k,v)
        ...
        cmisVersionSupported:1.1
        principalAnonymous:guest
        principalAnyone:GROUP_EVERYONE
        repositoryDescription:None
        changesOnType:cmis:folder
        changesIncomplete:true
        productVersion:5.2.0 (r133656-b12)
        rootFolderId:000f9013-af35-430e-912f-67328f106279
        repositoryId:-default-
        repositoryName:None
        vendorName:Alfresco
        productName:Alfresco Community

-------------------
Folders & Documents
-------------------

Once you've got the Repository object you can start working with folders.

 #. Create a new folder in the root. You should name yours something unique.

    >>> root = repo.rootFolder
    >>> someFolder = root.createFolder('someFolder')
    >>> someFolder.id
    u'92133bfd-8b69-4e97-9af2-761a09f29e01'

 #. Then, you can create some content:

    >>> someFile = open('test.txt', 'r')
    >>> someDoc = someFolder.createDocument('Test Document', contentFile=someFile)

 #. And, if you want, you can dump the properties of the newly-created document (this is a partial list):

    >>> props = someDoc.properties
    >>> for k,v in props.items():
    ...     print '%s:%s' % (k,v)
    ...
    cmis:contentStreamMimeType:text/plain
    cmis:creationDate:2016-12-29 14:53:47.430000-06:00
    cmis:baseTypeId:cmis:document
    cmis:isLatestMajorVersion:false
    cmis:isImmutable:false
    cmis:isMajorVersion:false
    cmis:objectId:c4bc9d00-5bf0-404d-8f0a-a6260f6d21ae;1.0

----------------------------------
Searching For & Retrieving Objects
----------------------------------

There are several different ways to grab an object:
 * You can run a CMIS query
 * You can ask the repository to give you one for a specific path or object ID
 * You can traverse the repository using a folder's children and/or descendants

 #. Let's find the doc we just created with a full-text search.

    >>> results = repo.query("select * from cmis:document where contains('test')")
    >>> for result in results:
    ...     print result.name
    ...
    Test Document2
    example test script.js

 #. Alternatively, you can also get objects by their path, like this:

    >>> someDoc = repo.getObjectByPath('/someFolder/Test Document')
    >>> someDoc.id
    'c4bc9d00-5bf0-404d-8f0a-a6260f6d21ae;1.0'

 #. Or their object ID, like this:

    >>> someDoc = repo.getObject('c4bc9d00-5bf0-404d-8f0a-a6260f6d21ae;1.0')
    >>> someDoc.name
    u'Test Document'

 #. Folder objects have getChildren() and getDescendants() methods that will return a list of :class:`CmisObject` objects:

	>>> children = someFolder.getChildren()
	>>> for child in children:
	...     print child.name
	...
	Test Document
	Test Document2
