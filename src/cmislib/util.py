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
"""
Module containing handy utility functions.
"""
import re
import iso8601
import logging
from cmislib.domain import CmisId, Document, Folder

moduleLogger = logging.getLogger('cmislib.util')

def multiple_replace(aDict, text):

    """
    Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new string.

    See http://code.activestate.com/recipes/81330/
    """

    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, aDict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: aDict[mo.string[mo.start():mo.end()]], text)

def parsePropValue(value, nodeName):

    """
    Returns a properly-typed object based on the type as specified in the
    node's element name.
    """

    moduleLogger.debug('Inside parsePropValue')

    if nodeName == 'propertyId':
        return CmisId(value)
    elif nodeName == 'propertyString':
        return value
    elif nodeName == 'propertyBoolean':
        bDict = {'false': False, 'true': True}
        return bDict[value.lower()]
    elif nodeName == 'propertyInteger':
        return int(value)
    elif nodeName == 'propertyDecimal':
        return float(value)
    elif nodeName == 'propertyDateTime':
        #%z doesn't seem to work, so I'm going to trunc the offset
        #not all servers return microseconds, so those go too
        return parseDateTimeValue(value)
    else:
        return value


def parseDateTimeValue(value):

    """
    Utility function to return a datetime from a string.
    """
    return iso8601.parse_date(value)


def parseBoolValue(value):

    """
    Utility function to parse booleans and none from strings
    """

    if value == 'false':
        return False
    elif value == 'true':
        return True
    elif value == 'none':
        return None
    else:
        return value


def toCMISValue(value):

    """
    Utility function to convert Python values to CMIS string values
    """

    if value == False:
        return 'false'
    elif value == True:
        return 'true'
    elif value == None:
        return 'none'
    else:
        return value


