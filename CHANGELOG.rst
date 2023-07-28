.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

Change Log
==========

`GSD <https://github.com/glotzerlab/gsd>`_ releases follow `semantic versioning
<https://semver.org/>`_.

3.x
---

3.1.0 (2023-07-28)
^^^^^^^^^^^^^^^^^^

*Fixed:*

* ``hoomd.read_log`` no longer triggers a numpy deprecation warning.

*Added:*

* ``HOOMDTrajectory.flush`` - flush buffered writes on an open ``HOOMDTrajectory``.

3.0.1 (2023-06-20)
^^^^^^^^^^^^^^^^^^

*Fixed:*

* Prevent ``ValueError: signal only works in main thread of the main interpreter`` when importing
  gsd in a non-main thread.

3.0.0 (2023-06-16)
^^^^^^^^^^^^^^^^^^

*Added:*

* ``gsd.version.version`` - version string identifier. PEP8 compliant name replaces ``__version__``.
* ``GSDFile.flush`` - flush write buffers (C API ``gsd_flush``)
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).
* ``GSDFile.maximum_write_buffer_size`` - get/set the write buffer size
  (C API ``gsd_get_maximum_write_buffer_size`` / ``gsd_set_maximum_write_buffer_size``)
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).
* ``GSDFile.index_entries_to_buffer`` - get/set the write buffer size
  (C API ``index_entries_to_buffer`` / ``index_entries_to_buffer``)
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).
* On importing `gsd`, install a ``SIGTERM`` handler that calls ``sys.exit(1)``
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).

*Changed:*

* ``write_chunk`` buffers writes across frames to increase performance
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).
* Use *Doxygen* and *breathe* to generate C API documentation in Sphinx
  (`#237 <https://github.com/glotzerlab/gsd/pull/237>`__).

*Removed:*

* ``gsd.__version__`` - use ``gsd.version.version``.
* ``gsd.hoomd.Snapshot`` - use ``gsd.hoomd.Frame``
  (`#249 <https://github.com/glotzerlab/gsd/pull/249>`__).
* ``gsd.hoomd.HOOMDTrajectory.read_frame`` - use ``gsd.hoomd.HOOMDTrajectory.__getitem__``
  (`#249 <https://github.com/glotzerlab/gsd/pull/249>`__).
* The file modes ``'wb'``, ``'wb+'``, ``'rb'``,  ``'rb+'``, ``'ab'``, ``'xb'``, and ``'xb+'``. Use
  ``'r'``, ``'r+'``, ``'w'``, ``'x'``, or ``'a'``
  (`#249 <https://github.com/glotzerlab/gsd/pull/249>`__).

2.x
---

2.9.0 (2023-05-19)
^^^^^^^^^^^^^^^^^^

*Added:*

* File modes ``'r'``, ``'r+'``, ``'w'``, ``'x'``, and ``'a'``
  (`#238 <https://github.com/glotzerlab/gsd/pull/238>`__).

*Changed:*

* Test on gcc9, clang10, and newer
  (`#235 <https://github.com/glotzerlab/gsd/pull/235>`__).
* Test and provide binary wheels on Python 3.8 and newer
  (`#235 <https://github.com/glotzerlab/gsd/pull/235>`__).

*Deprecated:*

* File modes ``'wb'``, ``'wb+'``, ``'rb'``,  ``'rb+'``, ``'ab'``, ``'xb'``, and ``'xb+'``
  (`#238 <https://github.com/glotzerlab/gsd/pull/238>`__).
* [C API] ``GSD_APPEND`` file open mode
  (`#238 <https://github.com/glotzerlab/gsd/pull/238>`__).

v2.8.1 (2023-03-13)
^^^^^^^^^^^^^^^^^^^

*Fixed:*

* Reduce memory usage in most use cases.
* Reduce likelihood  of data corruption when writing GSD files.

v2.8.0 (2023-02-24)
^^^^^^^^^^^^^^^^^^^

*Added:*

* ``gsd.hoomd.read_log`` - Read log quantities from a GSD file.
* ``gsd.hoomd.Frame`` class to replace ``gsd.hoomd.Snapshot``.

*Changed:*

* Improved documentation.

*Deprecated:*

* ``gsd.hoomd.Snapshot``.

v2.7.0 (2022-11-30)
^^^^^^^^^^^^^^^^^^^

*Added*

* Support Python 3.11.

v2.6.1 (2022-11-04)
^^^^^^^^^^^^^^^^^^^

*Fixed:*

* Default values are now written to frame N (N != 0) when non-default values
  exist in frame 0.
* Data chunks can now be read from files opened in 'wb', 'xb', and 'ab' modes.

v2.6.0 (2022-08-19)
^^^^^^^^^^^^^^^^^^^

*Changed:*

* Raise an error when writing a frame with duplicate types.

v2.5.3 (2022-06-22)
^^^^^^^^^^^^^^^^^^^

*Fixed*

* Support Python >=3.6.

v2.5.2 (2022-04-15)
^^^^^^^^^^^^^^^^^^^

*Fixed*

* Correctly handle non-ASCII characters on Windows.
* Document that the ``fname`` argument to ``gsd_`` C API functions is UTF-8
  encoded.

v2.5.1 (2021-11-17)
^^^^^^^^^^^^^^^^^^^

*Added*

* Support for Python 3.10.
* Support for clang 13.

v2.5.0 (2021-10-13)
^^^^^^^^^^^^^^^^^^^

*Changed*

* Improved documentation.

*Deprecated*

- ``HOOMDTrajectory.read_frame`` - use indexing (``trajectory[index]``) to access frames from a
  trajectory.

v2.4.2 (2021-04-14)
^^^^^^^^^^^^^^^^^^^

*Added*

* MacOS and Windows wheels on PyPI.

*Fixed*

- Documented array shapes for angles, dihedrals, and impropers.

v2.4.1 (2021-03-11)
^^^^^^^^^^^^^^^^^^^

*Added*

* Support macos-arm64.

*Changed*

* Stop testing with clang 4-5, gcc 4.8-6.

v2.4.0 (2020-11-11)
^^^^^^^^^^^^^^^^^^^

*Changed*

* Set ``gsd.hoomd.ConfigurationData.dimensions`` default based on ``box``'s
  :math:`L_z` value.

*Fixed*

* Failure in ``test_fl.py`` when run by a user and GSD was installed by root.


v2.3.0 (2020-10-30)
^^^^^^^^^^^^^^^^^^^

*Added*

* Support clang 11.
* Support Python 3.9.

*Changed*

* Install unit tests with the Python package.

*Fixed*

* Compile error on macOS 10.15.

v2.2.0 (2020-08-05)
^^^^^^^^^^^^^^^^^^^

*Added*

* Command line convenience interface for opening a GSD file.

v2.1.2 (2020-06-26)
^^^^^^^^^^^^^^^^^^^

*Fixed*

* Adding missing ``close`` method to ``HOOMDTrajectory``.
* Documentation improvements.

v2.1.1 (2020-04-20)
^^^^^^^^^^^^^^^^^^^

*Fixed*

* List defaults in ``gsd.fl.open`` documentation.

v2.1.0 (2020-02-27)
^^^^^^^^^^^^^^^^^^^

*Added*

* Shape specification for sphere unions.

v2.0.0 (2020-02-03)
^^^^^^^^^^^^^^^^^^^

*Note*

* This release introduces a new file storage format.
* GSD >= 2.0 can read and write to files created by GSD 1.x.
* Files created or upgraded by GSD >= 2.0 can not be opened by GSD < 1.x.

*Added*

* The ``upgrade`` method converts a GSD 1.0 file to a GSD 2.0 file in place.
* Support arbitrarily long chunk names (only in GSD 2.0 files).

*Changed*

* ``gsd.fl.open`` accepts ``None`` for ``application``, ``schema``, and
  ``schema_version`` when opening files for reading.
* Improve read latency when accessing files with thousands of chunk names in
  a frame (only for GSD 2.0 files).
* Buffer small writes to improve write performance.
* Improve performance and reduce memory usage in read/write modes ('rb+', 'wb+'
  and ('xb+').
* **C API**: functions return error codes from the ``gsd_error`` enum. v2.x
  integer error codes differ from v1.x, use the enum to check. For example:
  ``if (retval == GSD_ERROR_IO)``.
* Python, Cython, and C code must follow strict style guidelines.

*Removed*

* ``gsd.fl.create`` - use ``gsd.fl.open``.
* ``gsd.hoomd.create`` - use ``gsd.hoomd.open``.
* ``GSDFile`` v1.0 compatibility mode - use ``gsd.fl.open``.
* ``hoomdxml2gsd.py``.

*Fixed*

* Allow more than 127 data chunk names in a single GSD file.

v1.x
----

v1.10.0 (2019-11-26)
^^^^^^^^^^^^^^^^^^^^

* Improve performance of first frame write.
* Allow pickling of GSD file handles opened in read only mode.
* Removed Cython-generated code from repository. ``fl.pyx`` will be cythonized
  during installation.

v1.9.3 (2019-10-04)
^^^^^^^^^^^^^^^^^^^

* Fixed preprocessor directive affecting Windows builds using setup.py.
* Documentation updates

v1.9.2 (2019-10-01)
^^^^^^^^^^^^^^^^^^^

* Support chunk sizes larger than 2GiB

v1.9.1 (2019-09-23)
^^^^^^^^^^^^^^^^^^^

* Support writing chunks wider than 255 from Python.

v1.9.0 (2019-09-18)
^^^^^^^^^^^^^^^^^^^

* File API: Add ``find_matching_chunk_names()``
* ``HOOMD`` schema 1.4: Add user defined logged data.
* ``HOOMD`` schema 1.4: Add ``type_shapes`` specification.
* pytest >= 3.9.0 is required to run unit tests.
* ``gsd.fl.open`` and ``gsd.hoomd.open`` accept objects implementing
  ``os.PathLike``.
* Report an error when attempting to write a chunk that fails to allocate a
  name.
* Reduce virtual memory usage in ``rb`` and ``wb`` open modes.
* Additional checks for corrupt GSD files on open.
* Synchronize after expanding file index.

v1.8.1 (2019-08-19)
^^^^^^^^^^^^^^^^^^^

* Correctly raise ``IndexError`` when attempting to read frames before the first
  frame.
* Raise ``RuntimeError`` when importing ``gsd`` in unsupported Python versions.

v1.8.0 (2019-08-05)
^^^^^^^^^^^^^^^^^^^

* Slicing a HOOMDTrajectory object returns a view that can be used to directly
  select frames from a subset or sliced again.
* raise ``IndexError`` when attempting to read frames before the first frame.
* Dropped support for Python 2.

v1.7.0 (2019-04-30)
^^^^^^^^^^^^^^^^^^^

* Add ``hpmc/sphere/orientable`` to HOOMD schema.
* HOOMD schema 1.3


v1.6.2 (2019-04-16)
^^^^^^^^^^^^^^^^^^^

* PyPI binary wheels now support numpy>=1.9.3,<2

v1.6.1 (2019-03-05)
^^^^^^^^^^^^^^^^^^^

* Documentation updates

v1.6.0 (2018-12-20)
^^^^^^^^^^^^^^^^^^^

* The length of sliced HOOMDTrajectory objects can be determined with the
  built-in ``len()`` function.

v1.5.5 (2018-11-28)
^^^^^^^^^^^^^^^^^^^

* Silence numpy deprecation warnings

v1.5.4 (2018-10-04)
^^^^^^^^^^^^^^^^^^^

* Add ``pyproject.toml`` file that defines ``numpy`` as a proper build
  dependency (requires pip >= 10)
* Reorganize documentation

v1.5.3 (2018-05-22)
^^^^^^^^^^^^^^^^^^^

* Revert ``setup.py`` changes in v1.5.2 - these do not work in most
  circumstances.
* Include ``sys/stat.h`` on all architectures.

v1.5.2 (2018-04-04)
^^^^^^^^^^^^^^^^^^^

* Close file handle on errors in ``gsd_open``.
* Always close file handle in ``gsd_close``.
* ``setup.py`` now correctly pulls in the numpy dependency.

v1.5.1 (2018-02-26)
^^^^^^^^^^^^^^^^^^^

* Documentation fixes.

v1.5.0 (2018-01-18)
^^^^^^^^^^^^^^^^^^^

* Read and write HPMC shape state data.

v1.4.0 (2017-12-04)
^^^^^^^^^^^^^^^^^^^

* Support reading and writing chunks with 0 length. No schema changes are
  necessary to support this.

v1.3.0 (2017-11-17)
^^^^^^^^^^^^^^^^^^^

* Document ``state`` entries in the HOOMD schema.
* No changes to the gsd format or reader code in v1.3.

v1.2.0 (2017-02-21)
^^^^^^^^^^^^^^^^^^^

* Add ``gsd.hoomd.open()`` method which can create and open hoomd gsd files.
* Add ``gsd.fl.open()`` method which can create and open gsd files.
* The previous create/class ``GSDFile`` instantiation is still supported
  for backward compatibility.

v1.1.0 (2016-10-04)
^^^^^^^^^^^^^^^^^^^

* Add special pairs section pairs/ to HOOMD schema.
* HOOMD schema version is now 1.1.

v1.0.1 (2016-06-15)
^^^^^^^^^^^^^^^^^^^

* Fix compile error on more strict POSIX systems.

v1.0.0 (2016-05-24)
^^^^^^^^^^^^^^^^^^^

Initial release.
