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
      version='2.4.0',
      description=desc,
      long_description=readme,
      long_description_content_type='text/markdown',
      license='BSD - 2 clause',
      author='Joshua A. Anderson',
      author_email='joaander@umich.edu',
      url='https://gsd.readthedocs.io',
      download_url='http://glotzerlab.engin.umich.edu/Downloads/'
                   'gsd/gsd-v2.4.0.tar.gz',

      classifiers=[
          "Development Status :: 5 - Production/Stable",
          'Intended Audience :: Developers',
          "Intended Audience :: Science/Research",
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          "License :: OSI Approved :: BSD License",
          "Topic :: Scientific/Engineering :: Physics",
          ],

      install_requires=['cython>=0.29.0,<1', 'numpy>=1.9.3,<2'],
      python_requires='~=3.5',
      ext_modules=extensions,
      packages=['gsd', 'gsd.test'],
      package_data={'gsd': ['test/*.gsd']},
      entry_points={
          'console_scripts': [
              'gsd = gsd.__main__:main',
          ],
      }
      )
