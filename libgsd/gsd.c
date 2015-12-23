/* Copyright (c) The Regents of the University of Michigan
This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License:
(http://opensource.org/licenses/BSD-2-Clause).
*/

#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>

#include "gsd.h"

/*! \file gsd.c
    \brief Implements the GSD C API
*/

/*! \internal
    \brief Utility function to expand the memory space for the index block
    \ingroup c_api
*/
static int __gsd_expand_index(gsd_handle_t *handle)
    {
    // multiply the index size each time it grows
    // this allows the index to grow rapidly to accommodate new frames
    const int multiplication_factor = 2;

    // save the old size
    gsd_index_entry_t *old_array = handle->index;
    size_t old_size = handle->header.index_allocated_entries;

    // allocate the new larger index block
    handle->index = (gsd_index_entry_t *)malloc(sizeof(gsd_index_entry_t) * old_size * multiplication_factor);
    if (handle->index == NULL)
        return -1;

    // zero the memory
    memset(handle->index, 0, sizeof(gsd_index_entry_t) * old_size * multiplication_factor);

    // copy the old to the new slot and deallocate the old
    memcpy(handle->index, old_array, sizeof(gsd_index_entry_t) * old_size);
    handle->header.index_allocated_entries = old_size * multiplication_factor;
    free(old_array);

    // now, put the new larger index at the end of the file
    handle->header.index_location = lseek(handle->fd, 0, SEEK_END);
    size_t bytes_written = write(handle->fd, handle->index, sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries);
    if (bytes_written != sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries)
        return -1;

    // set the new file size
    handle->file_size = handle->header.index_location + bytes_written;

    // write the new header out
    handle->header.checksum = handle->header.gsd_version +
                              handle->header.schema_version +
                              handle->header.index_location +
                              handle->header.index_allocated_entries;

    lseek(handle->fd, 0, SEEK_SET);
    bytes_written = write(handle->fd, &(handle->header), sizeof(gsd_header_t));
    if (bytes_written != sizeof(gsd_header_t))
        return -1;

    return 0;
    }

/*! \param fname File name
    \param application Generating application name (truncated to 63 chars)
    \param schema Schema name for data to be written in this GSD file (truncated to 63 chars)
    \param schema_version Version of the scheme data to be written (0xaabbcc is aa.bb.cc)

    \post Creates an empty gsd file in a file of the given name. Overwrites any existing file at that location.

    The generated gsd file is not opened. Call gsd_open() to open it for writing.

    \returns 0 on success, -1 on a file IO failure - see errno for details
    \ingroup c_api
*/
int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version)
    {
    // create the file
    int fd = open(fname, O_RDWR | O_CREAT | O_TRUNC,  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);

    // check if the file was created
    if (fd == -1)
        return -1;

    // populate header fields
    gsd_header_t header;
    memset(&header, 0, sizeof(header));

    header.magic = 0x65DF65DF65DF65DF;
    header.version = 0x00000001;
    strncpy(header.application, application, sizeof(header.application)-1);
    header.application[sizeof(header.application)-1] = 0;
    strncpy(header.schema, schema, sizeof(header.schema)-1);
    header.schema[sizeof(header.schema)-1] = 0;
    header.schema_version = schema_version;
    header.index_location = sizeof(header);
    header.index_allocated_entries = 128;
    memset(header.reserved, 0, sizeof(header.reserved));
    header.checksum = header.gsd_version + header.schema_version + header.index_location + header.index_allocated_entries;

    // write the header out
    size_t bytes_written = write(fd, &header, sizeof(header));
    if (bytes_written != sizeof(header))
        return -1;

    // allocate and zero default index memory
    gsd_index_entry_t index[128];
    memset(index, 0, sizeof(index));

    // write the empty index out
    bytes_written = write(fd, index, sizeof(index));
    if (bytes_written != sizeof(index))
        return -1;

    return 0;
    }

/*! \param fname File name to open
    \param flags Either GSD_OPEN_READWRITE or GSD_OPEN_READONLY

    \pre The file name \a fname is a GSD file.

    \post Opens a GSD file and populates the handle for use by API calls.

    \returns An allocated pointer on success, NULL on failure. Check errno for potential causes of the error.
    \ingroup c_api
*/
gsd_handle_t* gsd_open(const char *fname, const uint8_t flags)
    {
    // allocate the handle
    // printf("Allocating\n");
    gsd_handle_t *handle = (gsd_handle_t *)malloc(sizeof(gsd_handle_t));
    if (handle == NULL)
        return NULL;
    memset(handle, 0, sizeof(gsd_handle_t));
    handle->index = NULL;
    handle->cur_frame = 0;

    // create the file
    // printf("Opening\n");
    if (flags == GSD_OPEN_READWRITE)
        {
        handle->fd = open(fname, O_RDWR);
        handle->open_flags = GSD_OPEN_READWRITE;
        }
    else if (flags == GSD_OPEN_READONLY)
        {
        handle->fd = open(fname, O_RDONLY);
        handle->open_flags = GSD_OPEN_READONLY;
        }

    // check if the file was created
    if (handle->fd == -1)
        return NULL;

    // read the header
    // printf("Reading header\n");
    size_t bytes_read = read(handle->fd, &handle->header, sizeof(gsd_header_t));
    if (bytes_read != sizeof(gsd_header_t))
        return NULL;

    // validate the header
    // printf("Validating header\n");
    if (handle->header.magic != 0x65DF65DF65DF65DF)
        return NULL;
    if (handle->header.checksum != header.gsd_version + header.schema_version + header.index_location + header.index_allocated_entries)
        return NULL;

    // determine the file size
    handle->file_size = lseek(handle->fd, 0, SEEK_END);

    // validate that the index block exists inside the file
    if (handle->header.index_location + sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries > handle->file_size)
        return NULL;

    // read the index block
    // printf("Reading index\n");
    handle->index = (gsd_index_entry_t *)malloc(sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries);
    if (handle->index == NULL)
        return NULL;

    lseek(handle->fd, handle->header.index_location, SEEK_SET);
    bytes_read = read(handle->fd, handle->index, sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries);
    if (bytes_read != sizeof(gsd_index_entry_t) * handle->header.index_allocated_entries)
        return NULL;

    // determine the number of index entries (marked by location = 0)
    // base case: the index is full
    handle->index_num_entries = handle->header.index_allocated_entries;

    // general case, find the first index entry with location 0
    size_t i;
    for (i = 0; i < handle->header.index_allocated_entries; i++)
        {
        if (handle->index[i].location == 0)
            {
            handle->index_num_entries = i;
            break;
            }
        }

    // determine the current frame counter
    handle->cur_frame = gsd_get_nframes(handle);

    // at this point, all valid index entries have been written to disk
    handle->index_written_entries = handle->index_num_entries;

    // printf("Returning handle %p\n", handle);
    return handle;
    }

/*! \param handle Handle to an open GSD file

    \pre \a handle was opened by gsd_open().
    \pre gsd_end_frame() has been called since the last call to gsd_write_chunk().

    \post The file is closed.
    \post \a handle is freed and can no longer be used.

    \warning Do not write chunks to the file with gsd_write_chunk() and then immediately close the file with gsd_close().
    This will result in data loss. Data chunks written by gsd_write_chunk() are not updated in the index until
    gsd_end_frame() is called. This is by design to prevent partial frames in files.

    \returns 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
    \ingroup c_api
*/
int gsd_close(gsd_handle_t* handle)
    {
    if (handle == NULL)
        return -2;

    // save the fd so we can use it after freeing the handle
    int fd = handle->fd;

    // zero and free memory allocated in the handle
    if (handle->index != NULL)
        {
        memset(handle->index, 0, sizeof(gsd_index_entry_t)*handle->header.index_allocated_entries);
        free(handle->index);
        handle->index = NULL;

        // only try and free the handle if handle->index is valid
        // this attempts to fail gracefully when calling gsd_close(handle) twice.
        memset(handle, 0, sizeof(gsd_handle_t));
        free(handle);
        }

    // close the file
    int retval = close(fd);
    if (retval != 0)
        return -1;

    return 0;
    }

/*! \param handle Handle to an open GSD file

    \pre \a handle was opened by gsd_open().
    \pre gsd_write_chunk() has been called at least once since the last call to gsd_end_frame().

    \post The current frame counter is increased by 1 and cached indexes are written to disk.

    \returns 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
    \ingroup c_api
*/
int gsd_end_frame(gsd_handle_t* handle)
    {
    if (handle == NULL)
        return -2;
    if (handle->open_flags == GSD_OPEN_READONLY)
        return -2;

    // all data chunks have already been written to the file and the index updated in memory. To end a frame, all we
    // need to do is increment the frame counter
    handle->cur_frame++;

    // and write unwritten index entries to the file (if there are any to write)
    uint64_t entries_to_write = handle->index_num_entries - handle->index_written_entries;
    if (entries_to_write > 0)
        {
        // write just those unwritten entries to the end of the index block
        lseek(handle->fd,
              handle->header.index_location + sizeof(gsd_index_entry_t)*handle->index_written_entries,
              SEEK_SET);

        size_t bytes_written = write(handle->fd,
                                     &(handle->index[handle->index_written_entries]),
                                     sizeof(gsd_index_entry_t)*entries_to_write);
        if (bytes_written != sizeof(gsd_index_entry_t) * entries_to_write)
            return -1;

        handle->index_written_entries += entries_to_write;
        }

    return 0;
    }

/*! \param handle Handle to an open GSD file
    \param name Name of the data chunk (truncated to 32 chars)
    \param type GSD_*_TYPE type ID that identifies the type of data in \a data
    \param N Number of rows in the data
    \param M Number of columns in the data
    \param step Current time step
    \param data Data buffer

    \pre \a handle was opened by gsd_open().
    \pre \a name is a unique name for data chunks in the given frame.
    \pre data is allocated and contains at least `N * M * gsd_sizeof_type(type)` bytes.

    \post The given data chunk is written to the end of the file and its location is updated in the in-memory index.

    \returns 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
    \ingroup c_api
*/
int gsd_write_chunk(gsd_handle_t* handle,
                     const char *name,
                     uint8_t type,
                     uint64_t N,
                     uint64_t M,
                     uint64_t step,
                     const void *data)
    {
    // validate input
    if (data == NULL)
        return -2;
    if (N == 0 || M == 0)
        return -2;
    if (handle->open_flags == GSD_OPEN_READONLY)
        return -2;

    // populate fields in the index_entry data
    gsd_index_entry_t index_entry;
    memset(&index_entry, 0, sizeof(index_entry));
    index_entry.frame = handle->cur_frame;
    strncpy(index_entry.name, name, sizeof(index_entry.name)-1);
    index_entry.name[sizeof(index_entry.name)-1] = 0;
    index_entry.type = type;
    index_entry.N = N;
    index_entry.M = M;
    size_t size = N * M * gsd_sizeof_type(type);
    index_entry.step = step;

    // find the location at the end of the file for the chunk
    index_entry.location = lseek(handle->fd, 0, SEEK_END);
    index_entry.checksum = type + N + M + step + index_entry.location;

    // write the data
    // printf("Writing %d bytes\n", size);
    size_t bytes_written = write(handle->fd, data, size);
    if (bytes_written != size)
        return -1;

    // update the file_size in the handle
    handle->file_size = index_entry.location + bytes_written;

    // update the index entry in the index
    // need to expand the index if it is already full
    if (handle->index_num_entries >= handle->header.index_allocated_entries)
        {
        int retval = __gsd_expand_index(handle);
        if (retval != 0)
            return 0;
        }

    // once we get here, there is a free slot to add this entry to the index
    handle->index[handle->index_num_entries] = index_entry;
    handle->index_num_entries++;

    return 0;
    }

/*! \param handle Handle to an open GSD file

    \pre \a handle was opened by gsd_open().

    \returns The step field of the last chunk written to the file, or 0 on error
    \ingroup c_api
*/
uint64_t gsd_get_last_step(gsd_handle_t* handle)
    {
    if (handle == NULL)
        return 0;

    size_t index_entry = handle->index_num_entries;
    if (index_entry == 0)
        return 0;

    return handle->index[index_entry-1].step;
    }

/*! \param handle Handle to an open GSD file

    \pre \a handle was opened by gsd_open().

    \returns The number of frames in the file, or 0 on error
    \ingroup c_api
*/
uint64_t gsd_get_nframes(gsd_handle_t* handle)
    {
    if (handle == NULL)
        return 0;

    size_t index_entry = handle->index_num_entries;
    if (index_entry == 0)
        return 0;

    return handle->index[index_entry-1].frame + 1;
    }


/*! \param handle Handle to an open GSD file
    \param frame Frame to look for chunk
    \param name Name of the chunk to find

    \pre \a handle was opened by gsd_open().

    \returns A pointer to the found chunk, or NULL if not found
    \ingroup c_api
*/
gsd_index_entry_t* gsd_find_chunk(gsd_handle_t* handle, uint64_t frame, const char *name)
    {
    if (handle == NULL)
        return NULL;
    if (name == NULL)
        return NULL;
    if (frame >= gsd_get_nframes(handle))
        return NULL;

    // binary search for the first index entry at the requested frame
    size_t L = 0;
    size_t R = handle->index_num_entries;

    // progressively narrow the search window by halves
    do
        {
        size_t m = (L+R)/2;

        if (frame < handle->index[m].frame)
            R = m;
        else
            L = m;
        } while ((R-L) > 1);

    // this finds L = the rightmost index with the desired frame
    size_t cur_index;

    // search all index entries with the matching frame
    for (cur_index = L; (cur_index >= 0) && (handle->index[cur_index].frame == frame); cur_index--)
        {
        // if the frame matches, check the name
        if (0 == strncmp(name, handle->index[cur_index].name, sizeof(handle->index[cur_index].name)))
            {
            return &(handle->index[cur_index]);
            }
        }

    // if we got here, we didn't find the specified chunk
    return NULL;
    }

/*! \param handle Handle to an open GSD file
    \param data Data buffer to read into
    \param chunk Chunk to read

    \pre \a handle was opened by gsd_open().
    \pre \a chunk was found by gsd_find_chunk().
    \pre \a data points to an allocated buffer with at least `N * M * gsd_sizeof_type(type)` bytes.

    \returns 0 on success, -1 on a file IO failure - see errno for details, and -2 on invalid input
    \ingroup c_api
*/
int gsd_read_chunk(gsd_handle_t* handle, void* data, const gsd_index_entry_t* chunk)
    {
    if (handle == NULL)
        return -2;
    if (data == NULL)
        return -2;
    if (chunk == NULL)
        return -2;

    size_t size = chunk->N * chunk->M * gsd_sizeof_type(chunk->type);
    if (size == 0)
        return -2;
    if (chunk->location == 0)
        return -2;

    // validate checksum
    if ((chunk->type + chunk->N + chunk->M + chunk->step + chunk->location) != chunk->checksum)
        {
        // checksum invalid, error out
        return -2;
        }
    // validate that we don't read past the end of the file
    if ((chunk->location + size) > handle->file_size)
        {
        // data chunk asks us to read pas the end of the file, error out
        return -2;
        }

    // printf("Reading %d bytes\n", chunk->size);
    lseek(handle->fd, chunk->location, SEEK_SET);
    size_t bytes_read = read(handle->fd, data, size);
    if (bytes_read != size)
        return -1;

    return 0;
    }

/*! \param type Type ID to query

    \returns Size of the given type, or 1 for an unknown type ID.
    \ingroup c_api
*/
size_t gsd_sizeof_type(uint8_t type)
    {
    if (type == GSD_UINT8_TYPE)
        return 1;
    else if (type == GSD_UINT32_TYPE)
        return 4;
    else if (type == GSD_FLOAT_TYPE)
        return 4;
    else if (type == GSD_DOUBLE_TYPE)
        return 8;
    else
        return 1;
    }
