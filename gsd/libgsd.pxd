# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

from libc.stdint cimport uint8_t, int8_t, uint16_t, int16_t, uint32_t, int32_t, uint64_t, int64_t

cdef extern from "gsd.h" nogil:
    cdef enum gsd_type:
        GSD_TYPE_UINT8=1
        GSD_TYPE_UINT16
        GSD_TYPE_UINT32
        GSD_TYPE_UINT64
        GSD_TYPE_INT8
        GSD_TYPE_INT16
        GSD_TYPE_INT32
        GSD_TYPE_INT64
        GSD_TYPE_FLOAT
        GSD_TYPE_DOUBLE

    cdef enum gsd_open_flag:
        GSD_OPEN_READWRITE=1
        GSD_OPEN_READONLY
        GSD_OPEN_APPEND

    cdef struct gsd_header:
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

    cdef struct gsd_index_entry:
        uint64_t frame;
        uint64_t N;
        int64_t location;
        uint32_t M;
        uint16_t id;
        uint8_t type;
        uint8_t flags;

    cdef struct gsd_namelist_entry:
        char name[64];

    cdef struct gsd_handle:
        int fd;
        gsd_header header;
        void *mapped_data;
        size_t append_index_size;
        gsd_index_entry *index;
        gsd_namelist_entry *namelist;
        uint64_t namelist_num_entries;
        uint64_t index_written_entries;
        uint64_t index_num_entries;
        uint64_t cur_frame;
        int64_t file_size;
        gsd_open_flag open_flags;

    uint32_t gsd_make_version(unsigned int major, unsigned int minor);
    int gsd_create(const char *fname, const char *application, const char *schema, uint32_t schema_version);
    int gsd_create_and_open(gsd_handle* handle,
                            const char *fname,
                            const char *application,
                            const char *schema,
                            uint32_t schema_version,
                            const gsd_open_flag flags,
                            int exclusive_create)
    int gsd_open(gsd_handle* handle, const char *fname, const gsd_open_flag flags);
    int gsd_truncate(gsd_handle* handle);
    int gsd_close(gsd_handle* handle);
    int gsd_end_frame(gsd_handle* handle);
    int gsd_write_chunk(gsd_handle* handle,
                    const char *name,
                    gsd_type type,
                    uint64_t N,
                    uint8_t M,
                    uint8_t flags,
                    const void *data);
    const gsd_index_entry* gsd_find_chunk(gsd_handle* handle, uint64_t frame, const char *name);
    int gsd_read_chunk(gsd_handle* handle, void* data, const gsd_index_entry* chunk);
    uint64_t gsd_get_nframes(gsd_handle* handle);
    size_t gsd_sizeof_type(gsd_type type);
