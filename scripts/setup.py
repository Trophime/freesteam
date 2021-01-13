from setuptools import setup, dist
from setuptools.command.install import install
import os

# force setuptools to recognize that this is
# actually a binary distribution
class BinaryDistribution(dist.Distribution):
    def has_ext_modules(foo):
        return True

# optional, use README.md as long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.txt')) as f:
    long_description = f.read()

setup(
    # this package is called mymodule
    name='freesteam',

    # this package contains one module,
    # which resides in the subdirectory mymodule
    # packages=['freesteam.py'],

    # make sure the shared library is included
    package_data={'freesteam': ['freesteam.py', '_freesteam.so']},
    include_package_data=True,

    description="Python3 binding for freesteam library",
    # optional, the contents of README.md that were read earlier
    long_description=long_description,
    long_description_content_type="text/txt",

    # See class BinaryDistribution that was defined earlier
    distclass=BinaryDistribution,

    version='2.2.1',
    url='http://freesteam.sourceforge.net/',
    author='John Pye',
    author_email='john.pye@anu.edu.au',
    # ...
)
