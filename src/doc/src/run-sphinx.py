#!/usr/bin/python
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
import sys
os.environ['SPHINXBUILD']="sphinx-build"
build_dir = sys.path[0] + "/../build"
os.environ['BUILDDIR']=build_dir
os.environ['SOURCEDIR']=sys.path[0]
# force a clean every time
print "Removing build dir: %s" % build_dir
os.system("rm -rf " + build_dir)
os.system("make -e --makefile=" + sys.path[0] + "/Makefile html")
zip_file = sys.path[0] + "/../docs.zip"
os.system("rm " + zip_file)
os.chdir(build_dir)
os.system("zip -r " + zip_file + " *")
