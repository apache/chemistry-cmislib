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
