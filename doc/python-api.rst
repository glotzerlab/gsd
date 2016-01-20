GSD python package
==================

GSD comes with an optional python API. This is the most convenient way for
users to read and write GSD files. Developers, or users not working with
the python language, may want to use the :ref:`c_api_` directly.

Submodules
----------

.. toctree::
   :maxdepth: 3

   python-module-gsd.fl

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
