Python API
==========

GSD comes with an optional python API. This is the most convenient way for
users to read and write GSD files. Developers, or users not working with
the python language, may want to use the `c_api_` directly.

The main package :py:mod:`gsd` is the root package. It holds the submodules
and does not import them. Users import the modules they need into their python
script::

    import gsd.fl
    f = gsd.fl.GSDFile('filename', 'r');

.. automodule:: gsd
    :synopsis: GSD main module.
    :members:

**Modules:**

.. toctree::
   :maxdepth: 2

   python-module-gsd.fl
