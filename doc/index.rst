.. Copyright (c) 2016-2022 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

GSD documentation
+++++++++++++++++

The **GSD** file format is the native file format for `HOOMD-blue <https://glotzerlab.engin.umich.edu/hoomd-blue/>`_.
**GSD** files store trajectories of the HOOMD-blue system state in a binary file with efficient random access to
frames. **GSD** allows all particle and topology properties to vary from one frame to the next. Use the **GSD** Python
API to specify the initial condition for a HOOMD-blue simulation or analyze trajectory output with a script. Read a
**GSD** trajectory with a visualization tool to explore the behavior of the simulation.

* `GitHub Repository <https://github.com/glotzerlab/gsd>`_: **GSD** source code and issue tracker.
* `HOOMD-blue <https://glotzerlab.engin.umich.edu/hoomd-blue/>`_: Simulation engine that reads and writes GSD files.
* `hoomd-users Google Group <https://groups.google.com/d/forum/hoomd-users>`_:
  Ask questions to the **HOOMD-blue** community.
* `freud <https://freud.readthedocs.io>`_: A powerful set of tools for analyzing trajectories.
* `OVITO <https://www.ovito.org/>`_: The Open Visualization Tool works with GSD files.
* `gsd-vmd plugin <https://github.com/mphoward/gsd-vmd>`_: VMD plugin to support GSD files.

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
    cli
    c-api
    specification

.. toctree::
    :maxdepth: 1
    :caption: Contributing

    contributing
    style

.. toctree::
    :maxdepth: 1
    :caption: Additional information

    credits
    license
    indices
