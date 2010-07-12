.. _examples:

========
Examples
========
There's nothing in cmislib that is specific to any particular vendor. Once you give it your CMIS provider's service URL and some credentials, it figures out where to go from there. But I haven't tested with anything other than Alfresco yet, and this thing is still hot out of the oven. If you want to help test it against other CMIS 1.0cd06 repositories I'd love the help.

Anyway, let's look at some examples using Alfresco's public CMIS repository.

-----------------------
Get a Repository object
-----------------------

 #. From the command-line, start the Python shell by typing `python` then hit enter.
 #. Import the CmisClient:

    >>> from cmislib.model import CmisClient

 #. Point the CmisClient at the repository's service URL 

    >>> client = CmisClient('http://cmis.alfresco.com/s/cmis', 'admin', 'admin')

 #. Get the default repository for the service

    >>> repo = client.defaultRepository
    >>> repo.id
    u'83beb297-a6fa-4ac5-844b-98c871c0eea9'

 #. Get the repository's properties. This for-loop spits out everything cmislib knows about the repo.

    >>> repo.name
    u'Main Repository'
    >>> info = repo.info
    >>> for k,v in info.items():
        ...     print "%s:%s" % (k,v)
        ...
        cmisSpecificationTitle:Version 1.0 Committee Draft 04
        cmisVersionSupported:1.0
        repositoryDescription:None
        productVersion:3.2.0 (r2 2440)
        rootFolderId:workspace://SpacesStore/aa1ecedf-9551-49c5-831a-0502bb43f348
        repositoryId:83beb297-a6fa-4ac5-844b-98c871c0eea9
        repositoryName:Main Repository
        vendorName:Alfresco
        productName:Alfresco Repository (Community)

-------------------
Folders & Documents
-------------------

Once you've got the Repository object you can start working with folders.

 #. Create a new folder in the root. You should name yours something unique.

    >>> root = repo.rootFolder
    >>> someFolder = root.createFolder('someFolder')
    >>> someFolder.id
    u'workspace://SpacesStore/91f344ef-84e7-43d8-b379-959c0be7e8fc'

 #. Then, you can create some content:

    >>> someFile = open('test.txt', 'r')
    >>> someDoc = someFolder.createDocument('Test Document', contentFile=someFile)

 #. And, if you want, you can dump the properties of the newly-created document (this is a partial list):

    >>> props = someDoc.properties
    >>> for k,v in props.items():
    ...     print '%s:%s' % (k,v)
    ...
    cmis:contentStreamMimeType:text/plain
    cmis:creationDate:2009-12-18T10:59:26.667-06:00
    cmis:baseTypeId:cmis:document
    cmis:isLatestMajorVersion:false
    cmis:isImmutable:false
    cmis:isMajorVersion:false
    cmis:objectId:workspace://SpacesStore/2cf36ad5-92b0-4731-94a4-9f3fef25b479

----------------------------------
Searching For & Retrieving Objects
----------------------------------

There are several different ways to grab an object:
 * You can run a CMIS query
 * You can ask the repository to give you one for a specific path or object ID
 * You can traverse the repository using a folder's children and/or descendants
 
 #. Let's find the doc we just created with a full-text search.
  
    .. note::
       Note that I'm currently seeing a problem with Alfresco in which the CMIS service returns one less result than what's really there):

    >>> results = repo.query("select * from cmis:document where contains('test')")
    >>> for result in results:
    ...     print result.name
    ...
    Test Document2
    example test script.js

 #. Alternatively, you can also get objects by their their path, like this:

    >>> someDoc = repo.getObjectByPath('/someFolder/Test Document')
    >>> someDoc.id
    u'workspace://SpacesStore/2cf36ad5-92b0-4731-94a4-9f3fef25b479'

 #. Or their object ID, like this:
 
    >>> someDoc = repo.getObject('workspace://SpacesStore/2cf36ad5-92b0-4731-94a4-9f3fef25b479')
    >>> someDoc.name
    u'Test Document'
 
 #. Folder objects have getChildren() and getDescendants() methods that will return a list of :class:`CmisObject` objects:
 
	>>> children= someFolder.getChildren()
	>>> for child in children:
	...     print child.name
	... 
	Test Document
	Test Document2  
