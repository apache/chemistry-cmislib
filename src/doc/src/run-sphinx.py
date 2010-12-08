#!/usr/bin/python
import os
import sys
print sys.path[0]
os.environ['BUILDDIR']=sys.path[0] + "/../build"
os.environ['SOURCEDIR']=sys.path[0]
os.system("make -e --makefile=" + sys.path[0] + "/Makefile html")
