# Copyright (c) 2016-2017 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

""" GSD file layer API.

Low level access to gsd files. :py:mod:`gsd.fl` allows direct access to create,
read, and write ``gsd`` files. The module is implemented in C and is optimized.
See :ref:`fl-examples` for detailed example code.

* :py:class:`GSDFile` - Class interface to read and write gsd files.
* :py:func:`create` - Create a gsd file (deprecated).
* :py:func:`open` - Open a gsd file.

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

def open(name, mode, application, schema, schema_version):
    """ open(name, mode, application, schema, schema_version)

    :py:func:`open` opens a GSD file and returns a :py:class:`GSDFile` instance.
    The return value of :py:func:`open` can be used as a context manager.

    Args:
        name (str): File name to open.
        mode (str): File access mode.
        application (str): Name of the application creating the file.
        schema (str): Name of the data schema.
        schema_version (``list[int]``): Schema version number [major, minor].

    Valid values for mode:

    +------------------+---------------------------------------------+
    | mode             | description                                 |
    +==================+=============================================+
    | ``'rb'``         | Open an existing file for reading.          |
    +------------------+---------------------------------------------+
    | ``'rb+'``        | Open an existing file for reading and       |
    |                  | writing. *Inefficient for large files.*     |
    +------------------+---------------------------------------------+
    | ``'wb'``         | Open a file for writing. Creates the file   |
    |                  | if needed, or overwrites an existing file.  |
    +------------------+---------------------------------------------+
    | ``'wb+'``        | Open a file for reading and writing.        |
    |                  | Creates the file if needed, or overwrites   |
    |                  | an existing file. *Inefficient for large    |
    |                  | files.*                                     |
    +------------------+---------------------------------------------+
    | ``'xb'``         | Create a gsd file exclusively and opens it  |
    |                  | for writing.                                |
    |                  | Raise an :py:exc:`FileExistsError`          |
    |                  | exception if it already exists.             |
    +------------------+---------------------------------------------+
    | ``'xb+'``        | Create a gsd file exclusively and opens it  |
    |                  | for reading and writing.                    |
    |                  | Raise an :py:exc:`FileExistsError`          |
    |                  | exception if it already exists.             |
    |                  | *Inefficient for large files.*              |
    +------------------+---------------------------------------------+
    | ``'ab'``         | Open an existing file for writing.          |
    |                  | Does *not* create or overwrite existing     |
    |                  | files.                                      |
    +------------------+---------------------------------------------+

    The '+' read/write modes are inefficient at handling large files, as they read the entire
    file index into memory. Prefer the appropriate read or write only modes.

    When opening a file for reading (``'r' or 'a'`` modes): ``application`` and ``schema_version`` are ignored.
    :py:func:`open` throws an exception if the file's schema does not match ``schema``.

    When opening a file for writing (``'w' or 'x'`` modes): The given ``application``, ``schema``, and
    ``schema_version`` are saved in the file.

    .. versionadded:: 1.2

    Example:

        .. ipython:: python

            with gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
                f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
                f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32));
                f.end_frame();
                f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
                f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32));
                f.end_frame();

            f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
            if f.chunk_exists(frame=0, name='chunk1'):
                data = f.read_chunk(frame=0, name='chunk1')
            data
    """

    return GSDFile(name, mode, application, schema, schema_version);

cdef class GSDFile:
    """ GSDFile(name, mode, application, schema, schema_version)

    GSD file access interface.

    GSDFile implements an object oriented class interface to the GSD file
    layer. Use :py:func:`open` to open a GSD file and obtain a GSDFile instance.
    :py:class:`GSDFile` can be used as a context manager.

    .. versionchanged:: 1.2

        For new code, use :py:func:`open` instead of constructing GSDFile directly.
        GSDFile.__init__ is backwards compatible with the old open syntax used in GSD versions 1.0.x and 1.1.x.

    Attributes:

        name (str): Name of the open file **(read only)**.
        mode (str): Mode of the open file **(read only)**.
        gsd_version (tuple[int]): GSD file layer version number [major, minor] **(read only)**.
        application (str): Name of the generating application **(read only)**.
        schema (str): Name of the data schema **(read only)**.
        schema_version (tuple[int]): Schema version number [major, minor] **(read only)**.
        nframes (int): Number of frames **(read only)**.
    """

    cdef libgsd.gsd_handle __handle;
    cdef bint __is_open;
    cdef str mode;
    cdef str name;

    def __init__(self, name, mode, application=None, schema=None, schema_version=None):
        cdef libgsd.gsd_open_flag c_flags;
        cdef int exclusive_create = 0;
        cdef int overwrite = 0;

        new_api = (application is not None and schema is not None and schema_version is not None);

        if new_api:
            if mode == 'wb':
                c_flags = libgsd.GSD_OPEN_APPEND;
                overwrite = 1;
            elif mode == 'wb+':
                c_flags = libgsd.GSD_OPEN_READWRITE;
                overwrite = 1;
            elif mode == 'rb':
                c_flags = libgsd.GSD_OPEN_READONLY;
            elif mode == 'rb+':
                c_flags = libgsd.GSD_OPEN_READWRITE;
            elif mode == 'xb':
                c_flags = libgsd.GSD_OPEN_APPEND;
                overwrite = 1;
                exclusive_create = 1;
            elif mode == 'xb+':
                c_flags = libgsd.GSD_OPEN_READWRITE;
                overwrite = 1;
                exclusive_create = 1;
            elif mode == 'ab':
                c_flags = libgsd.GSD_OPEN_APPEND;
            else:
                raise ValueError("mode must be 'wb', 'wb+', 'rb', 'rb+', 'xb', 'xb+', or 'ab'");
        else:
            # backwards compatible old API
            if mode == 'wb':
                c_flags = libgsd.GSD_OPEN_READWRITE;
            elif mode == 'rb':
                c_flags = libgsd.GSD_OPEN_READONLY;
            elif mode == 'ab':
                c_flags = libgsd.GSD_OPEN_APPEND;
            else:
                raise ValueError("mode must be 'rb', 'wb', or 'ab'");

        self.name = name;
        self.mode = mode;

        cdef char * c_name;
        cdef char * c_application;
        cdef char * c_schema;
        cdef int _c_schema_version;

        if overwrite:
            # create a new file or overwrite an existing one
            logger.info('opening file: ' + name + ' with mode: ' + mode + ', application: ' + application
                         + ', schema: ' + schema + ', and schema_version: ' + str(schema_version));
            name_e = name.encode('utf-8')
            c_name = name_e;

            application_e = application.encode('utf-8')
            c_application = application_e;

            schema_e = schema.encode('utf-8')
            c_schema = schema_e;

            _c_schema_version = libgsd.gsd_make_version(schema_version[0], schema_version[1])

            with nogil:
                retval = libgsd.gsd_create_and_open(&self.__handle,
                                                    c_name,
                                                    c_application,
                                                    c_schema,
                                                    _c_schema_version,
                                                    c_flags,
                                                    exclusive_create);
        else:
            # open an existing file
            logger.info('opening file: ' + name + ' with mode: ' + mode);
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
        elif retval == -6:
            raise MemoryError("Invalid gsd argument: " + name);
        elif retval != 0:
            raise RuntimeError("Unknown error");

        # validate schema
        if new_api:
            if self.schema != schema:
                raise RuntimeError('file ' + name + ' has incorrect schema: ' + schema);

        self.__is_open = True;

    def close(self):
        """ close()

        Close the file.

        Once closed, any other operation on the file object will result in a
        `ValueError`. :py:meth:`close()` may be called more than once.
        The file is automatically closed when garbage collected or when
        the context manager exits.

        Example:
            .. ipython:: python

                f = gsd.fl.open(name='file.gsd', mode='wb+', application="My application", schema="My Schema", schema_version=[1,0])
                f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32))
                f.end_frame();
                data = f.read_chunk(frame=0, name='chunk1')

                f.close()
                # Read fails because the file is closed
                @okexcept
                data = f.read_chunk(frame=0, name='chunk1')

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

        Example:
            .. ipython:: python

                with gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
                    for i in range(10):
                        f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32))
                        f.end_frame();

                f = gsd.fl.open(name='file.gsd', mode='ab', application="My application", schema="My Schema", schema_version=[1,0])
                f.nframes
                f.schema, f.schema_version, f.application
                f.truncate()
                f.nframes
                f.schema, f.schema_version, f.application
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

        .. danger::
            Call :py:meth:`end_frame()` to complete the current frame
            **before** closing the file. If you fail to call
            :py:meth:`end_frame()`, the last frame may not be written
            to disk.

        Example:
            .. ipython:: python

                f = gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0])

                f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
                f.end_frame();
                f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
                f.end_frame();
                f.write_chunk(name='chunk1', data=numpy.array([13,14], dtype=numpy.float32));
                f.end_frame();
                f.nframes

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
            data: Data to write into the chunk. Must be a numpy
                  array, or array-like, with 2 or fewer
                  dimensions.

        Warning:
            :py:meth:`write_chunk()` will implicitly converts array-like and
            non-contiguous numpy arrays to contiguous numpy arrays with
            ``numpy.ascontiguousarray(data)``. This may or may not produce
            desired data types in the output file and incurs overhead.

        Example:
            .. ipython:: python

                f = gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0])

                f.write_chunk(name='float1d', data=numpy.array([1,2,3,4], dtype=numpy.float32));
                f.write_chunk(name='float2d', data=numpy.array([[13,14],[15,16],[17,19]], dtype=numpy.float32));
                f.write_chunk(name='double2d', data=numpy.array([[1,4],[5,6],[7,9]], dtype=numpy.float64));
                f.write_chunk(name='int1d', data=numpy.array([70,80,90], dtype=numpy.int64));
                f.end_frame();
                f.nframes
                f.close()
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
            .. ipython:: python

                with gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
                    f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
                    f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32));
                    f.end_frame();
                    f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
                    f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32));
                    f.end_frame();

                f = gsd.fl.open(name='file.gsd', mode='rb', application="My application", schema="My Schema", schema_version=[1,0])

                f.chunk_exists(frame=0, name='chunk1')
                f.chunk_exists(frame=0, name='chunk2')
                f.chunk_exists(frame=0, name='chunk3')
                f.chunk_exists(frame=10, name='chunk1')
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
            ``numpy.ndarray[type, ndim=?, mode='c']``: Data read from file.
            ``type`` is determined by the chunk metadata. If the data is
            NxM in the file and M > 1, return a 2D array. If the data is
            Nx1, return a 1D array.

        .. tip::
            Each call to invokes a disk read and allocation of a
            new numpy array for storage. To avoid overhead, don't call
            :py:meth:`read_chunk()` on the same chunk repeatedly. Cache the
            arrays instead.

        Example:
            .. ipython:: python

                with gsd.fl.open(name='file.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
                    f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
                    f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32));
                    f.end_frame();
                    f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
                    f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32));
                    f.end_frame();

                f = gsd.fl.open(name='file.gsd', mode='rb', application="My application", schema="My Schema", schema_version=[1,0])
                f.read_chunk(frame=0, name='chunk1')
                f.read_chunk(frame=1, name='chunk1')
                @okexcept
                f.read_chunk(frame=2, name='chunk1')
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
        elif gsd_type == libgsd.GSD_TYPE_UINT16:
            data_array = numpy.empty(dtype=numpy.uint16, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_UINT32:
            data_array = numpy.empty(dtype=numpy.uint32, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_UINT64:
            data_array = numpy.empty(dtype=numpy.uint64, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_INT8:
            data_array = numpy.empty(dtype=numpy.int8, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_INT16:
            data_array = numpy.empty(dtype=numpy.int16, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_INT32:
            data_array = numpy.empty(dtype=numpy.int32, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_INT64:
            data_array = numpy.empty(dtype=numpy.int64, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_FLOAT:
            data_array = numpy.empty(dtype=numpy.float32, shape=[index_entry.N, index_entry.M])
        elif gsd_type == libgsd.GSD_TYPE_DOUBLE:
            data_array = numpy.empty(dtype=numpy.float64, shape=[index_entry.N, index_entry.M])
        else:
            raise ValueError("invalid type for chunk: " + name);

        logger.debug('read chunk: ' + self.name + ' - ' + str(frame) + ' - ' + name);

        # only read chunk if we have data
        if index_entry.N != 0 and index_entry.M != 0:
            if gsd_type == libgsd.GSD_TYPE_UINT8:
                data_ptr = __get_ptr_uint8(data_array)
            elif gsd_type == libgsd.GSD_TYPE_UINT16:
                data_ptr = __get_ptr_uint16(data_array)
            elif gsd_type == libgsd.GSD_TYPE_UINT32:
                data_ptr = __get_ptr_uint32(data_array)
            elif gsd_type == libgsd.GSD_TYPE_UINT64:
                data_ptr = __get_ptr_uint64(data_array)
            elif gsd_type == libgsd.GSD_TYPE_INT8:
                data_ptr = __get_ptr_int8(data_array)
            elif gsd_type == libgsd.GSD_TYPE_INT16:
                data_ptr = __get_ptr_int16(data_array)
            elif gsd_type == libgsd.GSD_TYPE_INT32:
                data_ptr = __get_ptr_int32(data_array)
            elif gsd_type == libgsd.GSD_TYPE_INT64:
                data_ptr = __get_ptr_int64(data_array)
            elif gsd_type == libgsd.GSD_TYPE_FLOAT:
                data_ptr = __get_ptr_float32(data_array)
            elif gsd_type == libgsd.GSD_TYPE_DOUBLE:
                data_ptr = __get_ptr_float64(data_array)
            else:
                raise ValueError("invalid type for chunk: " + name);

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

    Create an empty GSD file on the filesystem.

    .. deprecated:: 1.2

        As of version 1.2, you can create and open GSD files in the same call to
        :py:func:`open`. :py:func:`create` is kept for backwards compatibility.

    Args:
        name (str): File name to open.
        application (str): Name of the application creating the file.
        schema (str): Name of the data schema.
        schema_version (``list[int]``): Schema version number [major, minor].

    Example:

        Create a gsd file:

        .. ipython:: python

            gsd.fl.create(name="file.gsd",
                          application="My application",
                          schema="My Schema",
                          schema_version=[1,0]);

    .. danger::
        The file is overwritten if it already exists.
    """

    _c_schema_version = libgsd.gsd_make_version(schema_version[0], schema_version[1])
    retval = libgsd.gsd_create(name.encode('utf-8'), application.encode('utf-8'), schema.encode('utf-8'), _c_schema_version);

    if retval == -1:
        raise IOError(*__format_errno(name));
    elif retval != 0:
        raise RuntimeError("Unknown error");
