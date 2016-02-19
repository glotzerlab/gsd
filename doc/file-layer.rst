.. Copyright (c) 2016 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

File layer
==========

.. highlight:: c

General simulation data (GSD) **file layer** design and rationale. These use cases and design specifications
define the low level GSD file format.

Use-cases
---------

* capabilities
    * efficiently store many frames of data from simulation runs
    * high performance file read and write
    * support arbitrary chunks of data in each frame (position, orientation, type, etc...)
    * variable number of named chunks in each frame
    * variable size of chunks in each frame
    * each chunk identifies data type
    * common use cases: NxM arrays in double, float, int, char types.
    * generic use case: binary blob of N bytes
    * easy to integrate into other tools
    * append frames to an existing file with a monotonically increasing frame number
    * resilient to job kills
* queries
    * number of frames
    * is named chunk present in frame *i*
    * type and size of named chunk in frame *i*
    * read data for named chunk in frame *i*
    * read only a portion of a chunk
* writes
    * write data to named chunk in the current frame
    * write a single data chunk from multiple MPI ranks
    * end frame and commit to disk

These capabilities should enable a simple and rich higher level schema for storing particle and other types of
data. The schema determine which named chunks exist in a given file and what they mean.

Non use-cases
-------------

These capabilities are use-cases that GSD does **not** support, by design.

#. Modify data in the file: GSD is designed to capture simulation data, that raw data should not be modifiable.
#. Add chunks to frames in the middle of a file: See (1).
#. Transparent conversion between float and double: Callers must take care of this.
#. Transparent compression - this gets in the way of parallel I/O. Disk space is cheap.

Specifications
--------------

Support:

* Files as large as the underlying filesystem allows (up to 64-bit address limits)
* Data chunk names up to 63 characters
* Reference up to 65536 different chunk names within a file
* Application and scheme names up to 63 characters
* Store as many frames as can fit in a file up to file size limits
* Data chunks up to (64-bit) x (32-bit) elements

The limits on only 16-bit name indices and 32-bit column indices are to keep the size of each index entry as small as
possible to avoid wasting space in the file index. The primary use cases in mind for column indices are Nx3 and Nx4
arrays for position and quaternion values. Schemas that wish to store larger truly n-dimensional arrays can store
their dimensionality in metadata in another chunk and store as an Nx1 index entry. Or use a file format more suited
to N-dimensional arrays such as HDF5.

Dependencies
------------

The file layer is implemented in C (*not C++*) with no dependencies to enable trivial
installation and incorporation into existing projects. A single header and C file completely implement
the entire file layer in a few hundred lines of code. Python based projects that need only read access can use
:py:mod:`gsd.flpy`, a pure python gsd reader implementation.

A python interface to the file layer allows reference implementations and convenience methods for schemas.
Most non-technical users of GSD will probably use these reference implementations directly in their scripts.

Boost will **not** be used so the python API will work on the widest possible number of systems. Instead, the low
level C library will be wrapped with cython. A python setup.py file will provide simple installation
on as many systems as possible. Cython c++ output is checked in to the repository so users do not even need
cython as a dependency.

File format
-----------

There are four types of data blocks in a GSD file.

#. Header block
    * Overall header for the entire file, contains the magic cookie, a format version, the name of the generating
      application, the schema name, and its version. Some bytes in the header are reserved
      for future use. Header size: 256 bytes. The header block also includes a pointer to the index, the number
      of allocated entries, the number of used entries in the index, a pointer to the name list, the size of the name
      list, and the number of entries used in the name list.
    * The header is the first 256 bytes in the file.
#. Index block
    * Index the frame data, size information, location, name id, etc...
    * The index contains space for any number of `index_entry` structs, the header indicates how many slots are used.
    * When the index fills up, a new index block is allocated at the end of the file with more space and all
      current index entries are rewritten there.
    * Index entry size: 32 bytes
#. Name list
    * List of string names used by index entries.
    * Each name is a `name_entry` struct, which holds up to 63 characters.
    * The header stores the total number of names available in the list and the number of name slots used.
#. Data chunk
    * Raw binary data stored for the named frame data blocks.

Header index, and name blocks are stored in memory as C structs (or arrays of C structs) and written to disk in
whole chunks.

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


* ``magic`` is the magic number identifying this as a GSD file (``0x65DF65DF65DF65DF``)
* ``gsd_version`` is the version number of the gsd file layer (``0xaaaabbbb => aaaa.bbbb``)
* ``application`` is the name of the generating application
* ``schema`` is the name of the schema for data in this gsd file
* ``schema_version`` is the version of the schema (``0xaaaabbbb => aaaa.bbbb``)
* ``index_location`` is the file location f the index block
* ``index_allocated_entries`` is the number of entries allocated in the index block
* ``namelist_location`` is the file location of the namelist block
* ``namelist_allocated_entries`` is the number of entries allocated in the namelist block
* ``reserved`` are bytes saved for future use

This structure is ordered so that all known compilers at the time of writing produced a tightly packed 256-byte header.
Some compilers may required non-standard packing attributes or pragmas to enforce this.

Index block
^^^^^^^^^^^

An Index block is made of a number of line items that store a pointer to a single data chunk::

    struct gsd_index_entry
        {
        uint64_t frame;
        uint64_t N;
        int64_t location;
        uint32_t M;
        uint16_t id;
        uint8_t type;
        uint8_t flags;
        };

* ``frame`` is the index of the frame this chunk belongs to
* ``N`` and ``M`` define the dimensions of the data matrix (NxM in C ordering with M as the fast index).
* ``location`` is the location of the data chunk in the file
* ``id`` is the index of the name of this entry in the namelist.
* ``type`` is the type of the data (char, int, float, double) indicated by index values
* ``flags`` is reserved for future use (it rounds the struct size out to 32 bytes).


Many ``gsd_index_entry_t`` structs are combined into one index block. They are stored densely packed and in the same
order as the corresponding data chunks are written to the file.

This structure is ordered so that all known compilers at the time of writing produced a tightly packed 32-byte entry.
Some compilers may required non-standard packing attributes or pragmas to enforce this.

The frame index must monotonically increase from one index entry to the next. The GSD API ensures this.

Namelist block
^^^^^^^^^^^^^^

An namelist block is made of a number of line items that store the string name of a data chunk entry::

    struct gsd_namelist_entry
        {
        char name[64];
        };

The ``id`` field of the index entry refers to the index of the name within the namelist entry.

Data block
^^^^^^^^^^

A data block is just raw data bytes on the disk. For a given index entry ``entry``, the data starts at location
``entry.location`` and is the next ``entry.N * entry.M * gsd_sizeof_type(entry.type)`` bytes.

API and implementation thoughts
-------------------------------

The C-level API is object oriented through the use of the handle structure. In the handle, the API will store
cached index data in memory and so forth. A pointer to the handle will be passed in to every API call.

* ``int gsd_create()`` : Create a GSD file on disk, overwriting any existing file.
* ``gsd_handle_t* gsd_open()`` : Open a GSD file and return an allocated handle.
* ``int gsd_close()`` : Close a GSD file and free all memory associated with it.
* ``int gsd_end_frame()`` : Complete writing the current frame and flush it to disk. This automatically
                            starts a new frame.
* ``int gsd_write_chunk()`` : Write a chunk out to the current frame
* ``uint64_t gsd_get_nframes()`` : Get the number of frames written to the file
* ``int gsd_index_entry_t* gsd_find_chunk()`` : Find a chunk with the given name in the given frame.
* ``int gsd_read_chunk()`` : Read data from a given chunk (must find the chunk first with ``gsd_find_chunk``).

``gsd_open`` will open the file, read all of the index blocks in to memory, and determine some things it will need later.
The index block is stored in memory to facilitate fast lookup of frames and named data chunks in frames.

``gsd_end_frame`` increments the current frame counter and writes the current index block to disk.

``gsd_write_chunk`` seeks to the end of the file and writes out the chunk. Then it updates the cached index block with
a new entry. If the current index block is full, it will create a new, larger one at the end
of the file. Normally, ``write_chunk`` only updates the data in the index cache. Only a call to ``gsd_end_frame`` writes
out the updated index. This facilitates contiguous writes and helps ensure that all frame data blocks are
completely written in a self-consistent way.

Failure modes
-------------

GSD is resistant to failures. The code aggressively checks for failures in memory allocations,
and verifies that ``write()`` and ``read()`` return the correct number of bytes after each call. Any time an error
condition hits, the current function call aborts.

GSD has a protections against invalid data in files. A specially constructed file may still be able to cause
problems, but at GSD tries to stop if corrupt data is present in a variety of ways.

* The header has a magic number. If it is invalid, GSD reports an error on open. This
  guards against corrupt file headers.
* Before allocating memory for the index block, GSD verifies that the index block is contained within the file.
* When writing chunks, data is appended to the end of the file and the index is updated *in memory*. After all chunks
  for the current frame are written, the user calls ``gsd_end_frame()`` which writes out the updated index and header.
  This way, if the process is killed in the middle of writing out a frame, the index will not contain entries for the
  partially written data. Such a file could still be appended to safely.
* If an index entry lists a size that goes past the end of the file, ``read_chunk`` will return an error.
