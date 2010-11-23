..
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

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
 #. All changes checked in
 #. pep8 runs without much complaint
     * pep8 --ignore=E501,W601 --repeat model.py

 #. pylint runs without much complaint
     * pylint --disable-msg=C0103,R0904,R0913,C0301,W0511 cmislibtest.py

 #. Inline comments updated with changes
 #. Sphinx doc updated with changes
 #. Docs built cleanly
     * cd src/doc/src/
     * make html

 #. Setuptools build
     * python setup.py bdist sdist
 #. Upload egg and tar to Google Code downloads
 #. Make new downloads featured, old downloads deprecated
 #. Pypi update
     * python setup.py upload

 #. Tag the release in Subversion
 #. Check the `cheesecake <http://pycheesecake.org/>`_ score
     * python cheesecake_index --name=cmislib

