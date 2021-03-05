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

Use **pip** to install **gsd**:

.. code-block:: bash

   $ python3 -m pip install gsd

.. note::

    On some platforms, such as macOS with Apple silicon, **pip**'s default options may fail to
    install **gsd** or its dependencies. You can force **pip** to build these packages one at a time
    from source::

        $ python3 -m pip install cython
        $ python3 -m pip install --no-binary :all: --no-use-pep517 numpy
        $ python3 -m pip install --no-binary :all: --no-use-pep517 gsd

Compile from source
-------------------

Obtain the source
^^^^^^^^^^^^^^^^^

Download source releases directly from the web: https://glotzerlab.engin.umich.edu/downloads/gsd

.. code-block:: bash

   $ curl -O https://glotzerlab.engin.umich.edu/downloads/gsd/gsd-v2.4.0.tar.gz

Or, clone using git:

.. code-block:: bash

   $ git clone https://github.com/glotzerlab/gsd

Configure a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using a shared Python installation, create a `virtual environment
<https://docs.python.org/3/library/venv.html>`_ where you can install
**gsd**::

    $ python3 -m venv /path/to/environment

Activate the environment before configuring and before executing
**gsd** scripts::

   $ source /path/to/environment/bin/activate

.. note::

   Other types of virtual environments (such as *conda*) may work, but are not thoroughly tested.

Install Prerequisites
^^^^^^^^^^^^^^^^^^^^^

**gsd** requires:

* **C compiler** (tested with gcc 4.8-10.0, clang 4-11, vs2017-2019)
* **Python** >= 3.5
* **numpy** >= 1.9.3
* **Cython** >= 0.22

Additional packages may be needed:

* **pytest** >= 3.9.0 (unit tests)
* **Sphinx** (documentation)
* **IPython** (documentation)
* an internet connection (documentation)
* **CMake** (for development builds)

Install these tools with your system or virtual environment package manager. **gsd** developers have had success with
``pacman`` (`arch linux <https://www.archlinux.org/>`_), ``apt-get`` (`ubuntu <https://ubuntu.com/>`_), `Homebrew
<https://brew.sh/>`_ (macOS), and `MacPorts <https://www.macports.org/>`_ (macOS)::

    $ your-package-manager install ipython python python-pytest python-numpy cmake cython python-sphinx python-sphinx_rtd_theme

Typical HPC cluster environments provide **Python**, **numpy**, and **cmake** via a module system::

    $ module load gcc python cmake

.. note::

    Packages may be named differently, check your system's package list. Install any ``-dev`` packages as needed.

.. tip::

    You can install numpy and other python packages into your virtual environment::

        python3 -m pip install numpy


Install with setuptools
^^^^^^^^^^^^^^^^^^^^^^^

Use **pip** to install the python module into your virtual environment:

.. code-block:: bash

   $ python3 -m pip install .

Build with CMake for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can assemble a functional python module in the build directory. Configure with **CMake** and compile with **make**.

.. code-block:: bash

   $ mkdir build
   $ cd build
   $ cmake ../
   $ make

Add the build directory path to your ``PYTHONPATH`` to test **gsd** or build documentation:

.. code-block:: bash

   $ export PYTHONPATH=$PYTHONPATH:/path/to/build

Run tests
^^^^^^^^^

Use pytest to execute all unit tests:

.. code-block:: bash

   $ pytest --pyargs gsd

Build user documentation
^^^^^^^^^^^^^^^^^^^^^^^^

Build the user documentation with **Sphinx**. **IPython** is required to build the documentation, as is an active
internet connection. First, you need to compile and install **gsd**. If you compiled with **CMake**, add **gsd**
to your ``PYTHONPATH`` first:

.. code-block:: bash

   $ export PYTHONPATH=$PYTHONPATH:/path/to/build

To build the documentation:

.. code-block:: bash

   $ cd /path/to/gsd
   $ cd doc
   $ make html
   $ open _build/html/index.html

Using the C library
^^^^^^^^^^^^^^^^^^^^^^^^

**gsd** is implemented in a single C file. Copy ``gsd/gsd.h`` and ``gsd/gsd.c`` into your project.

Using the pure python reader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you only need to read files, you can skip installing and just extract the module modules ``gsd/pygsd.py`` and
``gsd/hoomd.py``. Together, these implement a pure Python reader for **gsd** and **HOOMD** files - no C compiler
required.
