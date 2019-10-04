Change Log
==========

`GSD <https://github.com/glotzerlab/gsd>`_ releases follow `semantic versioning <https://semver.org/>`_.

v1.9.3 (2019-10-04)
-------------------

* Fixed preprocessor directive affecting Windows builds using setup.py.

v1.9.2 (2019-10-01)
-------------------

* Support chunk sizes larger than 2GiB

v1.9.1 (2019-09-23)
-------------------

* Support writing chunks wider than 255 from Python.

v1.9.0 (2019-09-18)
-------------------

* File API: Add ``find_matching_chunk_names()``
* ``HOOMD`` schema 1.4: Add user defined logged data.
* ``HOOMD`` schema 1.4: Add ``type_shapes`` specification.
* pytest >= 3.9.0 is required to run unit tests.
* ``gsd.fl.open`` and ``gsd.hoomd.open`` accept objects implementing ``os.PathLike``.
* Report an error when attempting to write a chunk that fails to allocate a name.
* Reduce virtual memory usage in ``rb`` and ``wb`` open modes.
* Additional checks for corrupt GSD files on open.
* Synchronize after expanding file index.

v1.8.1 (2019-08-19)
-------------------

* Correctly raise ``IndexError`` when attempting to read frames before the first frame.
* Raise ``RuntimeError`` when importing ``gsd`` in unsupported Python versions.

v1.8.0 (2019-08-05)
-------------------

* Slicing a HOOMDTrajectory object returns a view that can be used to directly select frames from a subset
  or sliced again.
* raise ``IndexError`` when attempting to read frames before the first frame.
* Dropped support for Python 2.

v1.7.0 (2019-04-30)
-------------------

* Add ``hpmc/sphere/orientable`` to HOOMD schema.
* HOOMD schema 1.3


v1.6.2 (2019-04-16)
-------------------

* PyPI binary wheels now support numpy>=1.9.3,<2

v1.6.1 (2019-03-05)
-------------------

* Documentation updates

v1.6.0 (2018-12-20)
-------------------

* The length of sliced HOOMDTrajectory objects can be determined with the built-in ``len()`` function.

v1.5.5 (2018-11-28)
-------------------

* Silence numpy deprecation warnings

v1.5.4 (2018-10-04)
-------------------

* Add ``pyproject.toml`` file that defines ``numpy`` as a proper build dependency (requires pip >= 10)
* Reorganize documentation

v1.5.3 (2018-05-22)
-------------------

* Revert ``setup.py`` changes in v1.5.2 - these do not work in most circumstances.
* Include ``sys/stat.h`` on all architectures.

v1.5.2 (2018-04-04)
-------------------

* Close file handle on errors in ``gsd_open``.
* Always close file handle in ``gsd_close``.
* ``setup.py`` now correctly pulls in the numpy dependency.

v1.5.1 (2018-02-26)
-------------------

* Documentation fixes.

v1.5.0 (2018-01-18)
-------------------

* Read and write HPMC shape state data.

v1.4.0 (2017-12-04)
-------------------

* Support reading and writing chunks with 0 length. No schema changes are necessary to support this.

v1.3.0 (2017-11-17)
-------------------

* Document ``state`` entries in the HOOMD schema.
* No changes to the gsd format or reader code in v1.3.

v1.2.0 (2017-02-21)
-------------------

* Add ``gsd.hoomd.open()`` method which can create and open hoomd gsd files.
* Add ``gsd.fl.open()`` method which can create and open gsd files.
* The previous create/class ``GSDFile`` instantiation is still supported
  for backward compatibility.

v1.1.0 (2016-10-04)
-------------------

* Add special pairs section pairs/ to HOOMD schema.
* HOOMD schema version is now 1.1.

v1.0.1 (2016-06-15)
-------------------

* Fix compile error on more strict POSIX systems.

v1.0.0 (2016-05-24)
-------------------

Initial release.
