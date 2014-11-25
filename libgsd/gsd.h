/*
General Simulation Data (GSD)
Copyright (c) 2014, The Regents of the University of Michigan
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef __GSD_H__
#define __GSD_H__

#include <stdint.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

/*! \file gsd.h
    \brief Declare GSD data types and C API
*/

/*! \defgroup c_api C API
*/

//! GSD file header
/*! Defines the file header for GSD files.

    \warning All members are **read-only** to the caller. Only GSD API calls may modify members.

    \note Some fields are for internal use and are not shown in this documentation. See \ref design for full specifications.

    \ingroup c_api
*/
typedef struct gsd_header_t
    {
    uint32_t magic;
    char application[64];               //!< Name of generating application
    uint32_t version;                   //!< File format version: 0xaabbcc => aa.bb.cc
    char schema[64];                    //!< Name of schema defining stored data
    uint32_t schema_version;            //!< Schema version: 0xaabbcc => aa.bb.cc
    uint64_t index_location;
    uint64_t index_allocated_entries;
    uint64_t index_num_entries;
    char reserved[56];
    uint32_t check;
    } gsd_header_t;

//! Index entry
/*! Defines an index entry for a single data chunk.

    \warning All members are **read-only** to the caller. Only GSD API calls may modify members.

    \note Some fields are for internal use and are not shown in this documentation. See \ref design for full specifications.

    \ingroup c_api
*/
typedef struct gsd_index_entry_t
    {
    uint64_t frame;     //!< Frame index of the chunk

    char name[33];      //!< Name of the chunk
    uint8_t type;       //!< Data type of the chunk
    uint64_t N;         //!< Number of rows in the chunk
    uint64_t M;         //!< Number of columns in the chunk
    uint64_t step;      //!< Timestep the chunk was saved at

    int64_t location;
    uint64_t checksum;
    } gsd_index_entry_t;

//! File handle
/*! Defines a handle to an open GSD file.

    \warning All members are **read-only** to the caller. Only GSD API calls may modify members.

    \note Some fields are for internal use and are not shown in this documentation. See \ref design for full specifications.

    \ingroup c_api
*/
typedef struct gsd_handle_t
    {
    int fd;
    gsd_header_t header;                //!< GSD file header
    gsd_index_entry_t *index;
    uint64_t index_written_entries;
    uint64_t cur_frame;
    int64_t file_size;                  //!< File size (in bytes)
    uint8_t open_flags;                 //!< Flags passed to gsd_open()
    } gsd_handle_t;

// TODO: convert these to enums (need to wait for the cython wrap)

//! ID for uint8_t type
/*! \ingroup c_api
*/
const uint8_t GSD_UINT8_TYPE=1;
//! ID for uint32_t type
/*! \ingroup c_api
*/
const uint8_t GSD_UINT32_TYPE=2;
//! ID for float type
/*! \ingroup c_api
*/
const uint8_t GSD_FLOAT_TYPE=3;
//! ID for double type
/*! \ingroup c_api
*/
const uint8_t GSD_DOUBLE_TYPE=4;

//! Flag for read/write open
/*! \ingroup c_api
*/
const uint8_t GSD_OPEN_READWRITE=1;

//! Flag for read only open
/*! \ingroup c_api
*/
const uint8_t GSD_OPEN_READONLY=2;

//! Create a GSD file
int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version);

//! Open a GSD file for read/write
gsd_handle_t* gsd_open(const char *fname, const uint8_t flags);

//! Close a GSD file
int gsd_close(gsd_handle_t* handle);

//! Move on to the next frame
int gsd_end_frame(gsd_handle_t* handle);

//! Write a data chunk to the current frame
int gsd_write_chunk(gsd_handle_t* handle,
                     const char *name,
                     uint8_t type,
                     uint64_t N,
                     uint64_t M,
                     uint64_t step,
                     const void *data);

//! Find a chunk in the GSD file
gsd_index_entry_t* gsd_find_chunk(gsd_handle_t* handle, uint64_t frame, const char *name);

//! Read a chunk from the GSD file
int gsd_read_chunk(gsd_handle_t* handle, void* data, const gsd_index_entry_t* chunk);

//! Query the last time step in the GSD file
uint64_t gsd_get_last_step(gsd_handle_t* handle);

//! Get the number of frames in the GSD file
uint64_t gsd_get_nframes(gsd_handle_t* handle);

//! Query size of a GSD type ID
size_t gsd_sizeof_type(uint8_t type);

#ifdef __cplusplus
}
#endif

#endif

