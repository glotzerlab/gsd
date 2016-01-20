.. _c_api_:

C API
=====

Functions
---------

.. c:function:: int gsd_create(const char *fname,
                               const char *application,
                               const char *schema,
                               uint32_t schema_version);

    Create a GSD file.

.. c:function:: gsd_handle_t* gsd_open(const char *fname, const uint8_t flags);

    Open a GSD file for read/write.

.. c:function:: int gsd_close(gsd_handle_t* handle);

    Close a GSD file.

.. c:function:: int gsd_end_frame(gsd_handle_t* handle);

    Move on to the next frame.

.. c:function:: int gsd_write_chunk(gsd_handle_t* handle, \
                     const char *name, \
                     uint8_t type, \
                     uint64_t N, \
                     uint64_t M, \
                     uint64_t step, \
                     const void *data);

    Write a data chunk to the current frame.

.. c:function:: gsd_index_entry_t* gsd_find_chunk(gsd_handle_t* handle, uint64_t frame, const char *name);

    Find a chunk in the GSD file.

.. c:function:: int gsd_read_chunk(gsd_handle_t* handle, void* data, const gsd_index_entry_t* chunk);

    Read a chunk from the GSD file.

.. c:function:: uint64_t gsd_get_last_step(gsd_handle_t* handle);

    Query the last time step in the GSD file.

.. c:function:: uint64_t gsd_get_nframes(gsd_handle_t* handle);

    Get the number of frames in the GSD file.

.. c:function:: size_t gsd_sizeof_type(uint8_t type);

    Query size of a GSD type ID.

Constants
---------

.. _data-types:

Data types
^^^^^^^^^^

.. c:var:: uint8_t GSD_UINT8_TYPE

    Type ID: 8-bit unsigned integer.

.. c:var:: uint8_t GSD_UINT32_TYPE

    Type ID: 32-bit unsigned integer.

.. c:var:: uint8_t GSD_FLOAT_TYPE

    Type ID: 32-bit single precision floating point.

.. c:var:: uint8_t GSD_DOUBLE_TYPE

    Type ID: 64-bit double precision floating point.

.. open-flags:

Open flags
^^^^^^^^^^

.. c:var:: uint8_t GSD_OPEN_READWRITE

    Open file in **read/write**  mode.

.. c:var:: uint8_t GSD_OPEN_READONLY

    Open file in **read only** mode.


Data structures
---------------

.. c:type:: gsd_handle_t

    Handle to an open GSD file. All members are **read-only**.

    .. c:member:: gsd_header_t header

        File header. Use this field to access the header of the GSD file.

    .. c:member:: int64_t file_size

        Size of the open file.

    .. c:member:: uint8_t open_flags

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

    .. c:member:: uint64_t M

        Number of columns in the chunk.

    .. c:member:: uint64_t step

        Timestep the chunk was saved at.

    .. c:member:: char name[33]

        Name of the chunk.

    .. c:member:: uint8_t type

        Data type of the chunk. See :ref:`data-types`.
