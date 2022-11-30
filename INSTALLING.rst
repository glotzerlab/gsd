.. Copyright (c) 2016-2022 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

Installation
============

**gsd** binaries are available in the glotzerlab-software_ Docker_/Singularity_ images and in
packages on conda-forge_ and PyPI_. You can also compile **gsd** from source, embed ``gsd.c`` in
your code, or read gsd files with a pure Python reader ``pygsd.py``.

.. _glotzerlab-software: https://glotzerlab-software.readthedocs.io
.. _Docker: https://hub.docker.com/
.. _Singularity: https://www.sylabs.io/
.. _conda-forge: https://conda-forge.org/
.. _PyPI: https://pypi.org/

Binaries
--------

Conda package
^^^^^^^^^^^^^

**gsd** is available on conda-forge_ on the *linux-64*, *linux-aarch64*, *linux-ppc64le*, *osx-64*,
*osx-arm64* and *win-64* platforms. To install, download and install miniforge_ or miniconda_ Then
install **gsd** from the conda-forge_ channel:

.. _miniforge: https://github.com/conda-forge/miniforge
.. _miniconda: http://conda.pydata.org/miniconda.html

.. code-block:: bash

   $ conda install -c conda-forge gsd

Singularity / Docker images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the glotzerlab-software_ documentation for instructions to install and use the containers.

PyPI
^^^^

Use **pip** to install **gsd** binaries:

.. code-block:: bash

   $ python3 -m pip install gsd

Compile from source
-------------------

To build the **gsd** Python package from source:

1. `Install prerequisites`_::

   $ <package-manager> install cmake cython git numpy python pytest

2. `Obtain the source`_::

   $ git clone https://github.com/glotzerlab/gsd

3. `Install with setuptools`_::

   $ python3 -m pip install -e gsd

   **OR** `Build with CMake for development`_::

   $ cmake -B build/gsd -S gsd
   $ cmake --build build/gsd

To run the tests (optional):

1. `Run tests`_::

    $ pytest --pyargs gsd

To build the documentation from source (optional):

1. `Install prerequisites`_::

   $ <package-manager> install sphinx sphinx_rtd_theme ipython

2. `Build the documentation`_::

   $ sphinx-build -b html gsd/doc build/gsd-documentation

The sections below provide details on each of these steps.

.. _Install prerequisites:

Install prerequisites
^^^^^^^^^^^^^^^^^^^^^

**gsd** requires a number of tools and libraries to build.

.. note::

    This documentation is generic. Replace ``<package-manager>`` with your package or module
    manager. You may need to adjust package names and/or install additional packages, such as
    ``-dev`` packages that provide headers needed to build **gsd**.

.. tip::

    Create or use an existing `virtual environment`_, one place where you can install dependencies
    and **gsd**::

        $ python3 -m venv gsd-venv

    You will need to activate your environment before installing or configuring **gsd**::

        $ source gsd-venv/bin/activate

**General requirements:**

* **C compiler** (tested with gcc 7-12, clang 6-14, visual studio 2019-2022)
* **Python** >= 3.6
* **numpy** >= 1.9.3
* **Cython** >= 0.22

**To build the documentation**:

* **Sphinx**
* **IPython**
* an internet connection

**To execute unit tests:**

* **pytest** >= 3.9.0

.. _virtual environment: https://docs.python.org/3/library/venv.html

.. _Obtain the source:

Obtain the source
^^^^^^^^^^^^^^^^^

Clone using Git_::

   $ git clone https://github.com/glotzerlab/gsd

Release tarballs are also available on the `GitHub release pages`_.

.. seealso::

    See the `git book`_ to learn how to work with `Git`_ repositories.

.. _GitHub release pages: https://github.com/glotzerlab/gsd/releases/
.. _git book: https://git-scm.com/book
.. _Git: https://git-scm.com/

.. _Install with setuptools:

Install with setuptools
^^^^^^^^^^^^^^^^^^^^^^^

Use **pip** to install the Python module into your virtual environment:

.. code-block:: bash

   $ python3 -m pip install -e gsd

.. Build with CMake for development:

Build with CMake for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to the setuptools build system. GSD also provides a `CMake`_ configuration for
development and testing. You can assemble a functional Python module in the given build directory.
First, configure the build with ``cmake``.

.. code-block:: bash

   $ cmake -B build/gsd -S gsd

Then, build the code:

.. code-block:: bash

   $ cmake --build build/gsd

When modifying code, you only need to repeat the build step to update your build - it will
automatically reconfigure as needed.

.. tip::

    Use Ninja_ to perform incremental builds in less time::

        $ cmake -B build/gsd -S gsd -GNinja

.. tip::

    Place your build directory in ``/tmp`` or ``/scratch`` for faster builds. CMake_ performs
    out-of-source builds, so the build directory can be anywhere on the filesystem.

.. tip::

    Pass the following options to ``cmake`` to optimize the build for your processor:
    ``-DCMAKE_CXX_FLAGS=-march=native -DCMAKE_C_FLAGS=-march=native``.

.. important::

    When using a virtual environment, activate the environment and set the cmake prefix path
    before running CMake_: ``$ export CMAKE_PREFIX_PATH=<path-to-environment>``.

.. _CMake: https://cmake.org/
.. _Ninja: https://ninja-build.org/

.. _Run tests:

Run tests
^^^^^^^^^

Use `pytest`_ to execute unit tests:

.. code-block:: bash

   $ python3 -m pytest --pyargs gsd

Add the ``--validate`` option to include longer-running validation tests:

.. code-block:: bash

   $ python3 -m pytest --pyargs gsd -p gsd.pytest_plugin_validate --validate

.. tip::

    When using CMake builds, change to the build directory before running ``pytest``::

        $ cd build/gsd

.. _pytest: https://docs.pytest.org/

.. _Build the documentation:

Build the documentation
^^^^^^^^^^^^^^^^^^^^^^^

Run `Sphinx`_ to build the documentation:

.. code-block:: bash

   $ sphinx-build -b html gsd/doc build/gsd-documentation

Open the file :file:`build/gsd-documentation/index.html` in your web browser to view the
documentation.

.. tip::

    When iteratively modifying the documentation, the sphinx options ``-a -n -W -T --keep-going``
    are helpful to produce docs with consistent links in the side panel and to see more useful error
    messages::

        $ sphinx-build -a -n -W -T --keep-going -b html gsd/doc build/gsd-documentation

.. tip::

    When using CMake builds, set PYTHONPATH to the build directory before running ``sphinx-build``::

        $ PYTHONPATH=build/gsd sphinx-build -b html gsd/doc build/gsd-documentation

.. _Sphinx: https://www.sphinx-doc.org/

Embedding GSD in your project
-----------------------------

Using the C library
^^^^^^^^^^^^^^^^^^^

**gsd** is implemented in a single C file. Copy ``gsd/gsd.h`` and ``gsd/gsd.c`` into your project.

Using the pure Python reader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you only need to read files, you can skip installing and just extract the module modules
``gsd/pygsd.py`` and ``gsd/hoomd.py``. Together, these implement a pure Python reader for **gsd**
and **HOOMD** files - no C compiler required.
