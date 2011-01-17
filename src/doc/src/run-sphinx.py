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
zip_file = sys.path[0] + "/../docs.zip"
os.system("rm " + zip_file)
os.chdir(build_dir)
os.system("zip -r " + zip_file + " *")
