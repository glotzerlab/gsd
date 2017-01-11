.. Copyright (c) 2016-2017 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

.. _c_api_:

C API
=====

The GSD C API consists of a single header and source file (less than 1k lines of
code). It does not build as a shared library. Instead, it is intended that
developers simply drop the implementation into any package that needs it.

Functions
---------

.. c:function:: int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version)

    Create an empty gsd file in a file of the given name. Overwrite any existing file at that location.
    The generated gsd file is not opened. Call gsd_open() to open it for writing.

    :param fname: File name
    :param application: Generating application name (truncated to 63 chars)
    :param schema: Schema name for data to be written in this GSD file (truncated to 63 chars)
    :param schema_version: Version of the scheme data to be written (make with :c:func:`gsd_make_version()`)

    :return: 0 on success, -1 on a file IO failure - see errno for details

.. c:function:: int gsd_open(struct gsd_handle* handle, const char *fname, const enum gsd_open_flag flags)

    Open a GSD file and populates the handle for use by later API calls.

    :param handle: Handle to open.
    :param fname: File name to open.
    :param flags: Either ``GSD_OPEN_READWRITE``, ``GSD_OPEN_READONLY``, or ``GSD_OPEN_APPEND``.

    Prefer the modes ``GSD_OPEN_APPEND`` for writing and ``GSD_OPEN_READONLY`` for reading. These modes are optimized
    to only load as much of the index as needed. ``GSD_OPEN_READWRITE`` needs to store the entire index in memory: in
    files with millions of chunks, this can add up to GiB.

    :return: 0 on success. Negative value on failure:

        * -1: IO error (check errno)
        * -2: Not a GSD file
        * -3: Invalid GSD file version
        * -4: Corrupt file
        * -5: Unable to allocate memory

.. c:function:: int gsd_truncate(gsd_handle_t* handle)

    Truncate a GSD file opened by :c:func:`gsd_open()`.

    After truncating, a file will have no frames and no data chunks. The file
    size will be that of a newly created gsd file. The application, schema,
    and schema version metadata will be kept. Truncate does not close and
    reopen the file, so it is suitable for writing restart files on Lustre
    file systems without any metadata access.

    :param handle: Handle to truncate.

    :return: 0 on success. Negative value on failure:

        * -1: IO error (check errno)
        * -2: Not a GSD file
        * -3: Invalid GSD file version
        * -4: Corrupt file
        * -5: Unable to allocate memory

.. c:function:: int gsd_close(gsd_handle_t* handle)

    Close a GSD file opened by :c:func:`gsd_open()`.
    Call :c:func:`gsd_end_frame()` after the last call to :c:func:`gsd_write_chunk()` **before** closing
    the file.

    :param handle: Handle to close.

    .. warning::
        Do not write chunks to the file with gsd_write_chunk() and then immediately close the file with
        :c:func:`gsd_close()`. This will result in data loss. Data chunks written by :c:func:`gsd_write_chunk()`
        are not updated in the index until :c:func:`gsd_end_frame()` is called. This is by design to
        prevent partial frames in files.

    :return: 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input

.. c:function:: int gsd_end_frame(gsd_handle_t* handle)

    Move on to the next frame after writing 1 or more chunks with :c:func:`gsd_write_chunk()`.
    Increase the frame counter by 1 and flush the cached index to disk.

    :param handle: Handle to an open GSD file.

    :return: 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input

.. c:function:: int gsd_write_chunk(struct gsd_handle* handle, const char *name, enum gsd_type type, uint64_t N, uint32_t M, uint8_t flags, const void *data)

    Write a data chunk to the current frame. The chunk name must be unique within each frame.
    The given data chunk is written to the end of the file and its location is updated in the in-memory index.
    The data pointer must be allocated and contain at least contains at least ``N * M * gsd_sizeof_type(type)`` bytes.

    :param handle: Handle to an open GSD file.
    :param name: Name of the data chunk (truncated to 63 chars).
    :param type: type ID that identifies the type of data in data.
    :param N: Number of rows in the data.
    :param M: Number of columns in the data.
    :param flags: Unused, set to 0
    :param data: Data buffer.

    :return: 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input

.. c:function:: const struct gsd_index_entry* gsd_find_chunk(struct gsd_handle* handle, uint64_t frame, const char *name)

    Find a chunk in the GSD file. The found entry contains size and type metadata and can be passed to
    :c:func:`gsd_read_chunk()` to read the data.

    :param handle: Handle to an open GSD file
    :param frame: Frame to look for chunk
    :param name: Name of the chunk to find

    :return: A pointer to the found chunk, or NULL if not found.

.. c:function:: int gsd_read_chunk(gsd_handle_t* handle, void* data, const gsd_index_entry_t* chunk)

    Read a chunk from the GSD file. The index entry must first be found by :c:func:`gsd_find_chunk()`.
    ``data`` must point to an allocated buffer with at least ``N * M * gsd_sizeof_type(type)`` bytes.

    :param handle: Handle to an open GSD file
    :param data: Data buffer to read into
    :param chunk: Chunk to read

    :return: 0 on success

        * -1 on a file IO failure - see errno for details
        * -2 on invalid input
        * -3 on invalid file data

.. c:function:: uint64_t gsd_get_nframes(gsd_handle_t* handle)

    Get the number of frames in the GSD file.

    :param handle: Handle to an open GSD file.

    :return: The number of frames in the file, or 0 on error.

.. c:function:: size_t gsd_sizeof_type(enum gsd_type type)

    Query size of a GSD type ID.

    :param type: Type ID to query

    :return: Size of the given type, or 1 for an unknown type ID.

.. c:function:: uint32_t gsd_make_version(unsigned int major, unsigned int minor)

    Specify a version number.

    :param major: major version.
    :param minor: minor version.

    :return: a packed version number aaaa.bbbb suitable for storing in a gsd file version entry.

Constants
---------

.. _data-types:

Data types
^^^^^^^^^^

.. c:var:: gsd_type GSD_TYPE_UINT8

    Type ID: 8-bit unsigned integer.

.. c:var:: gsd_type GSD_TYPE_UINT16

    Type ID: 16-bit unsigned integer.

.. c:var:: gsd_type GSD_TYPE_UINT32

    Type ID: 32-bit unsigned integer.

.. c:var:: gsd_type GSD_TYPE_UINT64

    Type ID: 64-bit unsigned integer.

.. c:var:: gsd_type GSD_TYPE_INT8

    Type ID: 8-bit signed integer.

.. c:var:: gsd_type GSD_TYPE_INT16

    Type ID: 16-bit signed integer.

.. c:var:: gsd_type GSD_TYPE_INT32

    Type ID: 32-bit signed integer.

.. c:var:: gsd_type GSD_TYPE_INT64

    Type ID: 64-bit signed integer.

.. c:var:: gsd_type GSD_TYPE_FLOAT

    Type ID: 32-bit single precision floating point.

.. c:var:: gsd_type GSD_TYPE_DOUBLE

    Type ID: 64-bit double precision floating point.

.. open-flags:

Open flags
^^^^^^^^^^

.. c:var:: gsd_open_flag GSD_OPEN_READWRITE

    Open file in **read/write**  mode.

.. c:var:: gsd_open_flag GSD_OPEN_READONLY

    Open file in **read only** mode.


Data structures
---------------

.. c:type:: gsd_handle_t

    Handle to an open GSD file. All members are **read-only**. Only public members are documented here.

    .. c:member:: gsd_header_t header

        File header. Use this field to access the header of the GSD file.

    .. c:member:: int64_t file_size

        Size of the open file in bytes.

    .. c:member:: gsd_open_flag open_flags

        Flags used to open the file.

.. c:type:: gsd_header_t

    GSD file header. Access version, application, and schema information.

    .. c:member:: uint32_t gsd_version

        File format version: 0xaaaabbbb => aaaa.bbbb

    .. c:member:: char application[64]

        Name of the application that wrote the file.

    .. c:member:: char schema[64]

        Name of schema defining the stored data.

    .. c:member:: uint32_t schema_version

        Schema version: 0xaaaabbbb => aaaa.bbbb

.. c:type:: gsd_index_entry_t

    Entry for a single data chunk in the GSD file.

    .. c:member:: uint64_t frame

        Frame index of the chunk.

    .. c:member:: uint64_t N

        Number of rows in the chunk data.

    .. c:member:: uint8_t M

        Number of columns in the chunk.

    .. c:member:: uint8_t type

        Data type of the chunk. See :ref:`data-types`.
