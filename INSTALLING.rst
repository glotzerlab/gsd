.. Copyright (c) 2016-2024 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

Installation
============

**gsd** binaries are available on conda-forge_ and PyPI_. You can also compile **gsd** from source,
embed ``gsd.c`` in your code, or read gsd files with a pure Python reader ``pygsd.py``.

.. _conda-forge: https://conda-forge.org/
.. _PyPI: https://pypi.org/

Binaries
--------

Conda package
^^^^^^^^^^^^^

**gsd** is available on conda-forge_ for the *linux-64*, *linux-aarch64*, *linux-ppc64le*, *osx-64*,
*osx-arm64* and *win-64* architectures. Execute the following command to install **gsd**:

.. code-block:: bash

   $ mamba install gsd

PyPI
^^^^

Use **pip** to install **gsd** binaries from PyPI_:

.. code-block:: bash

   $ python3 -m pip install gsd

Compile from source
-------------------

To build the **gsd** Python package from source:

1. `Install prerequisites`_::

   $ {{ package-manager }} install cmake cython git ninja numpy python pytest

2. `Obtain the source`_::

   $ git clone https://github.com/glotzerlab/gsd

3. Change to the repository directory::

   $ cd gsd

4. `Install with pip`_::

   $ python3 -m pip install .

   **OR** `Build with CMake for development`_::

   $ cmake -B build -S . -GNinja
   $ cd build
   $ ninja

To run the tests:

1. `Run tests`_::

    $ python3 -m pytest gsd

To build the documentation from source:

1. `Install prerequisites`_::

   $ {{ package-manager }} install breathe doxygen sphinx furo ipython sphinx-copybutton

2. `Build the documentation`_::

   $ cd {{ path/to/gsd/repository }}
   $ doxygen
   $ sphinx-build -b html doc html

The sections below provide details on each of these steps.

.. _Install prerequisites:

Install prerequisites
^^^^^^^^^^^^^^^^^^^^^

**gsd** requires a number of tools and libraries to build.

.. note::

    This documentation is generic. Replace ``{{ package-manager }}`` with your package or module
    manager. You may need to adjust package names and/or install additional packages, such as
    ``-dev`` packages that provide headers needed to build **gsd**.

**General requirements:**

* **C compiler** (tested with gcc 10-14, clang 10-18, Visual Studio 2019-2022)
* **Python** >= 3.9
* **numpy** >= 1.19.0
* **Cython** >= 0.22

**To execute unit tests:**

* **pytest** >= 3.9.0

**To build the documentation**:

* **breathe**
* **Doxygen**
* **furo**
* **IPython**
* **Sphinx**
* **sphinx-copybutton**
* an internet connection


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

.. _Install with pip:

Install with pip
^^^^^^^^^^^^^^^^^^^^^^^

Use **pip** to install the Python module into your virtual environment:

.. code-block:: bash

   $ cd {{ path/to/gsd/repository }}
   $ python3 -m pip install .

.. Build with CMake for development:

Build with CMake for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GSD also provides `CMake`_ scripts for development and testing that build a functional Python module
in the given build directory. First, configure the build with ``cmake``.

.. code-block:: bash

   $ cd {{ path/to/gsd/repository }}
   $ cmake -B build -S . -GNinja

Then, build the code:

.. code-block:: bash

   $ cd build
   $ ninja

After you modify the code, execute ``ninja`` to rebuild. ``ninja`` will automatically reconfigure
as needed.

.. tip::

    Pass the following options to ``cmake`` to optimize the build for your processor:
    ``-DCMAKE_CXX_FLAGS=-march=native -DCMAKE_C_FLAGS=-march=native``.

.. important::

    When using a virtual environment, activate the environment and set the cmake prefix path
    before running CMake_: ``$ export CMAKE_PREFIX_PATH=<path-to-environment>``.

.. warning::

    When using a ``conda`` environment for development, make sure that the environment does not
    contain ``clang``, ``gcc``, or any other compiler or linker. These interfere with the native
    compilers on your system and will result in compiler errors when building, linker errors when
    running, or unexplainable segmentation faults.

.. _CMake: https://cmake.org/
.. _Ninja: https://ninja-build.org/

.. _Run tests:

Run tests
^^^^^^^^^

Use `pytest`_ to execute unit tests:

.. code-block:: bash

   $ python3 -m pytest gsd

Add the ``--validate`` option to include longer-running validation tests:

.. code-block:: bash

   $ python3 -m pytest --pyargs gsd -p gsd.pytest_plugin_validate --validate

.. _pytest: https://docs.pytest.org/

.. _Build the documentation:

Build the documentation
^^^^^^^^^^^^^^^^^^^^^^^

Run `Doxygen`_ to generate the C documentation:

.. code-block:: bash

   $ cd {{ path/to/gsd/repository }}
   $ doxygen

Run `Sphinx`_ to build the HTML documentation:

.. code-block:: bash

   $ sphinx-build -b html doc html

Open the file :file:`html/index.html` in your web browser to view the documentation.

.. tip::

    Add the sphinx options ``-a -n -W -T --keep-going`` to produce docs with consistent links in
    the side panel and provide more useful error messages::

.. tip::

    When using CMake builds, set PYTHONPATH to the build directory before running ``sphinx-build``::

        $ PYTHONPATH=build sphinx-build -b html doc html

.. _Sphinx: https://www.sphinx-doc.org/
.. _Doxygen: https://www.doxygen.nl/

Embedding GSD in your project
-----------------------------

Using the C library
^^^^^^^^^^^^^^^^^^^

**gsd** is implemented in a single C file. Copy ``gsd/gsd.h`` and ``gsd/gsd.c`` into your project.

Using the pure Python reader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Python modules ``gsd/pygsd.py`` and ``gsd/hoomd.py`` implement a pure Python reader for **gsd**
and **HOOMD** files.
