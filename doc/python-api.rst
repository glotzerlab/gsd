.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

gsd Python package
==================

**GSD** provides a **Python** API. Use the `gsd.hoomd` module to read and write files for
HOOMD-blue.

Submodules
----------

.. toctree::
   :maxdepth: 1

   python-module-gsd.fl
   python-module-gsd.hoomd
   python-module-gsd.pygsd
   python-module-gsd.version

Package contents
----------------

.. automodule:: gsd
    :synopsis: GSD main module.
    :members:

Logging
-------

All Python modules in **GSD** use the Python standard library module :py:mod:`logging` to log
events. Use this module to control the verbosity and output destination::

    import logging
    logging.basicConfig(level=logging.INFO)

.. seealso::

    Module :py:mod:`logging`
        Documentation of the :py:mod:`logging` standard module.

Signal handling
---------------

On import, `gsd` installs a ``SIGTERM`` signal handler that calls `sys.exit` so that open gsd files
have a chance to flush write buffers (`GSDFile.flush`) when a user's process is terminated. Use
`signal.signal` to adjust this behavior as needed.
