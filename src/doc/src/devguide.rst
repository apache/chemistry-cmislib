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

===============
Developer Guide
===============

This page is for people who wish to contribute code to this project.

Developer Setup
---------------
Check out the source from head, switch to the source code's root directory, then run:
  python setup.py develop
  
That will set up this project's src directory in the easy-install.pth file in site-packages.

Release Process
---------------

Checklist:
 #. All newly-added code has a unit test
 #. All tests pass cleanly (or have good reasons for not passing)
 #. Change setup.cfg to have the appropriate tag ('dev', for example, or '' for a stable release)
 #. Change setup.py to have the appropriate version number
 #. Inline comments updated with changes
 #. Sphinx doc updated with changes
 #. Docs build cleanly
     .. code-block:: bash

        cd src/doc/src/
        make html

 #. pep8 runs without much complaint
     .. code-block:: bash

        pep8 --ignore=E501,W601 --repeat model.py

 #. pylint runs without much complaint
     .. code-block:: bash

        pylint --disable=C0103,R0904,R0913,C0301,W0511 cmislibtest.py

 #. All changes checked in
 #. Tag the release using 'cmislib-[release num]-RC[x]'
 #. Use the release script to build the release artifacts
     .. code-block:: bash

        cd dist
        ./release.sh -u jpotts@apache.org

    This will do a 'setup.py bdist sdist' and will then sign all artifacts.

    Note that the artifacts will be named without 'RC[x]'. These are the same artifacts that will be distributed if the vote passes.

 #. Copy files to the Apache server under ~/public_html/chemistry/cmislib/[release num]
 #. Start vote. Send an email to dev@chemistry.apache.org announcing the vote, highlighting the changes, pointing to the tagged source, and referencing the artifacts that have been copied to the Apache server.
 #. After 72 hours, if the vote passes, continue, otherwise address issues and start over
 #. Copy the files to the appropriate Apache dist directory, which is /www/www.apache.org/dist/chemistry/cmislib/[release num]
 #. Rename the RC tag in source code control
 #. Update the cmislib home page with download links to the new release
 #. Upload files to Pypi
 #. Check the `cheesecake <http://pycheesecake.org/>`_ score
     .. code-block:: bash

        python cheesecake_index --name=cmislib

