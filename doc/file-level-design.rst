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
    * each frame has an associated time step
    * resilient to job kills
* queries
    * last time step written
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

Dependencies
------------

The file layer is implemented in C (*not C++*) with no dependencies to enable trivial
installation and incorporation into existing projects. A single header and C file completely implement
the entire file layer in a few hundred lines of code.

A python interface to the file layer allows reference implementations and convenience methods for schemas.
Most non-technical users of GSD will probably use these reference implementations directly in their scripts.

Boost will **not** be used to enable the python API on the widest possible number of systems. Instead, the low
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
      of allocated entries, the number of used entries in the index, a pointer to the name list, the size of the name list, and the number of entries used in the name list.
    * The header is the first 256 bytes in the file.
#. Index block
    * Index the frame data, size information, location, name id, etc...
    * The index contains space for any number of `index_entry` structs, the header indicates how many slots are used.
    * When the index fills up, a new index block is allocated at the end of the file with more space and all
      current index entries are rewritten there.
    * Index entry size: 45 bytes
#. Name list
    * List of string names used by index entries.
    * Each name is a `name_entry` struct, which holds up to 128 characters.
    * The header stores the total number of names available in the list and the number of name slots used.
#. Data chunk
    * Raw binary data stored for the named frame data blocks.

Header index, and name blocks are stored in memory as C structs (or arrays of C structs) and written to disk in
whole chunks.

Header block
^^^^^^^^^^^^

This is the header block::

    struct gsd_header_t
        {
        uint64_t magic;
        uint32_t gsd_version;
        char application[64];
        char schema[64];
        uint32_t schema_version;
        uint64_t index_location;
        uint64_t index_allocated_entries;
        uint64_t namelist_location;
        uint64_t namelist_allocated_entries;
        char reserved[80];
        } gsd_header_t;


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

Index block
^^^^^^^^^^^

An Index block is made of a number of line items that store a pointer to a single data chunk::

    struct gsd_index_entry_t
        {
        uint64_t frame;
        uint64_t N;
        uint64_t M;
        uint64_t step;
        int64_t location;
        uint32_t id;
        uint8_t type;
        };


* ``frame`` is the index of the frame this chunk belongs to
* ``N`` and ``M`` define the dimensions of the data matrix (NxM in C ordering with M as the fast index).
* ``step`` is the time step the data is saved at
* ``location`` is the location of the data chunk in the file
* ``id`` is the index of the name of this entry in the namelist.
* ``type`` is the type of the data (char, int, float, double) indicated by index values


Many ``gsd_index_entry_t`` structs are combined into one index block. They are stored densely packed and in the same order
as the corresponding data chunks are written to the file.

The frame index must monotonically increase from one index entry to the next. The GSD API ensures this.

Data block
^^^^^^^^^^

A data block is just raw data bytes on the disk. For a given index entry ``entry``, the data starts at location
``entry.location`` and is the next ``entry.N * entry.M * gsd_sizeof_type(entry.type)`` bytes.

API and implementation thoughts
-------------------------------

The C-level API is object oriented through the use of the handle structure. In the handle, the API will store
cached index data in memory and so forth. A pointer to the handle will be passed in to every API call.

* ``int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version)`` : Create a GSD file on disk, overwriting any existing file.
* ``gsd_handle_t* gsd_open(const char *fname, const uint8_t flags)`` : Open a GSD file and return an allocated handle.
* ``int gsd_close(gsd_handle_t* handle)`` : Close a GSD file and free all memory associated with it.
* ``int gsd_end_frame(gsd_handle_t* handle)`` : Start a new frame in the GSD file.
* ``int gsd_write_chunk(gsd_handle_t* handle, const char *name, uint8_t type, uint64_t N, uint64_t M, uint64_t step, const void *data)`` : Write a chunk out to the current frame
* ``uint64_t gsd_get_last_step(gsd_handle_t* handle)`` : Get the value of the timestep last written to the file
* ``uint64_t gsd_get_nframes(gsd_handle_t* handle)`` : Get the number of frames written to the file
* ``gsd_index_entry_t* gsd_find_chunk(gsd_handle_t* handle, uint64_t frame, char *name)`` : Find a chunk with the given name in the given frame.
* ``int gsd_read_chunk(gsd_handle_t* handle, void* data, const gsd_index_entry_t* chunk)`` : Read data from a given chunk (must find the chunk first with ``gsd_find_chunk``).

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

* The header has a magic number at the start and end. If either is invalid, GSD reports an error on open. This
  guards against corrupt file headers.
* Before allocating memory for the index block, GSD verifies that the index block is contained within the file.
* When writing chunks, data is appended to the end of the file and the index is updated *in memory*. After all chunks
  for the current frame are written, the user calls ``gsd_end_frame()`` which writes out the updated index and header.
  This way, if the process is killed in the middle of writing out a frame, the index will not contain entries for the
  partially written data. Such a file could still be appended to safely.
* Each index entry is checksummed. If the checksum does not verify, ``read_chunk`` will return an error.
* If an index entry lists a size that goes past the end of the file, ``read_chunk`` will return an error.
