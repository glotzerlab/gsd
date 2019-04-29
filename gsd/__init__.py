# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

""" The GSD main module

The main package :py:mod:`gsd` is the root package. It holds submodules
and does not import them. Users import the modules they need into their python
script::

    import gsd.fl
    f = gsd.fl.GSDFile('filename', 'rb');

Attributes:
    __version__ (str): GSD software version number. This is the version number of the software package as a whole,
                       not the file layer version it reads/writes.
"""

__version__ = "1.7.0";
