import os
from setuptools import setup, find_packages

version = '0.4'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cmislib",
    description = 'CMIS client library for Python',
    version = version,
    author = 'Jeff Potts',
    author_email = 'jeffpotts01@gmail.com',
    license = 'Apache',
    url = 'http://code.google.com/p/cmislib/',
    package_dir = {'':'src'},
    packages = find_packages("src"),
    include_package_data = True,
    long_description = read('README.txt'),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        ],
)
