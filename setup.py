# Copyright (c) 2016-2023 The Regents of the University of Michigan
# Part of GSD, released under the BSD 2-Clause License.

from setuptools import setup
from setuptools.extension import Extension
import numpy
from Cython.Build import cythonize

extensions = cythonize(
    [Extension(
        'gsd.fl',
        sources=['gsd/fl.pyx', 'gsd/gsd.c'],
        include_dirs=[numpy.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
        )],
    compiler_directives={'language_level': 3})

setup(ext_modules=extensions)
