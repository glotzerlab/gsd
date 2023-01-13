.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

.. _c_api_:

C API
=====

The GSD C API consists of a single header and source file. Developers can drop
the implementation into any package that needs it.

Functions
---------

.. c:function:: int gsd_create(const char *fname, \
                               const char *application, \
                               const char *schema, \
                               uint32_t schema_version)

    Create an empty gsd file with the given name. Overwrite any existing file at
    that location. The generated gsd file is not opened. Call
    :c:func:`gsd_open()` to open it for writing.

    :param fname: File name (UTF-8 encoded).
    :param application: Generating application name (truncated to 63 chars).
    :param schema: Schema name for data to be written in this GSD file
      (truncated to 63 chars).
    :param schema_version: Version of the scheme data to be written (make with
      :c:func:`gsd_make_version()`).

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).

.. c:function:: int gsd_create_and_open(struct gsd_handle* handle, \
                                        const char *fname, \
                                        const char *application, \
                                        const char *schema, \
                                        uint32_t schema_version,  \
                                        gsd_open_flag flags, \
                                        int exclusive_create)

    Create an empty gsd file with the given name. Overwrite any existing
    file at that location. Open the generated gsd file in *handle*.

    :param handle: Handle to open.
    :param fname: File name (UTF-8 encoded).
    :param application: Generating application name (truncated to 63 chars).
    :param schema: Schema name for data to be written in this GSD file
      (truncated to 63 chars).
    :param schema_version: Version of the scheme data to be written (make with
      :c:func:`gsd_make_version()`).
    :param flags: Either ``GSD_OPEN_READWRITE``, or ``GSD_OPEN_APPEND``.
    :param exclusive_create: Set to non-zero to force exclusive creation of the
      file.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_NOT_A_GSD_FILE: Not a GSD file.
      * GSD_ERROR_INVALID_GSD_FILE_VERSION: Invalid GSD file version.
      * GSD_ERROR_FILE_CORRUPT: Corrupt file.
      * GSD_ERROR_MEMORY_ALLOCATION_FAILED: Unable to allocate memory.

.. c:function:: int gsd_open(struct gsd_handle* handle, \
                             const char *fname, \
                             gsd_open_flag flags)

    Open a GSD file and populates the handle for use by later API calls.

    :param handle: Handle to open.
    :param fname: File name to open (UTF-8 encoded).
    :param flags: Either ``GSD_OPEN_READWRITE``, ``GSD_OPEN_READONLY``, or
      ``GSD_OPEN_APPEND``.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_NOT_A_GSD_FILE: Not a GSD file.
      * GSD_ERROR_INVALID_GSD_FILE_VERSION: Invalid GSD file version.
      * GSD_ERROR_FILE_CORRUPT: Corrupt file.
      * GSD_ERROR_MEMORY_ALLOCATION_FAILED: Unable to allocate memory.

.. c:function:: int gsd_truncate(gsd_handle* handle)

    Truncate a GSD file.

    After truncating, a file will have no frames and no data chunks. The file
    size will be that of a newly created gsd file. The application, schema,
    and schema version metadata will be kept. Truncate does not close and
    reopen the file, so it is suitable for writing restart files on Lustre
    file systems without any metadata access.

    :param handle: Open GSD file to truncate.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_NOT_A_GSD_FILE: Not a GSD file.
      * GSD_ERROR_INVALID_GSD_FILE_VERSION: Invalid GSD file version.
      * GSD_ERROR_FILE_CORRUPT: Corrupt file.
      * GSD_ERROR_MEMORY_ALLOCATION_FAILED: Unable to allocate memory.

.. c:function:: int gsd_close(gsd_handle* handle)

    Close a GSD file.

    :param handle: GSD file to close.

    .. warning::
        Ensure that all :c:func:`gsd_write_chunk()` calls are committed with
        :c:func:`gsd_end_frame()` before closing the file.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_INVALID_ARGUMENT: *handle* is NULL.

.. c:function:: int gsd_end_frame(gsd_handle* handle)

    Commit the current frame and increment the frame counter.

    :param handle: Handle to an open GSD file.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_INVALID_ARGUMENT: *handle* is NULL.
      * GSD_ERROR_FILE_MUST_BE_WRITABLE: The file was opened read-only.
      * GSD_ERROR_MEMORY_ALLOCATION_FAILED: Unable to allocate memory.

.. c:function:: int gsd_write_chunk(struct gsd_handle* handle, \
                                    const char *name, \
                                    gsd_type type, \
                                    uint64_t N, \
                                    uint32_t M, \
                                    uint8_t flags, \
                                    const void *data)

    Write a data chunk to the current frame. The chunk name must be unique
    within each frame. The given data chunk is written to the end of the file
    and its location is updated in the in-memory index. The data pointer must be
    allocated and contain at least contains at least ``N * M *
    gsd_sizeof_type(type)`` bytes.

    :param handle: Handle to an open GSD file.
    :param name: Name of the data chunk.
    :param type: type ID that identifies the type of data in *data*.
    :param N: Number of rows in the data.
    :param M: Number of columns in the data.
    :param flags: Unused, set to 0.
    :param data: Data buffer.

    .. note:: If the GSD file is version 1.0, the chunk name is truncated to 63
              bytes. GSD version 2.0 files support arbitrarily long names.

    :return:

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_INVALID_ARGUMENT: *handle* is NULL, *N* == 0, *M* == 0, *type* is invalid, or
        *flags* != 0.
      * GSD_ERROR_FILE_MUST_BE_WRITABLE: The file was opened read*only.
      * GSD_ERROR_NAMELIST_FULL: The file cannot store any additional unique chunk names.
      * GSD_ERROR_MEMORY_ALLOCATION_FAILED: failed to allocate memory.

.. c:function:: const struct gsd_index_entry_t* gsd_find_chunk( \
                             struct gsd_handle* handle, \
                             uint64_t frame, \
                             const char *name)

    Find a chunk in the GSD file. The found entry contains size and type
    metadata and can be passed to :c:func:`gsd_read_chunk()` to read the data.

    :param handle: Handle to an open GSD file.
    :param frame: Frame to look for chunk.
    :param name: Name of the chunk to find.

    :return: A pointer to the found chunk, or NULL if not found.

.. c:function:: int gsd_read_chunk(gsd_handle* handle, \
                                   void* data, \
                                   const gsd_index_entry_t* chunk)

    Read a chunk from the GSD file. The index entry must first be found by
    :c:func:`gsd_find_chunk()`. ``data`` must point to an allocated buffer with
    at least ``N * M * gsd_sizeof_type(type)`` bytes.

    :param handle: Handle to an open GSD file.
    :param data: Data buffer to read into.
    :param chunk: Chunk to read.

    :return: 0 on success

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_INVALID_ARGUMENT: *handle* is NULL, *data* is NULL, or *chunk* is NULL.
      * GSD_ERROR_FILE_MUST_BE_READABLE: The file was opened in append mode.
      * GSD_ERROR_FILE_CORRUPT: The GSD file is corrupt.

.. c:function:: uint64_t gsd_get_nframes(gsd_handle* handle)

    Get the number of frames in the GSD file.

    :param handle: Handle to an open GSD file.

    :return: The number of frames in the file, or 0 on error.

.. c:function:: size_t gsd_sizeof_type(gsd_type type)

    Query size of a GSD type ID.

    :param type: Type ID to query

    :return: Size of the given type, or 0 for an unknown type ID.

.. c:function:: uint32_t gsd_make_version(unsigned int major, \
                                          unsigned int minor)

    Specify a version number.

    :param major: major version.
    :param minor: minor version.

    :return: a packed version number aaaa.bbbb suitable for storing in a gsd
      file version entry.

.. c:function:: const char *gsd_find_matching_chunk_name( \
                              struct gsd_handle* handle, \
                              const char* match, \
                              const char *prev)

    Search for chunk names in a gsd file.

    :param handle: Handle to an open GSD file.
    :param match: String to match.
    :param prev: Search starting point.

    To find the first matching chunk name, pass ``NULL`` for ``prev``. Pass in
    the previous found string to find the next after that, and so on. Chunk
    names match if they *begin* with the string in ``match``. Chunk names
    returned by this function may be present in at least one frame.

    :return: Pointer to a string, ``NULL`` if no more matching chunks are found
      found, or ``NULL`` if ``prev`` is invalid.

.. c:function:: int gsd_upgrade(gsd_handle* handle)

    Upgrade a GSD file to the latest specification.

    :param handle: Handle to an open GSD file.

    :return: 0 on success

      * GSD_SUCCESS (0) on success. Negative value on failure:
      * GSD_ERROR_IO: IO error (check errno).
      * GSD_ERROR_INVALID_ARGUMENT: *handle* is NULL, *data* is NULL, or *chunk*
        is NULL.
      * GSD_ERROR_FILE_MUST_BE_WRITEABLE: The file was opened in the read only
        mode.

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

.. c:var:: gsd_open_flag GSD_OPEN_APPEND

    Open file in **append only** mode.

Error values
^^^^^^^^^^^^

.. c:var:: gsd_error GSD_SUCCESS

    Success.

.. c:var:: gsd_error GSD_ERROR_IO

    IO error. Check ``errno`` for details.

.. c:var:: gsd_error GSD_ERROR_INVALID_ARGUMENT

    Invalid argument passed to function.

.. c:var:: gsd_error GSD_ERROR_NOT_A_GSD_FILE

    The file is not a GSD file.

.. c:var:: gsd_error GSD_ERROR_INVALID_GSD_FILE_VERSION

    The GSD file version cannot be read.

.. c:var:: gsd_error GSD_ERROR_FILE_CORRUPT

    The GSD file is corrupt.

.. c:var:: gsd_error GSD_ERROR_MEMORY_ALLOCATION_FAILED

    GSD failed to allocated memory.

.. c:var:: gsd_error GSD_ERROR_NAMELIST_FULL

    The GSD file cannot store any additional unique data chunk names.

.. c:var:: gsd_error GSD_ERROR_FILE_MUST_BE_WRITABLE

    This API call requires that the GSD file opened in with the mode
    GSD_OPEN_APPEND or GSD_OPEN_READWRITE.

.. c:var:: gsd_error GSD_ERROR_FILE_MUST_BE_READABLE

    This API call requires that the GSD file opened the mode GSD_OPEN_READ
    or GSD_OPEN_READWRITE.


Data structures
---------------

.. c:type:: gsd_handle

    Handle to an open GSD file. All members are **read-only**. Only public
    members are documented here.

    .. c:member:: gsd_header_t header

        File header. Use this field to access the header of the GSD file.

    .. c:member:: int64_t file_size

        Size of the open file in bytes.

    .. c:member:: gsd_open_flag open_flags

        Flags used to open the file.

.. c:type:: gsd_header_t

    GSD file header. Access version, application, and schema information.

    .. c:member:: uint32_t gsd_version

        GSD file format version from :c:func:`gsd_make_version()`

    .. c:member:: char application[64]

        Name of the application that generated this file.

    .. c:member:: char schema[64]

        Name of data schema.

    .. c:member:: uint32_t schema_version

        Schema version from :c:func:`gsd_make_version()`.

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

.. c:type:: gsd_open_flag

    Enum defining the file open flag. Valid values are ``GSD_OPEN_READWRITE``,
    ``GSD_OPEN_READONLY``, and ``GSD_OPEN_APPEND``.

.. c:type:: gsd_type

    Enum defining the file type of the GSD data chunk.

.. c:type:: gsd_error

    Enum defining the possible error return values.

.. c:type:: uint8_t

    8-bit unsigned integer (defined by C compiler).

.. c:type:: uint32_t

    32-bit unsigned integer (defined by C compiler).

.. c:type:: uint64_t

    64-bit unsigned integer (defined by C compiler).

.. c:type:: int64_t

    64-bit signed integer (defined by C compiler).

.. c:type:: size_t

    unsigned integer (defined by C compiler).
