# Copyright (c) 2016-2023 The Regents of the University of Michigan
# Part of GSD, released under the BSD 2-Clause License.

"""The GSD main module.

The main package :py:mod:`gsd` is the root package. It holds the submodules
:py:mod:`gsd.fl` and :py:mod:`gsd.hoomd`, but does not import them by default.
You must explicitly import these modules before use::

    import gsd.fl

    import gsd.hoomd

Attributes:
    __version__ (str): GSD software version number. This is the version number
                       of the software package as a whole,
                       not the file layer version it reads/writes.
"""

import signal
import sys
from .version import __version__  # noqa: F401

# Install a SIGTERM handler that gracefully exits, allowing open files to flush
# buffered writes and close.
signal.signal(signal.SIGTERM, lambda n, f: sys.exit(128))
