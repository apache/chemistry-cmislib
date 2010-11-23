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

Documentation
=============

This documentation was generated with `Sphinx <http://sphinx.pocoo.org/>`_. To install Sphinx on Mac OS X using Macports:

MAC OS X::

    sudo port install py26-sphinx

Once you've got Sphinx installed, if you need to regenerate the documentation::

    cd /path/to/cmislib/src/doc/src
    Run either:    
    	sphinx-build -b html -d ../build/.doctrees . ../build
	make html

The generated HTML will be placed in doc/build::

    firefox file:///path/to/cmislib/src/doc/build/index.html
