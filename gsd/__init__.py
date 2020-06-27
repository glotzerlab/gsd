# Copyright (c) 2016-2020 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under
# the BSD 2-Clause License.

"""The GSD main module.

The main package :py:mod:`gsd` is the root package. It holds submodules
and does not import them. Users import the modules they need into their python
script::

    import gsd.fl
    f = gsd.fl.GSDFile('filename', 'rb');

Attributes:
    __version__ (str): GSD software version number. This is the version number
                       of the software package as a whole,
                       not the file layer version it reads/writes.
"""

import sys
from .version import __version__  # noqa: F401

if sys.version_info < (3, 5) or sys.version_info >= (4, 0):
    raise RuntimeError("Python ~= 3.5 is required")
