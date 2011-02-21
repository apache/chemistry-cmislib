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

#
# Override these settings with values to match your environment.
#
# CMIS repository's service URL
#REPOSITORY_URL = 'http://cmis.alfresco.com/s/cmis'
#REPOSITORY_URL = 'http://localhost:8080/cmis/repository' # Apache Chemistry
#REPOSITORY_URL = 'http://cmis.dnsdojo.com:8080/p8cmis/resources/DaphneA/Service'
#REPOSITORY_URL = 'http://cmis.dnsdojo.com:8080/p8cmis/'
#REPOSITORY_URL = 'http://localhost:8080/alfresco/s/api/cmis'  # Alfresco
#REPOSITORY_URL = 'http://cmis.demo.nuxeo.org/nuxeo/atom/cmis' # Nuxeo demo
#REPOSITORY_URL = 'http://localhost:8080/nuxeo/atom/cmis' # Nuxeo local
#REPOSITORY_URL = 'http://localhost:8080/opencmis/atom'  # OpenCMIS from the OpenText guys
#REPOSITORY_URL = 'http://ec2-174-129-218-67.compute-1.amazonaws.com/cmis/atom' #OpenText on Amazon
REPOSITORY_URL = 'http://localhost:8080/opencmis-inmemory/atom'  # Apache Chemistry OpenCMIS

# CMIS repository credentials
#USERNAME = 'admin'
#PASSWORD = 'admin'
#USERNAME = 'Administrator'  # Nuxeo
#PASSWORD = 'Administrator'  # Nuxeo
#USERNAME = 'CEMPAdmin' # IBM
#PASSWORD = 'CEMPAdmin' # IBM
USERNAME = ''
PASSWORD = ''
#USERNAME = 'cmisuser'
#PASSWORD = 'otcmis'
EXT_ARGS = {}
#EXT_ARGS = {'alf_ticket': 'TICKET_cef29079d8d5341338bf372b08278bc30ec89380'}
# Absolute path to a directory where test folders can be created, including
# the trailing slash.
#TEST_ROOT_PATH = '/default-domain/jeff test'  # No trailing slash
TEST_ROOT_PATH = '/cmislib'  # No trailing slash
#TEST_ROOT_PATH = '/'
# Binary test files. Assumed to exist in the same dir as this python script
TEST_BINARY_1 = '250px-Cmis_logo.png'
TEST_BINARY_2 = 'sample-a.pdf'
# For repositories that support setting an ACL, the name of an existing
# principal ID to add to the ACL of a test object. Some repositories care
# if this ID doesn't exist. Some repositories don't.
TEST_PRINCIPAL_ID = 'tuser1'
# For repositories that may index test content asynchronously, the number of
# times a query is retried before giving up.
MAX_FULL_TEXT_TRIES = 10
# The number of seconds the test should sleep between tries.
FULL_TEXT_WAIT = 10
