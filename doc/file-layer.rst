.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

File layer
==========

.. highlight:: c

**Version: 2.0**

General simulation data (GSD) **file layer** design and rationale. These use
cases and design specifications define the low level GSD file format.

Differences from the 1.0 specification are noted.

Use-cases
---------

* capabilities

  * efficiently store many frames of data from simulation runs
  * high performance file read and write
  * support arbitrary chunks of data in each frame (position, orientation, type,
    etc...)
  * variable number of named chunks in each frame
  * variable size of chunks in each frame
  * each chunk identifies data type
  * common use cases: NxM arrays in double, float, int, char types.
  * generic use case: binary blob of N bytes
  * can be integrated into other tools
  * append frames to an existing file with a monotonically increasing frame
    number
  * resilient to job kills

* queries

  * number of frames
  * is named chunk present in frame *i*
  * type and size of named chunk in frame *i*
  * read data for named chunk in frame *i*
  * read only a portion of a chunk
  * list chunk names in the file

* writes

  * write data to named chunk in the current frame
  * end frame and commit to disk

These capabilities enable a simple and rich higher level schema for storing
particle and other types of data. The schema determine which named chunks exist
in a given file and what they mean.

Non use-cases
-------------

These capabilities are use-cases that GSD does **not** support, by design.

#. Modify data in the file: GSD is designed to capture simulation data.
#. Add chunks to frames in the middle of a file: See (1).
#. Transparent conversion between float and double: Callers must take care of
   this.
#. Transparent compression: this gets in the way of parallel I/O. Disk space is
   cheap.

Dependencies
------------

The file layer is implemented in C (*not C++*) with no dependencies to enable
trivial installation and incorporation into existing projects. A single header
and C file completely implement the entire file layer. Python based projects
that need only read access can use :py:mod:`gsd.pygsd`, a pure Python gsd reader
implementation.

A Python interface to the file layer allows reference implementations and
convenience methods for schemas. Most non-technical users of GSD will probably
use these reference implementations directly in their scripts.

The low level C library is wrapped with cython. A Python setup.py file will
provide simple installation on as many systems as possible. Cython c++ output is
checked in to the repository so users do not even need cython as a dependency.

Specifications
--------------

Support:

* Files as large as the underlying filesystem allows (up to 64-bit address
  limits)
* Data chunk names of arbitrary length (v1.0 limits chunk names to 63 bytes)
* Reference up to 65535 different chunk names within a file
* Application and schema names up to 63 characters
* Store as many frames as can fit in a file up to file size limits
* Data chunks up to (64-bit) x (32-bit) elements

The limits on only 16-bit name indices and 32-bit column indices are to keep the
size of each index entry as small as possible to avoid wasting space in the file
index. The primary use cases in mind for column indices are Nx3 and Nx4 arrays
for position and quaternion values. Schemas that wish to store larger truly
n-dimensional arrays can store their dimensionality in metadata in another chunk
and store as an Nx1 index entry. Or use a file format more suited to
N-dimensional arrays such as HDF5.

File format
-----------

There are four types of data blocks in a GSD file.

#. Header block

   * Overall header for the entire file, contains the magic cookie, a format
     version, the name of the generating application, the schema name, and its
     version. Some bytes in the header are reserved for future use. Header size:
     256 bytes. The header block also includes a pointer to the index, the
     number of allocated entries, the number of allocated entries in the index, a
     pointer to the name list, and the size of the name list block.
   * The header is the first 256 bytes in the file.

#. Index block

   * Index the frame data, size information, location, name id, etc...
   * The index contains space for any number of ``index_entry`` structs
   * The first index in the list with a location of 0 marks the end of the list.
   * When the index fills up, a new index block is allocated at the end of the
     file with more space and all current index entries are rewritten there.
   * Index entry size: 32 bytes

#. Name list

   * List of string names used by index entries.
   * v1.0 files: Each name is a 64-byte character string.
   * v2.0 files: Names may have any length and are separated by 0 terminators.
   * The first name that starts with the 0 byte marks the end of the list
   * The header stores the total size of the name list block.

#. Data chunk

   * Raw binary data stored for the named frame data blocks.

Header index, and name blocks are stored in memory as C structs (or arrays of C
structs) and written to disk in whole chunks.

Header block
^^^^^^^^^^^^

This is the header block::

    struct gsd_header
        {
        uint64_t magic;
        uint64_t index_location;
        uint64_t index_allocated_entries;
        uint64_t namelist_location;
        uint64_t namelist_allocated_entries;
        uint32_t schema_version;
        uint32_t gsd_version;
        char application[64];
        char schema[64];
        char reserved[80];
        };


* ``magic`` is the magic number identifying this as a GSD file
  (``0x65DF65DF65DF65DF``).
* ``gsd_version`` is the version number of the gsd file layer
  (``0xaaaabbbb => aaaa.bbbb``).
* ``application`` is the name of the generating application.
* ``schema`` is the name of the schema for data in this gsd file.
* ``schema_version`` is the version of the schema (``0xaaaabbbb => aaaa.bbbb``).
* ``index_location`` is the file location f the index block.
* ``index_allocated_entries`` is the number of 64-byte segments available in the
  namelist block.
* ``namelist_location`` is the file location of the namelist block.
* ``namelist_allocated_entries`` is the number of entries allocated in the
  namelist block.
* ``reserved`` are bytes saved for future use.

This structure is ordered so that all known compilers at the time of writing
produced a tightly packed 256-byte header. Some compilers may required
non-standard packing attributes or pragmas to enforce this.

Index block
^^^^^^^^^^^

An Index block is made of a number of line items that store a pointer to a
single data chunk::

    struct gsd_index_entry
        {
        uint64_t frame;
        uint64_t N;
        int64_t location;
        uint32_t M;
        uint16_t *id*;
        uint8_t type;
        uint8_t flags;
        };

* ``frame`` is the index of the frame this chunk belongs to
* ``N`` and ``M`` define the dimensions of the data matrix (NxM in C ordering
  with M as the fast index).
* ``location`` is the location of the data chunk in the file
* ``id`` is the index of the name of this entry in the namelist.
* ``type`` is the type of the data (char, int, float, double) indicated by index
  values
* ``flags`` is reserved for future use.

Many ``gsd_index_entry_t`` structs are combined into one index block. They are
stored densely packed and in the same order as the corresponding data chunks are
written to the file.

This structure is ordered so that all known compilers at the time of writing
produced a tightly packed 32-byte entry. Some compilers may required
non-standard packing attributes or pragmas to enforce this.

In v1.0 files, the frame index must monotonically increase from one index entry
to the next. The GSD API ensures this.

In v2.0 files, the entire index block is stored sorted first by frame, then
by *id*.

Namelist block
^^^^^^^^^^^^^^

In v2.0 files, the namelist block stores a list of strings separated by 0
terminators.

In v1.0 files, the namelist block stores a list of 0-terminated strings in
64-byte segments.

The first string that starts with 0 marks the end of the list.

Data block
^^^^^^^^^^

A data block stores raw data bytes on the disk. For a given index entry
``entry``, the data starts at location ``entry.location`` and is the next
``entry.N * entry.M * gsd_sizeof_type(entry.type)`` bytes.
