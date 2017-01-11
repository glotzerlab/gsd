.. Copyright (c) 2016-2017 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

gsd python package
==================

GSD provides an optional python API. This is the most convenient way for
users to read and write GSD files. Developers, or users not working with
the python language, may want to use the :ref:`c_api_`.

Submodules
----------

.. toctree::
   :maxdepth: 3

   python-module-gsd.fl
   python-module-gsd.pygsd
   python-module-gsd.hoomd

Package contents
----------------

.. automodule:: gsd
    :synopsis: GSD main module.
    :members:

Logging
-------

All python modules in GSD use the python standard library module :py:mod:`logging`
to log events. Use this module to control the verbosity and output destination::

    import logging
    logging.basicConfig(level=logging.INFO)

.. seealso::

    Module :py:mod:`logging`
        Documenation of the :py:mod:`logging` standard module.
