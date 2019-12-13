// Copyright (c) 2016-2019 The Regents of the University of Michigan
// This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

#ifndef GSD_H
#define GSD_H

#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/*! \file gsd.h
    \brief Declare GSD data types and C API
*/

/// Identifiers for the gsd data chunk element types
enum gsd_type
    {
    GSD_TYPE_UINT8=1,
    GSD_TYPE_UINT16,
    GSD_TYPE_UINT32,
    GSD_TYPE_UINT64,
    GSD_TYPE_INT8,
    GSD_TYPE_INT16,
    GSD_TYPE_INT32,
    GSD_TYPE_INT64,
    GSD_TYPE_FLOAT,
    GSD_TYPE_DOUBLE
    };

/// Flag for GSD file open options
enum gsd_open_flag
    {
    GSD_OPEN_READWRITE=1,
    GSD_OPEN_READONLY,
    GSD_OPEN_APPEND
    };

/// Maximum size of a GSD chunk name in memory
enum { GSD_NAME_SIZE = 64 };

/// Reserved bytes in the header structure
enum { GSD_RESERVED_BYTES = 80 };

/** GSD file header

    The in-memory and on-disk storage of the GSD file header. Stored in the first 256 bytes of the
    file.

    @warning All members are **read-only** to the caller.
*/
struct gsd_header
    {
    /// Magic number marking that this is a GSD file.
    uint64_t magic;

    /// Location of the chunk index in the file.
    uint64_t index_location;

    /// Number of index entries that will fit in the space allocated.
    uint64_t index_allocated_entries;

    /// Location of the name list in the file.
    uint64_t namelist_location;

    /// Number of namelist entries that will fit in the space allocated.
    uint64_t namelist_allocated_entries;

    /// Schema version: from gsd_make_version().
    uint32_t schema_version;

    /// GSD file format version from gsd_make_version().
    uint32_t gsd_version;

    /// Name of the application that generated this file.
    char application[GSD_NAME_SIZE];

    /// Name of data schema.
    char schema[GSD_NAME_SIZE];

    /// Reserved for future use.
    char reserved[GSD_RESERVED_BYTES];
    };

/** Index entry

    An index entry for a single chunk of data.

    @warning All members are **read-only** to the caller.
*/
struct gsd_index_entry
    {
    /// Frame index of the chunk.
    uint64_t frame;

    /// Number of rows in the chunk.
    uint64_t N;

    /// Location of the chunk in the file.
    int64_t location;

    /// Number of columns in the chunk.
    uint32_t M;

    /// Index of the chunk name in the name list.
    uint16_t id;

    /// Data type of the chunk: one of gsd_type.
    uint8_t type;

    /// Flags (for internal use).
    uint8_t flags;
    };

/** Namelist entry

     An entry in the list of data chunk names

    @warning All members are **read-only** to the caller.
*/
struct gsd_namelist_entry
    {
    /// Entry name
    char name[GSD_NAME_SIZE];
    };

/** File handle

    A handle to an open GSD file.

    This handle is obtained when opening a GSD file and is passed into every method that operates
    on the file.

    @warning All members are **read-only** to the caller.
*/
struct gsd_handle
    {
    /// File descriptor
    int fd;

    /// The file header
    struct gsd_header header;

    /// Pointer to mapped data
    void *mapped_data;

    /// Size of temporary buffer to store index entries to append
    size_t append_index_size;

    /// Pointer to the data chunk index
    struct gsd_index_entry *index;

    /// Pointer to the name list
    struct gsd_namelist_entry *namelist;

    /// Number of entries in the name list
    uint64_t namelist_num_entries;

    /// Number of index entries comitted to the file
    uint64_t index_written_entries;

    /// Number of entries in the index
    uint64_t index_num_entries;

    /// The index of the last frame in the file
    uint64_t cur_frame;

    /// Size of the file (in bytes)
    int64_t file_size;

    /// Flags passed to gsd_open() when opening this handle
    enum gsd_open_flag open_flags;

    /// Whether the handle requires an fsync call (new data was written)
    bool needs_sync;
    };

/** Specify a version

    @param major major version
    @param minor minor version

    @return a packed version number aaaa.bbbb suitable for storing in a gsd file version entry.
*/
uint32_t gsd_make_version(unsigned int major, unsigned int minor);

/** Create a GSD file

    @param fname File name.
    @param application Generating application name (truncated to 63 chars).
    @param schema Schema name for data to be written in this GSD file (truncated to 63 chars).
    @param schema_version Version of the scheme data to be written (make with gsd_make_version()).

    @post Create an empty gsd file in a file of the given name. Overwrite any existing file at that
    location.

    The generated gsd file is not opened. Call gsd_open() to open it for writing.

    @return 0 on success, -1 on a file IO failure - see errno for details
*/
int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version);

/** Create and open a GSD file

    @param handle Handle to open.
    @param fname File name.
    @param application Generating application name (truncated to 63 chars).
    @param schema Schema name for data to be written in this GSD file (truncated to 63 chars).
    @param schema_version Version of the scheme data to be written (make with gsd_make_version()).
    @param flags Either GSD_OPEN_READWRITE, or GSD_OPEN_APPEND.
    @param exclusive_create Set to non-zero to force exclusive creation of the file.

    @post Create an empty gsd file with the given name. Overwrite any existing file at that
    location.

    Open the generated gsd file in *handle*.

    The file descriptor is closed if there when an error opening the file.

    @return 0 on success. Negative value on failure:
        * -1: IO error (check errno)
        * -2: Not a GSD file
        * -3: Invalid GSD file version
        * -4: Corrupt file
        * -5: Unable to allocate memory
        * -6: Invalid argument
*/
int gsd_create_and_open(struct gsd_handle* handle,
                        const char *fname,
                        const char *application,
                        const char *schema,
                        uint32_t schema_version,
                        enum gsd_open_flag flags,
                        int exclusive_create);

/** Open a GSD file

    @param handle Handle to open.
    @param fname File name to open.
    @param flags Either GSD_OPEN_READWRITE, GSD_OPEN_READONLY, or GSD_OPEN_APPEND.

    @pre The file name *fname* is a GSD file.

    @post Open a GSD file and populates the handle for use by API calls.

    The file descriptor is closed if there is an error opening the file.

    Prefer the modes GSD_OPEN_APPEND for writing and GSD_OPEN_READONLY for reading. These modes are
    optimized to only load as much of the index as needed. GSD_OPEN_READWRITE needs to store the
    entire index in memory: in files with millions of chunks, this can add up to GiB.

    @return 0 on success. Negative value on failure:
        * -1: IO error (check errno)
        * -2: Not a GSD file
        * -3: Invalid GSD file version
        * -4: Corrupt file
        * -5: Unable to allocate memory
*/
int gsd_open(struct gsd_handle* handle, const char *fname, enum gsd_open_flag flags);

/** Truncate a GSD file

    @param handle Open GSD file to truncate.

    After truncating, a file will have no frames and no data chunks. The file size will be that of a
    newly created gsd file. The application, schema, and schema version metadata will be kept.
    Truncate does not close and reopen the file, so it is suitable for writing restart files on
    Lustre file systems without any metadata access.

    @return 0 on success. Negative value on failure:
      * -1: IO error (check errno)
      * -2: Invalid input
      * -3: Invalid GSD file version
      * -4: Corrupt file
      * -5: Unable to allocate memory
*/
int gsd_truncate(struct gsd_handle* handle);

/** Close a GSD file

    @param handle GSD file to close.

    @pre *handle* was opened by gsd_open().
    @pre gsd_end_frame() has been called since the last call to gsd_write_chunk().

    @post The file is closed.
    @post *handle* is freed and can no longer be used.

    @warning Do not write chunks to the file with gsd_write_chunk() and then immediately close the
    file with gsd_close(). This will result in data loss. Data chunks written by gsd_write_chunk()
    are not updated in the index until gsd_end_frame() is called. This is by design to prevent
    partial frames in files.

    @return 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
*/
int gsd_close(struct gsd_handle* handle);

/** Commit the current frame and increment the frame counter.

    @param handle Handle to an open GSD file

    @pre *handle* was opened by gsd_open().
    @pre gsd_write_chunk() has been called at least once since the last call to gsd_end_frame().

    @post The current frame counter is increased by 1 and cached indexes are written to disk.

    @return 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
*/
int gsd_end_frame(struct gsd_handle* handle);

/** Write a data chunk to the current frame

    @param handle Handle to an open GSD file.
    @param name Name of the data chunk (truncated to 63 chars).
    @param type type ID that identifies the type of data in *data*.
    @param N Number of rows in the data.
    @param M Number of columns in the data.
    @param flags set to 0, non-zero values reserved for future use.
    @param data Data buffer.

    @pre *handle* was opened by gsd_open().
    @pre *name* is a unique name for data chunks in the given frame.
    @pre data is allocated and contains at least `N * M * gsd_sizeof_type(type)` bytes.

    @post The given data chunk is written to the end of the file and its location is updated in the
    in-memory index.

    @return 0 on success, -1 on a file IO failure - see errno for details, -2 on invalid input, and
    -3 when out of names
*/
int gsd_write_chunk(struct gsd_handle* handle,
                    const char *name,
                    enum gsd_type type,
                    uint64_t N,
                    uint32_t M,
                    uint8_t flags,
                    const void *data);

/** Find a chunk in the GSD file

    @param handle Handle to an open GSD file
    @param frame Frame to look for chunk
    @param name Name of the chunk to find

    @pre *handle* was opened by gsd_open() in read or readwrite mode.

    The found entry contains size and type metadata and can be passed to gsd_read_chunk() to read
    the data.

    @return A pointer to the found chunk, or NULL if not found
*/
const struct gsd_index_entry* gsd_find_chunk(struct gsd_handle* handle, uint64_t frame, const char *name);

/** Read a chunk from the GSD file

    @param handle Handle to an open GSD file.
    @param data Data buffer to read into.
    @param chunk Chunk to read.

    @pre *handle* was opened in read or readwrite mode.
    @pre *chunk* was found by gsd_find_chunk().
    @pre *data* points to an allocated buffer with at least `N * M * gsd_sizeof_type(type)` bytes.

    @return 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
*/
int gsd_read_chunk(struct gsd_handle* handle, void* data, const struct gsd_index_entry* chunk);

/** Get the number of frames in the GSD file

    @param handle Handle to an open GSD file

    @pre *handle* was opened by gsd_open().

    @return The number of frames in the file, or 0 on error.
*/
uint64_t gsd_get_nframes(struct gsd_handle* handle);

/** Query size of a GSD type ID.

    @param type Type ID to query.

    @return Size of the given type in bytes, or 0 for an unknown type ID.
*/
size_t gsd_sizeof_type(enum gsd_type type);

/** Search for chunk names in a gsd file.

    @param handle Handle to an open GSD file.
    @param match String to match.
    @param prev Search starting point.

    @pre *handle* was opened by gsd_open()
    @pre *prev* was returned by a previous call to gsd_find_matching_chunk_name()

    To find the first matching chunk name, pass NULL for prev. Pass in the previous found string to
    find the next after that, and so on. Chunk names match if they begin with the string in *match*.
    Chunk names returned by this function may be present in at least one frame.

    @return Pointer to a string, NULL if no more matching chunks are found found, or NULL if *prev*
    is invalid
*/
const char *gsd_find_matching_chunk_name(struct gsd_handle* handle, const char* match, const char *prev);

#ifdef __cplusplus
}
#endif

#endif  // #ifndef GSD_H
