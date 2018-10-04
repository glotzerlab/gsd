.. Copyright (c) 2016-2018 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

GSD documentation
+++++++++++++++++

GSD (General Simulation Data) is a file format specification and a library to read and write it. The package also
contains a python module that reads and writes `hoomd <https://glotzerlab.engin.umich.edu/hoomd-blue/>`_ schema gsd
files with an easy to use syntax.

GSD files:

* Efficiently store many frames of data from simulation runs.
* High performance file read and write.
* Support arbitrary chunks of data in each frame (position, orientation, type, etc...).
* Append frames to an existing file with a monotonically increasing frame number.
* Resilient to job kills.
* Variable number of named chunks in each frame.
* Variable size of chunks in each frame.
* Each chunk identifies data type.
* Common use cases: NxM arrays in double, float, int, char types.
* Generic use case: binary blob of N bytes.
* Easy to integrate into other tools with python, or a C API (< 1k lines).
* Fast random access to frames.

.. toctree::
    :maxdepth: 1
    :caption: Getting started

    installation
    changes
    community

.. toctree::
    :maxdepth: 1
    :caption: Tutorials

    hoomd-examples
    fl-examples

.. toctree::
    :maxdepth: 1
    :caption: Reference

    python-api
    c-api
    specification
    scripts
    benchmark

.. toctree::
    :maxdepth: 1
    :caption: Additional information

    license
    indices
