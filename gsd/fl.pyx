# Copyright (c) 2016 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

""" GSD file layer API.

Low level access to gsd files. :py:mod:`gsd.fl` allows direct access to create,
read, and write ``gsd`` files.

* :py:func:`create` - Create a gsd file.
* :py:class:`GSDFile` - Read and write gsd files.
"""

from libc.stdint cimport uint8_t, int8_t, uint16_t, int16_t, uint32_t, int32_t, uint64_t, int64_t
from libc.errno cimport errno
cimport libgsd
cimport numpy
import os
import logging
import numpy

logger = logging.getLogger('gsd.fl')

########################
### Helper functions ###

cdef __format_errno(fname):
    """ Return a tuple for constructing an IOError """
    return (errno, os.strerror(errno), fname);

# Getter methods for 2D numpy arrays of all supported types
# cython needs strongly typed numpy arrays to get a void *
# to the data, so we implement each by hand here and dispacth
# from the read and write routines
cdef void * __get_ptr_uint8(data):
    cdef numpy.ndarray[uint8_t, ndim=2, mode="c"] data_array_uint8;
    data_array_uint8 = data;
    return <void*>&data_array_uint8[0,0];

cdef void * __get_ptr_uint16(data):
    cdef numpy.ndarray[uint16_t, ndim=2, mode="c"] data_array_uint16;
    data_array_uint16 = data;
    return <void*>&data_array_uint16[0,0];

cdef void * __get_ptr_uint32(data):
    cdef numpy.ndarray[uint32_t, ndim=2, mode="c"] data_array_uint32;
    data_array_uint32 = data;
    return <void*>&data_array_uint32[0,0];

cdef void * __get_ptr_uint64(data):
    cdef numpy.ndarray[uint64_t, ndim=2, mode="c"] data_array_uint64;
    data_array_uint64 = data;
    return <void*>&data_array_uint64[0,0];

cdef void * __get_ptr_int8(data):
    cdef numpy.ndarray[int8_t, ndim=2, mode="c"] data_array_int8;
    data_array_int8 = data;
    return <void*>&data_array_int8[0,0];

cdef void * __get_ptr_int16(data):
    cdef numpy.ndarray[int16_t, ndim=2, mode="c"] data_array_int16;
    data_array_int16 = data;
    return <void*>&data_array_int16[0,0];

cdef void * __get_ptr_int32(data):
    cdef numpy.ndarray[int32_t, ndim=2, mode="c"] data_array_int32;
    data_array_int32 = data;
    return <void*>&data_array_int32[0,0];

cdef void * __get_ptr_int64(data):
    cdef numpy.ndarray[int64_t, ndim=2, mode="c"] data_array_int64;
    data_array_int64 = data;
    return <void*>&data_array_int64[0,0];

cdef void * __get_ptr_float32(data):
    cdef numpy.ndarray[float, ndim=2, mode="c"] data_array_float32;
    data_array_float32 = data;
    return <void*>&data_array_float32[0,0];

cdef void * __get_ptr_float64(data):
    cdef numpy.ndarray[double, ndim=2, mode="c"] data_array_float64;
    data_array_float64 = data;
    return <void*>&data_array_float64[0,0];

cdef class GSDFile:
    """ GSDFile(name, mode)

    GSD file access interface.

    Args:

        name (str): File name to open.
        mode (str): 'r' for read only access, 'w' for read-write access.

    GSDFile implements an object oriented class interface to the GSD file
    layer. Use it to open an existing file in a **read-only** or
    **read-write** mode.

    Examples:

        Open a file in **read-only** mode::

            f = GSDFile(name=filename, mode='r');
            if f.chunk_exists(frame=0, name='chunk'):
                data = f.read_chunk(frame=0, name='chunk');

        Access file **metadata**::

            f = GSDFile(name=filename, mode='r');
            print(f.name, f.mode, f.file_size, f.gsd_version);
            print(f.application, f.schema, f.schema_version);
            print(f.nframes);

        Open a file in **read-write** mode::

            f = GSDFile(name=filename, mode='w');
            f.write_chunk(name='chunk', data=data_write);
            f.end_frame()
            data_read = f.read_chunk(frame=0, name='chunk');

        Use as a **context manager**::

            with GSDFile(filename, 'r') as f:
                data = f.read_chunk(frame=0, name='chunk');

    Attributes:

        name (str): Name of the open file **(read only)**.
        mode (str): Mode of the open file **(read only)**.
        gsd_version (tuple[int]): GSD file layer version number [major, minor] **(read only)**.
        application (str): Name of the generating application **(read only)**.
        schema (str): Name of the data schema **(read only)**.
        schema_version (tuple[int]): Schema version number [major, minor] **(read only)**.
        file_size (int): File size in bytes **(read only)**.
        nframes (int): Number of frames **(read only)**.
    """

    cdef libgsd.gsd_handle __handle;
    cdef bint __is_open;
    cdef str mode;
    cdef str name;

    def __init__(self, name, mode):
        cdef libgsd.gsd_open_flag c_flags;
        if mode == 'w':
            c_flags = libgsd.GSD_OPEN_READWRITE;
        elif mode == 'r':
            c_flags = libgsd.GSD_OPEN_READONLY;
        else:
            raise ValueError("mode must be 'r' or 'w'");
        self.name = name;
        self.mode = mode;

        logger.info('opening file: ' + name + ' with mode: ' + mode);
        cdef char * c_name;
        name_e = name.encode('utf-8')
        c_name = name_e;

        with nogil:
            retval = libgsd.gsd_open(&self.__handle, c_name, c_flags);

        if retval == -1:
            raise IOError(*__format_errno(name));
        elif retval == -2:
            raise RuntimeError("Not a GSD file: " + name);
        elif retval == -3:
            raise RuntimeError("Unsupported GSD file version: " + name);
        elif retval == -4:
            raise RuntimeError("Corrupt GSD file: " + name);
        elif retval == -5:
            raise MemoryError("Unable to allocate GSD index: " + name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

        self.__is_open = True;

    def close(self):
        """ close()

        Close the file.

        Once closed, any other operation on the file object will result in a
        `ValueError`. :py:meth:`close()` may be called more than once.
        The file is automatically closed when garbage collected or when
        the context manager exists.
        """
        if self.__is_open:
            logger.info('closing file: ' + self.name);
            with nogil:
                libgsd.gsd_close(&self.__handle);
            self.__is_open = False;

    def truncate(self):
        """ truncate()

        Truncate all data from the file. After truncation, the file has no
        frames and no data chunks. The application, schema, and schema version
        remain the same.
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        logger.info('truncating file: ' + self.name);
        with nogil:
            retval = libgsd.gsd_truncate(&self.__handle);

        if retval == -1:
            raise IOError(*__format_errno(self.name));
        elif retval == -2:
            raise RuntimeError("Not a GSD file: " + self.name);
        elif retval == -3:
            raise RuntimeError("Unsupported GSD file version: " + self.name);
        elif retval == -4:
            raise RuntimeError("Corrupt GSD file: " + self.name);
        elif retval == -5:
            raise MemoryError("Unable to allocate GSD index: " + self.name);
        elif retval != 0:
            raise RuntimeError("Unknown error");


    def end_frame(self):
        """ end_frame()

        Complete writing the current frame. After calling :py:meth:`end_frame()`
        future calls to :py:meth:`write_chunk()` will write to the **next** frame
        in the file.

        Example:

            Write several frames to the file::

                with GSDFile(name=filename, mode='w') as f:
                    f.write_chunk(name='chunk', data=data);
                    f.end_frame()
                    f.write_chunk(name='chunk', data=data);
                    f.end_frame()
                    f.write_chunk(name='chunk', data=data);
                    f.end_frame()

                with GSDFile(name=filename, mode='r') as f:
                    f.chunk_exists(frame=0, name='chunk');  # True
                    f.chunk_exists(frame=1, name='chunk');  # True
                    f.chunk_exists(frame=2, name='chunk');  # True
                    f.chunk_exists(frame=3, name='chunk');  # False (wrote only 3 frames)

        .. danger::
            Call :py:meth:`end_frame()` to complete the current frame
            **before** closing the file. If you fail to call
            :py:meth:`end_frame()`, the last frame may not be written
            to disk.
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        logger.debug('end frame: ' + self.name);

        with nogil:
            retval = libgsd.gsd_end_frame(&self.__handle)

        if retval == -1:
            raise IOError(*__format_errno(self.name));
        elif retval == -2:
            raise RuntimeError("GSD file is opened read only: " + self.name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

    def write_chunk(self, name, data):
        """ write_chunk(name, data)

        Write a data chunk to the file. After writing all chunks in the
        current frame, call :py:meth:`end_frame()`.

        Args:
            name (str): Name of the chunk
            data (numpy array): Data to write into the chunk. Must be a numpy
                                array, or array-like, with 2 or fewer
                                dimensions.

        Examples:

            Write 1D arrays::

                data = numpy.array([1,2,3,4], dtype=numpy.float32);
                with GSDFile(name=filename, mode='w') as f:
                    f.write_chunk(name='chunk1d', data);

            Write 2D arrays::

                data = numpy.array([[1,2],[2,3],[3,4]], dtype=numpy.float32);
                with GSDFile(name=filename, mode='w') as f:
                    f.write_chunk(name='chunk2d', data);

            Write several chunks to each frame::

                with GSDFile(name=filename, mode='w') as f:
                    f.write_chunk(name='chunk1', data=[1,2,3,4]);
                    f.write_chunk(name='chunk2', data=[5,6,7,8]);
                    f.end_frame()
                    f.write_chunk(name='chunk1', data=[10,20]);
                    f.write_chunk(name='chunk2', data=[30,40]);
                    f.end_frame()

        Warning:
            :py:meth:`write_chunk()` will implicitly converts array-like and
            non-contiguous numpy arrays to contiguous numpy arrays with
            ``numpy.ascontiguousarray(data)``. This may or may not produce
            desired data types in the output file and incurs overhead.
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        data_array = numpy.ascontiguousarray(data);
        if data_array is not data:
            logger.warning('implicit data copy when writing chunk: ' + name);
        data_array = data_array.view();

        cdef uint64_t N;
        cdef uint8_t M;

        if len(data_array.shape) > 2:
            raise ValueError("GSD can only write 1 or 2 dimensional arrays: " + name);

        if len(data_array.shape) == 1:
            data_array = data_array.reshape([data_array.shape[0], 1]);

        if data_array.shape[1] > 255:
            raise ValueError("Dimension 2 is greater than 255 in chunk: " + name);
        N = data_array.shape[0];
        M = data_array.shape[1];

        cdef libgsd.gsd_type gsd_type;
        cdef void *data_ptr;
        if data_array.dtype == numpy.uint8:
            gsd_type = libgsd.GSD_TYPE_UINT8;
            data_ptr = __get_ptr_uint8(data_array)
        elif data_array.dtype == numpy.uint16:
            gsd_type = libgsd.GSD_TYPE_UINT16;
            data_ptr = __get_ptr_uint16(data_array)
        elif data_array.dtype == numpy.uint32:
            gsd_type = libgsd.GSD_TYPE_UINT32;
            data_ptr = __get_ptr_uint32(data_array)
        elif data_array.dtype == numpy.uint64:
            gsd_type = libgsd.GSD_TYPE_UINT64;
            data_ptr = __get_ptr_uint64(data_array)
        elif data_array.dtype == numpy.int8:
            gsd_type = libgsd.GSD_TYPE_INT8;
            data_ptr = __get_ptr_int8(data_array)
        elif data_array.dtype == numpy.int16:
            gsd_type = libgsd.GSD_TYPE_INT16;
            data_ptr = __get_ptr_int16(data_array)
        elif data_array.dtype == numpy.int32:
            gsd_type = libgsd.GSD_TYPE_INT32;
            data_ptr = __get_ptr_int32(data_array)
        elif data_array.dtype == numpy.int64:
            gsd_type = libgsd.GSD_TYPE_INT64;
            data_ptr = __get_ptr_int64(data_array)
        elif data_array.dtype == numpy.float32:
            gsd_type = libgsd.GSD_TYPE_FLOAT;
            data_ptr = __get_ptr_float32(data_array)
        elif data_array.dtype == numpy.float64:
            gsd_type = libgsd.GSD_TYPE_DOUBLE;
            data_ptr = __get_ptr_float64(data_array)
        else:
            raise ValueError("invalid type for chunk: " + name);

        logger.debug('write chunk: ' + self.name + ' - ' + name);

        cdef char * c_name;
        name_e = name.encode('utf-8')
        c_name = name_e;
        with nogil:
            retval = libgsd.gsd_write_chunk(&self.__handle,
                                           c_name,
                                           gsd_type,
                                           N,
                                           M,
                                           0,
                                           data_ptr);

        if retval == -1:
            raise IOError(*__format_errno(name));
        elif retval == -2:
            raise RuntimeError("GSD file is opened read only: " + self.name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

    def chunk_exists(self, frame, name):
        """ chunk_exists(frame, name)

        Test if a chunk exists.

        Args:
            frame (int): Index of the frame to check
            name (str): Name of the chunk

        Returns:
            bool: True if the chunk exists in the file. False if it does not.

        Example:

            Handle non-existent chunks::

                with GSDFile(name=filename, mode='r') as f:
                    if f.chunk_exists(frame=0, name='chunk'):
                        return f.read_chunk(frame=0, name='chunk');
                    else:
                        return None;
        """

        cdef const libgsd.gsd_index_entry* index_entry;
        cdef char * c_name;
        name_e = name.encode('utf-8')
        c_name = name_e;
        cdef int64_t c_frame;
        c_frame = frame;

        logger.debug('chunk exists: ' + self.name + ' - ' + name);

        with nogil:
            index_entry = libgsd.gsd_find_chunk(&self.__handle, c_frame, c_name)

        return index_entry != NULL;

    def read_chunk(self, frame, name):
        """ read_chunk(frame, name)

        Read a data chunk from the file and return it as a numpy array.

        Args:
            frame (int): Index of the frame to read
            name (str): Name of the chunk

        Returns:
            numpy.ndarray[type, ndim=?, mode='c']: Data read from file.
            ``type`` is determined by the chunk metadata. If the data is
            NxM in the file and M > 1, return a 2D array. If the data is
            Nx1, return a 1D array.

        Examples:

            Read a 1D array::

                with GSDFile(name=filename, mode='r') as f:
                    data = f.read_chunk(frame=0, name='chunk1d');
                    # data.shape == [N]

            Read a 2D array::

                with GSDFile(name=filename, mode='r') as f:
                    data = f.read_chunk(frame=0, name='chunk2d');
                    # data.shape == [N,M]

            Read multiple frames::

                with GSDFile(name=filename, mode='r') as f:
                    data0 = f.read_chunk(frame=0, name='chunk');
                    data1 = f.read_chunk(frame=1, name='chunk');
                    data2 = f.read_chunk(frame=2, name='chunk');
                    data3 = f.read_chunk(frame=3, name='chunk');

        .. tip::
            Each call to invokes a disk read and allocation of a
            new numpy array for storage. To avoid overhead, don't call
            :py:meth:`read_chunk()` on the same chunk repeatedly. Cache the
            arrays instead.
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        cdef const libgsd.gsd_index_entry* index_entry;
        cdef char * c_name;
        name_e = name.encode('utf-8')
        c_name = name_e;
        cdef int64_t c_frame;
        c_frame = frame;

        with nogil:
            index_entry = libgsd.gsd_find_chunk(&self.__handle, c_frame, c_name)

        if index_entry == NULL:
            raise KeyError("frame " + str(frame) + " / chunk " + name + " not found in: " + self.name);

        cdef libgsd.gsd_type gsd_type;
        gsd_type = <libgsd.gsd_type>index_entry.type;

        cdef void *data_ptr;
        if gsd_type == libgsd.GSD_TYPE_UINT8:
            data_array = numpy.empty(dtype=numpy.uint8, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_uint8(data_array)
        elif gsd_type == libgsd.GSD_TYPE_UINT16:
            data_array = numpy.empty(dtype=numpy.uint16, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_uint16(data_array)
        elif gsd_type == libgsd.GSD_TYPE_UINT32:
            data_array = numpy.empty(dtype=numpy.uint32, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_uint32(data_array)
        elif gsd_type == libgsd.GSD_TYPE_UINT64:
            data_array = numpy.empty(dtype=numpy.uint64, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_uint64(data_array)
        elif gsd_type == libgsd.GSD_TYPE_INT8:
            data_array = numpy.empty(dtype=numpy.int8, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_int8(data_array)
        elif gsd_type == libgsd.GSD_TYPE_INT16:
            data_array = numpy.empty(dtype=numpy.int16, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_int16(data_array)
        elif gsd_type == libgsd.GSD_TYPE_INT32:
            data_array = numpy.empty(dtype=numpy.int32, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_int32(data_array)
        elif gsd_type == libgsd.GSD_TYPE_INT64:
            data_array = numpy.empty(dtype=numpy.int64, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_int64(data_array)
        elif gsd_type == libgsd.GSD_TYPE_FLOAT:
            data_array = numpy.empty(dtype=numpy.float32, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_float32(data_array)
        elif gsd_type == libgsd.GSD_TYPE_DOUBLE:
            data_array = numpy.empty(dtype=numpy.float64, shape=[index_entry.N, index_entry.M])
            data_ptr = __get_ptr_float64(data_array)
        else:
            raise ValueError("invalid type for chunk: " + name);

        logger.debug('read chunk: ' + self.name + ' - ' + str(frame) + ' - ' + name);

        with nogil:
            retval = libgsd.gsd_read_chunk(&self.__handle,
                                           data_ptr,
                                           index_entry);

        if retval == -1:
            raise IOError(*__format_errno(name));
        elif retval == -2:
            raise RuntimeError("Programming error: " + self.name);
        elif retval == -3:
            raise RuntimeError("Corrupt chunk: " + str(frame) + " / " + name + " in file" + self.name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

        if index_entry.M == 1:
            return data_array.reshape([index_entry.N]);
        else:
            return data_array;

    def __enter__(self):
        return self;

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    property name:
        def __get__(self):
            return self.name;

    property mode:
        def __get__(self):
            return self.mode;

    property gsd_version:
        def __get__(self):
            cdef uint32_t v = self.__handle.header.gsd_version;
            return (v >> 16, v & 0xffff);

    property schema_version:
        def __get__(self):
            cdef uint32_t v = self.__handle.header.schema_version;
            return (v >> 16, v & 0xffff);

    property schema:
        def __get__(self):
            return self.__handle.header.schema.decode('utf-8');

    property application:
        def __get__(self):
            return self.__handle.header.application.decode('utf-8');

    property file_size:
        def __get__(self):
            return self.__handle.file_size;

    property nframes:
        def __get__(self):
            if not self.__is_open:
                raise ValueError("File is not open");

            return libgsd.gsd_get_nframes(&self.__handle);

    def __dealloc__(self):
        if self.__is_open:
            logger.info('closing file: ' + self.name);
            libgsd.gsd_close(&self.__handle);
            self.__is_open = False;

def create(name, application, schema, schema_version):
    """ create(name, application, schema, schema_version)

    Create an empty GSD file on the filesystem. To write to the file, open it
    with :py:class:`GSDFile` after creating it.

    Args:
        name (str): File name to open.
        application (str): Name of the application creating the file.
        schema (str): Name of the data schema.
        schema_version (list[int]): Schema version number [major, minor].

    Example:

        Create a gsd file::

            create(name="file.gsd",
                   application="My application",
                   schema="My Schema",
                   schema_version=[1,0]);

            with GSDFile(filename="file.gsd", mode='r') as f:
                f.write_chunk(...);

    .. danger::
        The file is overwritten if it already exists.
    """

    _c_schema_version = libgsd.gsd_make_version(schema_version[0], schema_version[1])
    retval = libgsd.gsd_create(name.encode('utf-8'), application.encode('utf-8'), schema.encode('utf-8'), _c_schema_version);

    if retval == -1:
        raise IOError(*__format_errno(name));
    elif retval != 0:
        raise RuntimeError("Unknown error");
