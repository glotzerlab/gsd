from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy
import sys
import hashlib
import os

current_checksum = hashlib.sha256()
with open('gsd/fl.pyx') as f:
    current_checksum.update(f.read().encode('UTF-8'))
with open('gsd/fl.pyx.sha256') as f:
    existing_checksum = f.read();

if existing_checksum.strip() != current_checksum.hexdigest():
    print('fl.pyx has been updated, it needs to be cythonized before setup.py can continue.');
    sys.exit(1);

fl = Extension('gsd.fl',
               sources=['gsd/fl{0}.c'.format(sys.version_info.major), 'gsd/gsd.c'],
               include_dirs = [numpy.get_include()]
               )

# Read README for PyPI, fallback to short description if it fails.
desc = 'General simulation data file format.'
try:
    readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'README.md')
    with open(readme_file) as f:
        readme = f.read()
except ImportError:
    readme = desc


setup(name = 'gsd',
      version = '1.7.0',
      description = desc,
      long_description = readme,
      long_description_content_type='text/markdown',
      license = 'BSD - 2 clause',
      author = 'Joshua A. Anderson',
      author_email = 'joaander@umich.edu',
      url = 'https://gsd.readthedocs.io',
      download_url = 'http://glotzerlab.engin.umich.edu/Downloads/gsd/gsd-v1.7.0.tar.gz',

        classifiers=[
            "Development Status :: 5 - Production/Stable",
            'Intended Audience :: Developers',
            "Intended Audience :: Science/Research",
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            "License :: OSI Approved :: BSD License",
            "Topic :: Scientific/Engineering :: Physics",
        ],

      install_requires=['numpy>=1.9.3,<2'],
      ext_modules = [fl],
      packages = ['gsd']
     )
