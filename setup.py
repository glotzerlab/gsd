from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext
import sys
import hashlib

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

current_checksum = hashlib.sha256()
with open('gsd/fl.pyx') as f:
    current_checksum.update(f.read().encode('UTF-8'))
with open('gsd/fl.pyx.sha256') as f:
    existing_checksum = f.read();

if existing_checksum.strip() != current_checksum.hexdigest():
    print('fl.pyx has been updated, it needs to be cythonized before setup.py can continue.');
    sys.exit(1);

setup(name = 'gsd',
      version = '1.5.2',
      description = 'General simulation data file format.',
      license = 'BSD - 2 clause',
      author = 'Joshua A. Anderson',
      author_email = 'joaander@umich.edu',
      url = 'https://bitbucket.org/glotzer/gsd',
      download_url = 'http://glotzerlab.engin.umich.edu/Downloads/gsd/gsd-v1.5.2.tar.gz',

        classifiers=[
            "Development Status :: 5 - Production/Stable",
            'Intended Audience :: Developers',
            "Intended Audience :: Science/Research",
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            "License :: OSI Approved :: BSD License",
            "Topic :: Scientific/Engineering :: Physics",
        ],

      cmdclass={'build_ext':build_ext},
      setup_requires=['numpy'],
      ext_modules = [Extension('gsd.fl',
               sources=['gsd/fl{0}.c'.format(sys.version_info.major), 'gsd/gsd.c']
               )],
      packages = ['gsd']
     )
