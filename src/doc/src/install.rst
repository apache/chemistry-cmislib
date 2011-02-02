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

Installation
============

Requirements
------------
These requirements must be met:
 - Python 2.6.x
 - CMIS provider compliant with CMIS 1.0

Steps
-----
 #. If you don't have `Python <http://www.python.org>`_ installed already, do so.
 #. If you don't have `setuptools <http://pypi.python.org/pypi/setuptools>`_ installed already, do so.
 #. Once setuptools is installed, type `easy_install cmislib`
 #. That's it! 

Once you do that, you should be able to fire up Python on the command-line and import cmislib successfully.

  >>> from cmislib import CmisClient, Repository, Folder

To validate everything is working, run some :ref:`tests` or walk through some :ref:`examples`.
