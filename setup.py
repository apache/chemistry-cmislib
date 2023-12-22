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
from setuptools import setup, find_packages

version = '0.7.1'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cmislib",
    description='Apache Chemistry CMIS client library for Python',
    version=version,
    install_requires=[
        'iso8601',
        'requests',
        'requests-toolbelt',
        ],
    author='Apache Chemistry Project',
    author_email='dev@chemistry.apache.org',
    license='Apache License (2.0)',
    url='http://chemistry.apache.org/',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests']),
    # include_package_data=True,
    exclude_package_data={'': ['tests']},
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries",
        ],
)
