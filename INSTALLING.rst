Installation
============

**GSD** binaries are available in the `glotzerlab-software <https://glotzerlab-software.readthedocs.io>`_
`Docker <https://hub.docker.com/>`_/`Singularity <https://www.sylabs.io/>`_ images and in packages on
`conda-forge <https://conda-forge.org/>`_ and `PyPI <https://pypi.org/>`_. You can also compile **GSD** from source,
embed ``gsd.c`` in your code, or read gsd files with a single file pure python reader ``pygsd.py``.

Binaries
--------

Anaconda package
^^^^^^^^^^^^^^^^

**GSD** is available on `conda-forge <https://conda-forge.org/>`_. To install, first download and install
`miniconda <http://conda.pydata.org/miniconda.html>`_.
Then add the ``conda-forge`` channel and install **GSD**:

.. code-block:: bash

   $ conda config --add channels conda-forge
   $ conda install gsd

You can update **GSD** with:

.. code-block:: bash

   $ conda update gsd

Docker images
^^^^^^^^^^^^^

Pull the `glotzerlab-software <https://glotzerlab-software.readthedocs.io>`_ image to get
**GSD** along with many other tools commonly used in simulation and analysis workflows. See full usage information in the
`glotzerlab-software documentation <https://glotzerlab-software.readthedocs.io>`_.

Singularity:

.. code-block:: bash

   $ singularity pull shub://glotzerlab/software

Docker:

.. code-block:: bash

   $ docker pull glotzerlab/software

PyPI
^^^^

Use **pip** to install **GSD**:

.. code-block:: bash

   $ pip install gsd


Compile from source
-------------------

Download source releases directly from the web: https://glotzerlab.engin.umich.edu/Downloads/gsd

.. code-block:: bash

   $ curl -O https://glotzerlab.engin.umich.edu/Downloads/gsd/gsd-v1.5.5.tar.gz

Or, clone using git:

.. code-block:: bash

   $ git clone https://bitbucket.org/glotzer/gsd.git

Prerequisites
^^^^^^^^^^^^^

* A standards compliant C compiler
* Python >= 2.7
* numpy

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

* Cython >= 0.22 (only needed for non-tagged releases)
* nose (unit tests)
* sphinx (documentation)
* ipython (documentation)
* an internet connection (documentation)
* cmake (for development builds)
* Python >= 3.2 (to execute unit tests)

Install with setuptools
^^^^^^^^^^^^^^^^^^^^^^^

Use ``python setup.py`` to install the python module with **setuptools**. For example, to install into
your home directory, execute:

.. code-block:: bash

    $ python setup.py install --user

When using conda, you can install into your **conda** site-packages with:

.. code-block:: bash

    $ python setup.py install

Uninstall using pip:

.. code-block:: bash

    $ pip uninstall gsd

Build with cmake for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can assemble a functional python module in the build directory. Configure with **cmake** and compile with **make**.

.. code-block:: bash

   $ mkdir build
   $ cd build
   $ cmake ../
   $ make

Add ``/path/to/build`` to your ``PYTHONPATH`` to test **GSD**, where ``/path/to`` is the directory containing your
``build`` directory.

.. code-block:: bash

   $ export PYTHONPATH=$PYTHONPATH:/path/to/build

Run tests
^^^^^^^^^

**GSD** has extensive unit tests to verify correct execution. Tests require python 3.2 or newer to execute.

Run ``nosetests`` in the source directory to execute all unit tests. This requires that the
python module is on the python path.

.. code-block:: bash

   $ cd /path/to/gsd
   $ nosetests

Build user documentation
^^^^^^^^^^^^^^^^^^^^^^^^

Build the user documentation with **sphinx**. ``ipython`` is also required to build the documentation, as is an active
internet connection. To build the documentation:

.. code-block:: bash

   $ cd /path/to/gsd
   $ cd doc
   $ make html
   $ open _build/html/index.html

Using the C library
^^^^^^^^^^^^^^^^^^^^^^^^

GSD is implemented in less than 1k lines of C code. It doesn't build a shared library, just
copy ``gsd/gsd.h`` and ``gsd/gsd.c`` into your project and compile it directly in.

Using the pure python reader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you only need to read files, you can skip installing and just extract the module modules ``gsd/pygsd.py`` and
``gsd/hoomd.py``. Together, these implement a pure-python reader for GSD and hoomd files - no C compiler required.
