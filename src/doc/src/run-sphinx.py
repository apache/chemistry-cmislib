#!/usr/bin/python
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
