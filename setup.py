# Copyright (c) 2016-2022 The Regents of the University of Michigan
# Part of GSD, released under the BSD 2-Clause License.

from setuptools import setup
from setuptools.extension import Extension
import numpy
import os
from Cython.Build import cythonize

extensions = cythonize(
    [Extension(
        'gsd.fl',
        sources=['gsd/fl.pyx', 'gsd/gsd.c'],
        include_dirs=[numpy.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
        )],
    compiler_directives={'language_level': 3})

# Read README for PyPI, fallback to short description if it fails.
desc = 'General simulation data file format.'
try:
    readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'README.md')
    with open(readme_file) as f:
        readme = f.read()
except ImportError:
    readme = desc


setup(name='gsd',
      version='2.6.0',
      description=desc,
      long_description=readme,
      long_description_content_type='text/markdown',
      license='BSD - 2 clause',
      author='Joshua A. Anderson',
      author_email='joaander@umich.edu',
      url='https://gsd.readthedocs.io',
      download_url='https://github.com/glotzerlab/gsd/releases/download/v2.6.0'
                   '/gsd-v2.6.0.tar.gz',
      project_urls={
          "Documentation": "https://gsd.readthedocs.io",
          "Source Code": "https://github.com/glotzerlab/gsd",
          "Issue Tracker": "https://github.com/glotzerlab/gsd/issues",
      },

      classifiers=[
          "Development Status :: 5 - Production/Stable",
          'Intended Audience :: Developers',
          "Intended Audience :: Science/Research",
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          "License :: OSI Approved :: BSD License",
          "Topic :: Scientific/Engineering :: Physics",
          ],

      install_requires=['numpy>=1.9.3'],
      python_requires='>=3.6',
      ext_modules=extensions,
      packages=['gsd', 'gsd.test'],
      package_data={'gsd': ['test/*.gsd']},
      entry_points={
          'console_scripts': [
              'gsd = gsd.__main__:main',
          ],
      }
      )
