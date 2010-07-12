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
