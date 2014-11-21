from ctypes import *
from ctypes import util
import os
import sys

# find and load the library
libfile = util.find_library('gsd');

# if not found, try relative to the module path
if libfile is None:
    path = os.path.dirname(__file__)
    libfile = path + '/../../../../lib/libgsd.so.1';
    # libfile = path + '/../../../../lib/libgsd.1.dylib';
    if not os.path.isfile(libfile):
        raise RuntimeError('libgsd.so not found');

_libgsd = CDLL(libfile, use_errno=True);

# define function arguments
_libgsd.gsd_create.argtypes = [c_char_p, c_char_p, c_char_p, c_uint];
_libgsd.gsd_create.restype = c_int;

_libgsd.gsd_open.argtypes = [c_char_p];
_libgsd.gsd_open.restype = c_void_p;

_libgsd.gsd_close.argtypes = [c_void_p];
_libgsd.gsd_close.restype = c_int;

_libgsd.gsd_end_frame.argtypes = [c_void_p];
_libgsd.gsd_end_frame.restype = c_int;

_libgsd.gsd_write_chunk.argtypes = [c_void_p, c_char_p, c_ubyte, c_ulonglong, c_ulonglong, c_ulonglong, c_void_p];
_libgsd.gsd_write_chunk.restype = c_int;

_libgsd.gsd_get_last_step.argtypes = [c_void_p];
_libgsd.gsd_get_last_step.restype = c_ulonglong;

_libgsd.gsd_get_nframes.argtypes = [c_void_p];
_libgsd.gsd_get_nframes.restype = c_ulonglong;

_libgsd.gsd_find_chunk.argtypes = [c_void_p, c_ulonglong, c_char_p]
_libgsd.gsd_find_chunk.restype = c_void_p;

_libgsd.gsd_read_chunk.argtypes = [c_void_p, c_void_p, c_void_p];
_libgsd.gsd_read_chunk.restype = c_int;

_libgsd.gsd_sizeof_type.argtypes = [c_ubyte]
_libgsd.gsd_sizeof_type.restype = c_size_t;

# helper function to convert a str to a char_p array for use in ctypes
def _str_to_char_p(s):
    # return the same thing if it is already a bytes object
    if isinstance(s, bytes):
        return s;

    # need to convert to a bytes object, which is different in python2 and python3
    if sys.version_info[0] > 2:
        return bytes(s, 'utf_8');
    else:
        return bytes(s);

def gsd_create(fname, application, schema, schema_version):
    retval = _libgsd.gsd_create(_str_to_char_p(fname), _str_to_char_p(application), _str_to_char_p(schema), c_uint(schema_version));
    if retval != 0:
        raise RuntimeError("Error creating GSD file: {0}".format(os.strerror(get_errno())))
    return retval

def gsd_open(fname):
    retval = _libgsd.gsd_open(_str_to_char_p(fname));
    if retval is None:
        raise RuntimeError("Error opening GSD file: {0}".format(os.strerror(get_errno())))

    return c_void_p(retval)

def gsd_close(handle):
    retval = _libgsd.gsd_close(handle);
    if retval != 0:
        raise RuntimeError("Error closing GSD file: {0}".format(os.strerror(get_errno())))
    return retval

def gsd_end_frame(handle):
    retval = _libgsd.gsd_end_frame(handle);
    if retval != 0:
        raise RuntimeError("Error ending frame in GSD file: {0}".format(os.strerror(get_errno())))
    return retval

def gsd_write_chunk(handle, name, type, N, M, step, data):
    retval = _libgsd.gsd_write_chunk(handle,
                                       _str_to_char_p(name),
                                       c_ubyte(type),
                                       c_ulonglong(N),
                                       c_ulonglong(M),
                                       c_ulonglong(step),
                                       data.ctypes.data_as(c_void_p));
    if retval != 0:
        raise RuntimeError("Error writing GSD file: {0}".format(os.strerror(get_errno())))
    return retval

def gsd_get_last_step(handle):
    return _libgsd.gsd_get_last_step(handle);

def gsd_get_nframes(handle):
    return _libgsd.gsd_get_nframes(handle);

def gsd_find_chunk(handle, frame, name):
    retval = _libgsd.gsd_find_chunk(handle, c_ulonglong(frame), _str_to_char_p(name));
    return retval

def gsd_read_chunk(handle, data, chunk):
    #addr, count = data.buffer_info()

    #retval = _libgsd.gsd_read_chunk(handle,
    #                                  cast(addr, c_void_p),
    #                                  chunk);

    retval = _libgsd.gsd_read_chunk(handle,
                                      data.ctypes.data_as(c_void_p),
                                      chunk);
    if retval != 0:
        raise RuntimeError("Error reading GSD file: {0}".format(os.strerror(get_errno())))
    return retval
