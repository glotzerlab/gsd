# GSD

## Overview

GSD (General Simulation Data) is a file format specification and a library to read and write it.

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

## Installing the python module

Official binaries of GSD are available via [conda](http://conda.pydata.org/docs/) through
the [glotzer channel](https://anaconda.org/glotzer).
To install GSD, first download and install
[miniconda](http://conda.pydata.org/miniconda.html) following [conda's instructions](http://conda.pydata.org/docs/install/quick.html).
Then add the `glotzer` channel and install GSD:

```bash
$ conda config --add channels glotzer
$ conda install gsd
```

TODO: It is not actually available yet.

## Examples

```python
with GSDFile(name='file.gsd', mode='w') as f:
    f.write_chunk(name='position', data=numpy.array([[1,2,3],[4,5,6]], dtype=numpy.float32));
    f.write_chunk(name='angle', data=numpy.array([0, 1], dtype=numpy.float32));
    f.write_chunk(name='box', data=numpy.array([10, 10, 10], dtype=numpy.float32));
    f.end_frame()
```

```python
with GSDFile(name='file.gsd', mode='r') as f:
    for i in range(1,f.nframes):
        position = f.read_chunk(frame=i, name='position');
        do_something(position);
```

## Compiling the python module

### Prerequisites

    * A standards compliant C compiler
    * Python >= 2.7
    * Cython >= 0.22 (not needed to build tagged releases)

### Install with setuptools

Use ``python setup.py`` to install the python module with setuptools. For example, to install into
your home directory, execute:

```bash
$ python setup.py install --user
```

### Build with cmake for development

You can assemble a functional python module in the build directory using cmake:

```bash
$ mkdir build
$ cd build
$ cmake ../
$ make
```

Then add the directory to your PYTHONPATH temporarily for testing.

```bash
export PYTHONPATH=/path/to/build:$PYTHONPATH
```

### Install with cmake

The cmake build scripts expect ``${CMAKE_INSTALL_PREFIX}`` to be a valid python site directory.
You can set the prefix automatically with **one** of the following cmake options:

    * ``INSTALL_USER``, install into the user site (like ``setup.py install --user``)
    * ``INSTALL_SITE``, install into the system site (like ``setup.py install``)

```bash
$ cmake ../ -D INSTALL_USER=on
$ make install
```

### Run unit tests

Run `nosetests` in the source directory to execute all unit tests. This requires that the
python module is on the python path.

```bash
$ nosetests
```

### Build Documentation

Documentation builds with sphinx and requires that the python module is on the python path.
To build the documentation:

```bash
$ cd doc
$ make html
$ open _build/html/index.html
```

## Using the C library

GSD is implemented in less than 1k lines of C code. It doesn't build a shared library, just
copy `gsd/gsd.h` and `gsd/gsd.c` into your project and compile it directly in.
