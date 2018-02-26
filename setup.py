from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy
import sys
import hashlib

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

setup(name = 'gsd',
      version = '1.5.1',
      description = 'General simulation data file format.',
      license = 'BSD - 2 clause',
      author = 'Joshua A. Anderson',
      author_email = 'joaander@umich.edu',
      url = 'https://bitbucket.org/glotzer/gsd',
      download_url = 'http://glotzerlab.engin.umich.edu/Downloads/gsd/gsd-v1.5.1.tar.gz',

        classifiers=[
            "Development Status :: 5 - Production/Stable",
            'Intended Audience :: Developers',
            "Intended Audience :: Science/Research",
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            "License :: OSI Approved :: BSD License",
            "Topic :: Scientific/Engineering :: Physics",
        ],

      install_requires=['numpy'],
      ext_modules = [fl],
      packages = ['gsd']
     )
