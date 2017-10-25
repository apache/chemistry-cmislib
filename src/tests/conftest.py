# -*- coding: utf-8 -*-
#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#

import os
import tempfile
from collections import namedtuple
from time import time
from time import sleep

import pytest

from cmislib.atompub import AtomPubBinding
from cmislib.browser import BrowserBinding
from cmislib.exceptions import \
    NotSupportedException, RuntimeException
from cmislib.model import CmisClient

CmisEnv = namedtuple(
    'CmisEnv',
    ['env_name',
     'binding',
     'url',
     'user',
     'pwd',
     'versionable_type_id',
     'acl_principal_id',
     'ext_args',
     ]
)


CMIS_ENV_PARAMS = [
    CmisEnv(
        'alfresco',
        BrowserBinding(),
        'http://localhost:80/alfresco/api/-default-/cmis/versions/1.1/browser',
        'admin',
        'admin',
        'cmis:document',
        'anyone',
        {}
    ),
    CmisEnv(
        'alfresco',
        AtomPubBinding(),
        'http://localhost:80/alfresco/api/-default-/cmis/versions/1.1/atom',
        'admin',
        'admin',
        'cmis:document',
        'anyone',
        {}

    )
]


def _make_cmis_env_ids():
    env_ids = []
    for env in CMIS_ENV_PARAMS:
        env_ids.append(
            '{name}-{binding}'.format(
                name=env.env_name,
                binding=env.binding.__class__.__name__
            )
        )
    return env_ids


CMIS_ENV_IDS = _make_cmis_env_ids()
MAX_FULL_TEXT_TRIES = 10


@pytest.fixture(params=CMIS_ENV_PARAMS, ids=CMIS_ENV_IDS)
def cmis_conf(request):
    """Apply config params as attribute on the class"""
    param = request.param
    request.cls.max_full_text_tries = MAX_FULL_TEXT_TRIES
    for field in param._fields:
        setattr(request.cls, field, getattr(param, field))
    request.cls.fixture_id =  '{name}-{binding}'.format(
        name=param.env_name,
        binding=param.binding.__class__.__name__
    )


@pytest.fixture(params=CMIS_ENV_PARAMS, ids=CMIS_ENV_IDS)
def cmis_env(request):
    """Initialize a cmis environement with
    * CmisClient
    * repo
    * rootFolder
    * test folder name
    * test folder
    All these attributes are reset after each test method
    """
    cmis_conf(request)
    param = request.param
    request.cls._cmisClient = CmisClient(
        param.url, param.user, param.pwd, binding=param.binding,
        **param.ext_args)
    request.cls._repo = request.cls._cmisClient.getDefaultRepository()
    request.cls._rootFolder = request.cls._repo.getRootFolder()
    request.cls._folderName = " ".join([
        'cmislib', request.cls.__name__, str(time())])
    request.cls._testFolder = request.cls._rootFolder.createFolder(
        request.cls._folderName)
    yield request
    try:
        request.cls._testFolder.deleteTree()
    except NotSupportedException:
        print("Couldn't delete test folder because deleteTree is not "
              "supported")
    except RuntimeException:
        # deleting a folder could fail if the indexation of a new document
        # is in progress
        sleep(5)
        try:
            request.cls._testFolder.deleteTree()
        except RuntimeException:
            print("Couldn't delete test folder")


TEST_BINARY_1 = '250px-Cmis_logo.png'
TEST_BINARY_2 = 'sample-a.pdf'


@pytest.fixture(scope="class")
def binary_files(request):
    global TEST_BINARY_1
    global TEST_BINARY_2
    my_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        os.stat(TEST_BINARY_1)
    except OSError:
        TEST_BINARY_1 = os.path.join(my_dir, TEST_BINARY_1)
    try:
        os.stat(TEST_BINARY_2)
    except OSError:
        TEST_BINARY_2 = os.path.join(my_dir, TEST_BINARY_2)
    request.cls.binary_file_1 = TEST_BINARY_1
    request.cls.binary_filename_1 = os.path.basename(TEST_BINARY_1)
    request.cls.binary_file_2 = TEST_BINARY_2
    request.cls.binary_filename_2 = os.path.basename(TEST_BINARY_2)


@pytest.fixture()
def cleandir():
    """ Use temp directory as working directory"""
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
