Installation
============

Requirements
------------
These requirements must be met:
 - Python 2.6.x
 - CMIS provider compliant with CMIS 1.0 Committee Draft 04
 
   - Alfresco 3.2r2 (`Download <http://wiki.alfresco.com/wiki/Download_Alfresco_Community_Network>`_)

Steps
-----
 #. If you don't have `Python <http://www.python.org>`_ installed already, do so.
 #. If you don't have `setuptools <http://pypi.python.org/pypi/setuptools>`_ installed already, do so.
 #. Once setuptools is installed, type `easy_install cmislib`
 #. That's it! 

Once you do that, you should be able to fire up Python on the command-line and import cmislib successfully.

  >>> from cmislib.model import CmisClient, Repository, Folder

To validate everything is working, run some :ref:`tests` or walk through some :ref:`examples`.