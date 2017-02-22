# GSD

See the [full GSD documentation](http://gsd.readthedocs.io) at readthedocs.io.

## Overview

GSD (General Simulation Data) is a file format specification and a library to read and write it. The package also
contains a python module that reads and writes hoomd schema gsd files with an easy to use syntax.

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

## HOOMD examples

Create a hoomd gsd file.
```python
>>> s = gsd.hoomd.Snapshot()
>>> s.particles.N = 4
>>> s.particles.types = ['A', 'B']
>>> s.particles.typeid = [0,0,1,1]
>>> s.particles.position = [[0,0,0],[1,1,1], [-1,-1,-1], [1,-1,-1]]
>>> s.configuration.box = [3, 3, 3, 0, 0, 0]
>>> traj = gsd.hoomd.open(name='test.gsd', mode='wb')
>>> traj.append(s)
```

Append frames to a gsd file:
```python
>>> def create_frame(i):
...     s = gsd.hoomd.Snapshot();
...     s.configuration.step = i;
...     s.particles.N = 4+i;
...     s.particles.position = numpy.random.random(size=(4+i,3))
...     return s;
>>> with gsd.hoomd.open('test.gsd', 'ab') as t:
...     t.extend( (create_frame(i) for i in range(10)) )
...     print(len(t))
11
```

Randomly index frames:
```python
>>> with gsd.hoomd.open('test.gsd', 'rb') as t:
...     snap = t[5]
...     print(snap.configuration.step)
4
...     print(snap.particles.N)
8
...     print(snap.particles.position)
[[ 0.56993282  0.42243481  0.5502916 ]
 [ 0.36892486  0.38167036  0.27310368]
 [ 0.04739023  0.13603486  0.196539  ]
 [ 0.120232    0.91591144  0.99463677]
 [ 0.79806316  0.16991436  0.15228257]
 [ 0.13724308  0.14253527  0.02505   ]
 [ 0.39287439  0.82519054  0.01613089]
 [ 0.23150323  0.95167434  0.7715748 ]]
```

Slice frames:
```python
>>> with gsd.hoomd.open('test.gsd', 'rb') as t:
...     for s in t[5:-2]:
...         print(s.configuration.step, end=' ')
4 5 6 7
```

## File layer examples

```python
with gsd.fl.open(name='file.gsd', mode='wb') as f:
    f.write_chunk(name='position', data=numpy.array([[1,2,3],[4,5,6]], dtype=numpy.float32));
    f.write_chunk(name='angle', data=numpy.array([0, 1], dtype=numpy.float32));
    f.write_chunk(name='box', data=numpy.array([10, 10, 10], dtype=numpy.float32));
    f.end_frame()
```

```python
with gsd.fl.open(name='file.gsd', mode='rb') as f:
    for i in range(1,f.nframes):
        position = f.read_chunk(frame=i, name='position');
        do_something(position);
```

## Compiling the python module

### Prerequisites

    * A standards compliant C compiler
    * Python >= 2.7
    * numpy

### Optional dependencies

    * Cython >= 0.22 (only needed for non-tagged releases)
    * nose (unit tests)
    * sphinx (documentation)
    * ipython (documentation)
    * cmake (for development builds)

Either install using your distributions package manager, by loading the appropriate module on a cluster or with a
conda install in your home directory.

    conda install cython nose sphinx ipython cmake

### Install with setuptools

Use ``python setup.py`` to install the python module with setuptools. For example, to install into
your home directory, execute:

```bash
$ python setup.py install --user
```

When using conda, you can install into your `conda` site-packages with:

```bash
$ python setup.py install --user
```

Uninstall using pip:

```bash
$ pip uninstall gsd
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

### Run unit tests

Run `nosetests` in the source directory to execute all unit tests. This requires that the
python module is on the python path.

```bash
$ nosetests
```

### Build Documentation

Documentation builds with sphinx and requires that the python module is on the python path.
`ipython` is also required to build the documentation.
To build the documentation:

```bash
$ cd doc
$ make html
$ open _build/html/index.html
```

## Using the C library

GSD is implemented in less than 1k lines of C code. It doesn't build a shared library, just
copy `gsd/gsd.h` and `gsd/gsd.c` into your project and compile it directly in.

## Using the pure python reader

If you only need to read files, you can skip installing and just extract the module modules `gsd/pygsd.py` and
`gsd/hoomd.py`. Together, these implement a pure-python reader for GSD and hoomd files - no C compiler required.

# Change log

See [ChangeLog.md](ChangeLog.md).
