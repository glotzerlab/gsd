""" GSD file layer API"""

from libc.stdint cimport uint32_t, int64_t
from libc.errno cimport errno
cimport libgsd
import os

cdef __format_errno(fname):
    """ Return a tuple for constructing an IOError """
    return (errno, os.strerror(errno), fname);

cdef class GSDFile:
    """ GSD file access interface.

    GSDFile implements a python object oriented class interface to the GSD file layer. It can be used as a single use
    context manager::

        with GSDFile(filename, 'r') as f:
            f.do_something()

    Args:
        fname (str): File name to open.
        flags (str): 'r' for read only access, 'w' for read-write access.
    """

    cdef libgsd.gsd_handle __handle;
    cdef bint __is_open;

    def __init__(self, fname, flags):

        cdef libgsd.gsd_open_flag c_flags;
        if flags == 'w':
            c_flags = libgsd.GSD_OPEN_READWRITE;
        elif flags == 'r':
            c_flags = libgsd.GSD_OPEN_READONLY;
        else:
            raise ValueError("flags must be 'r' or 'w'");

        retval = libgsd.gsd_open(&self.__handle, fname.encode('utf-8'), c_flags);

        if retval == -1:
            raise IOError(*__format_errno(fname));
        if retval == -2:
            raise RuntimeError("Not a GSD file: " + fname);
        if retval == -3:
            raise RuntimeError("Unsupported GSD file version: " + fname);
        if retval == -4:
            raise RuntimeError("Corrupt GSD file: " + fname);
        if retval == -5:
            raise MemoryError("Unable to allocate GSD index: " + fname);
        elif retval != 0:
            raise RuntimeError("Unknown error");

        self.__is_open = True;

    def close(self):
        """ Close the file.

        Once closed, any other operation on the file object will result in a `ValueError`. close() may be called
        more than once.
        """
        if self.__is_open:
            libgsd.gsd_close(&self.__handle);
            self.__is_open == False;

    def __enter__(self):
        return self;

    def __exit__(self):
        self.close()

    def __dealloc__(self):
        if self.__is_open:
            libgsd.gsd_close(&self.__handle);
            self.__is_open = False;

def create(fname, application, schema, schema_version):
    """ Create a GSD file.

    create() creates an empty GSD file on disk.

    Args:
        fname (str): File name to open.
        application (str): Name of the application creating the file.
        schema (str): Name of the data schema.
        schema_version (list[int]): Schema version number [major, minor].

    Warning:
        The file *fname* is overwritten if it already exists.
    """

    _c_schema_version = libgsd.gsd_make_version(schema_version[0], schema_version[1])
    retval = libgsd.gsd_create(fname.encode('utf-8'), application.encode('utf-8'), schema.encode('utf-8'), _c_schema_version);

    if retval == -1:
        raise IOError(*__format_errno(fname));
    elif retval != 0:
        raise RuntimeError("Unknown error");
