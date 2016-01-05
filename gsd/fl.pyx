""" GSD file layer API"""

from libc.stdint cimport uint32_t, int64_t
cimport libgsd

cdef class GSDFile:
    """ GSD file access interface.

    GSDFile implements a python object oriented class interface to the GSD file layer.

    Args:
        fname (str): File name to open.
        flags (str): 'r' for read only access, 'w' for read-write access.
    """

    cdef libgsd.gsd_handle* __handle;

    def __init__(self, fname, flags):

        cdef libgsd.gsd_open_flag c_flags;
        if flags == 'w':
            c_flags = libgsd.GSD_OPEN_READWRITE;
        elif flags == 'r':
            c_flags = libgsd.GSD_OPEN_READONLY;
        else:
            raise ValueError("flags must be 'r' or 'w'");

        self.__handle = libgsd.gsd_open(fname.encode('utf-8'), c_flags);

    def __dealloc__(self):
        print('closing file')
        if self.__handle is not NULL:
            libgsd.gsd_close(self.__handle)
