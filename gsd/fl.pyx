""" GSD file layer API"""

from libc.stdint cimport uint8_t, int8_t, uint16_t, int16_t, uint32_t, int32_t, uint64_t, int64_t
from libc.errno cimport errno
cimport libgsd
cimport numpy
import os
import logging
import numpy

logger = logging.getLogger('gsd')

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
    """ GSD file access interface.

    GSDFile implements a python object oriented class interface to the GSD file
    layer. It can be used as a single use context manager::

        with GSDFile(filename, 'r') as f:
            f.do_something()

    Args:
        name (str): File name to open.
        mode (str): 'r' for read only access, 'w' for read-write access.

    Attributes:
        name (str): Name of the open file.
        mode (str): Mode of the open file.
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

        retval = libgsd.gsd_open(&self.__handle, name.encode('utf-8'), c_flags);

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
        """ Close the file.

        Once closed, any other operation on the file object will result in a
        `ValueError`. close() may be called more than once.
        """
        if self.__is_open:
            logger.info('closing file: ' + self.name);
            libgsd.gsd_close(&self.__handle);
            self.__is_open == False;

    def end_frame(self):
        """ Complete writing the current frame.

        end_frame() completes the current frame. After calling end_frame()
        future calls to write_chunk() will write to the next frame in the file.
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        logger.debug('end frame: ' + self.name);
        retval = libgsd.gsd_end_frame(&self.__handle)

        if retval == -1:
            raise IOError(*__format_errno(self.name));
        elif retval == -2:
            raise RuntimeError("GSD file is opened read only: " + self.name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

    def write_chunk(self, name, data):
        """ Writes a data chunk to the file.

        write_chunk() writes the provided data to a named chunk in the file.
        After writing all chunks in the current frame, call end_frame().

        Args:
            name (str): Name of the chunk
            data (numpy array): Data to write into the chunk. Must be a numpy
                                array, or array-like, with 2 or fewer
                                dimensions.
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

        logger.debug('write chunk: ' + self.name + ' / ' + name);

        cdef char * c_name;
        name_e = name.encode('utf-8')
        c_name = name_e;
        with nogil:
            retval = libgsd.gsd_write_chunk(&self.__handle,
                                           c_name,
                                           gsd_type,
                                           N,
                                           M,
                                           data_ptr);

        if retval == -1:
            raise IOError(*__format_errno(name));
        elif retval == -2:
            raise RuntimeError("GSD file is opened read only: " + self.name);

    def __enter__(self):
        return self;

    def __exit__(self):
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

    def __dealloc__(self):
        if self.__is_open:
            logger.info('closing file: ' + self.name);
            libgsd.gsd_close(&self.__handle);
            self.__is_open = False;

def create(name, application, schema, schema_version):
    """ Create a GSD file.

    create() creates an empty GSD file on disk.

    Args:
        name (str): File name to open.
        application (str): Name of the application creating the file.
        schema (str): Name of the data schema.
        schema_version (list[int]): Schema version number [major, minor].

    Warning:
        The file *name* is overwritten if it already exists.
    """

    _c_schema_version = libgsd.gsd_make_version(schema_version[0], schema_version[1])
    retval = libgsd.gsd_create(name.encode('utf-8'), application.encode('utf-8'), schema.encode('utf-8'), _c_schema_version);

    if retval == -1:
        raise IOError(*__format_errno(name));
    elif retval != 0:
        raise RuntimeError("Unknown error");
