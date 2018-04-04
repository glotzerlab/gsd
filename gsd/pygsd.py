# Copyright (c) 2016-2018 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

""" GSD reader written in pure python

:file:`pygsd.py` is a pure python implementation of a GSD reader. If your analysis tool is written in python and you
want to embed a GSD reader without requiring C code compilation, then use the following python files from the
:file:`gsd/` directory to make a pure python reader. It is not as high performance as the C reader, but is reasonable
for files up to a few thousand frames.

* :file:`gsd/`

    * :file:`__init__.py`
    * :file:`pygsd.py`
    * :file:`hoomd.py`


The reader reads from file-like python objects, which may be useful for reading from in memory buffers, in-database
grid files, etc... For regular files on the filesystem, and for writing gsd files, use :py:mod:`gsd.fl`.

The :py:class:`GSDFile` in this module can be used with the :py:class:`gsd.hoomd.HOOMDTrajectory` hoomd reader:

>>> with gsd.pygsd.GSDFile('test.gsd', 'rb') as f:
...     t = gsd.hoomd.HOOMDTrajectory(f);
...     pos = t[0].particles.position

"""

from __future__ import print_function
from __future__ import division
import logging
import numpy
import struct
from collections import namedtuple
import sys

__version__ = "1.5.2";

logger = logging.getLogger('gsd.pygsd')

gsd_header = namedtuple('gsd_header', 'magic index_location index_allocated_entries namelist_location namelist_allocated_entries schema_version gsd_version application schema reserved')
gsd_header_struct = struct.Struct('QQQQQII64s64s80s');

gsd_index_entry = namedtuple('gsd_index_entry', 'frame N location M id type flags');
gsd_index_entry_struct = struct.Struct('QQqIHBB');

gsd_namelist_entry = namedtuple('gsd_namelist_entry', 'name');
gsd_namelist_entry_struct = struct.Struct('64s');

gsd_type_mapping = {
    1: numpy.dtype('uint8'),
    2: numpy.dtype('uint16'),
    3: numpy.dtype('uint32'),
    4: numpy.dtype('uint64'),
    5: numpy.dtype('int8'),
    6: numpy.dtype('int16'),
    7: numpy.dtype('int32'),
    8: numpy.dtype('int64'),
    9: numpy.dtype('float32'),
    10: numpy.dtype('float64'),
    }

class GSDFile(object):
    """ GSDFile(file)

    GSD file access interface. Implemented in pure python and accepts any python file-like object.

    Args:

        file: File-like object to read.

    GSDFile implements an object oriented class interface to the GSD file
    layer. Use it to open an existing file in a **read-only** mode. For
    read-write access to files, use the full featured C implementation in
    :py:mod:`gsd.fl`. Otherwise, this implementation has all the same methods
    and the two classes can be used interchangeably.

    Examples:

        Open a file in **read-only** mode::

            f = GSDFile(open('file.gsd', mode='rb'));
            if f.chunk_exists(frame=0, name='chunk'):
                data = f.read_chunk(frame=0, name='chunk');

        Access file **metadata**::

            f = GSDFile(open('file.gsd', mode='rb'));
            print(f.name, f.mode, f.gsd_version);
            print(f.application, f.schema, f.schema_version);
            print(f.nframes);

        Use as a **context manager**::

            with GSDFile(open('file.gsd', mode='rb')) as f:
                data = f.read_chunk(frame=0, name='chunk');

    Attributes:

        file (file-like): File-like object opened **(read only)**.
        name (str): file.name **(read only)**.
        mode (str): Mode of the open file **(read only)**.
        gsd_version (tuple[int]): GSD file layer version number [major, minor] **(read only)**.
        application (str): Name of the generating application **(read only)**.
        schema (str): Name of the data schema **(read only)**.
        schema_version (tuple[int]): Schema version number [major, minor] **(read only)**.
        nframes (int): Number of frames **(read only)**.
    """

    def __init__(self, file):
        self.__file = file;

        logger.info('opening file: ' + str(file));

        # read the header
        self.__file.seek(0);
        try:
            header_raw = self.__file.read(gsd_header_struct.size);
        except UnicodeDecodeError:
            print("\nDid you open the file in binary mode (rb)?\n", file=sys.stderr);
            raise;

        if len(header_raw) != gsd_header_struct.size:
            raise IOError;

        self.__header = gsd_header._make(gsd_header_struct.unpack(header_raw));

        # validate the header
        if self.__header.magic != 0x65DF65DF65DF65DF:
            raise RuntimeError("Not a GSD file: " + str(self.__file));
        if self.__header.gsd_version < (1 << 16) and self.__header.gsd_version != (0 << 16 | 3):
            raise RuntimeError("Unsupported GSD file version: " + str(self.__file));
        if self.__header.gsd_version >= (2 << 16):
            raise RuntimeError("Unsupported GSD file version: " + str(self.__file));

        # determine the file size (only works in python 3)
        self.__file.seek(0, 2);

        # read the index block. Since this is a read-only implementation, only read in the used entries
        self.__index = [];
        self.__file.seek(self.__header.index_location, 0);
        for i in range(self.__header.index_allocated_entries):
            index_entry_raw = self.__file.read(gsd_index_entry_struct.size);
            if len(index_entry_raw) != gsd_index_entry_struct.size:
                raise IOError

            idx = gsd_index_entry._make(gsd_index_entry_struct.unpack(index_entry_raw));

            # 0 location signifies end of index
            if idx.location == 0:
                break
            self.__index.append(idx);

        # read the namelist block into a dict for easy lookup
        self.__namelist = {};
        c = 0;
        self.__file.seek(self.__header.namelist_location, 0);
        for i in range(self.__header.index_allocated_entries):
            namelist_entry_raw = self.__file.read(gsd_namelist_entry_struct.size);
            n = gsd_namelist_entry._make(gsd_namelist_entry_struct.unpack(namelist_entry_raw));

            # 0 first byte signifies end
            sname = n.name.rstrip(b'\x00').decode('utf-8')
            if len(sname) == 0:
                break

            self.__namelist[sname] = c;
            c = c + 1;

        self.__is_open = True;

    def close(self):
        """ close()

        Close the file.

        Once closed, any other operation on the file object will result in a
        `ValueError`. :py:meth:`close()` may be called more than once.
        The file is automatically closed when garbage collected or when
        the context manager exits.
        """
        if self.__is_open:
            logger.info('closing file: ' + str(self.__file));
            self.__handle = None;
            self.__index = None;
            self.__namelist = None;
            self.__is_open = False;
            self.__file.close();

    def truncate(self):
        raise NotImplementedError;

    def end_frame(self):
        raise NotImplementedError;

    def write_chunk(self, name, data):
        raise NotImplementedError

    def _find_chunk(self, frame, name):
        # find the id for the given name
        if name in self.__namelist:
            match_id = self.__namelist[name];
        else:
            return None;

        # binary search for the first index entry at the requested frame
        L = 0;
        R = len(self.__index);

        # progressively narrow the search window by halves
        while (R-L > 1):
            m = (L+R)//2;

            if frame < self.__index[m].frame:
                R = m;
            else:
                L = m;

        # this finds L = the rightmost index with the desired frame
        # search all index entries with the matching frame
        cur_index = L;
        while cur_index >= 0 and self.__index[cur_index].frame == frame:
            if match_id == self.__index[cur_index].id:
                return self.__index[cur_index];
            cur_index = cur_index - 1;

        # if we got here, we didn't find the specified chunk
        return None;


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

                with GSDFile(open('file.gsd', mode='rb')) as f:
                    if f.chunk_exists(frame=0, name='chunk'):
                        return f.read_chunk(frame=0, name='chunk');
                    else:
                        return None;
        """

        if not self.__is_open:
            raise ValueError("File is not open");

        chunk = self._find_chunk(frame, name);
        return chunk is not None;

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

        Examples:

            Read a 1D array::

                with GSDFile(name=filename, mode='rb') as f:
                    data = f.read_chunk(frame=0, name='chunk1d');
                    # data.shape == [N]

            Read a 2D array::

                with GSDFile(name=filename, mode='rb') as f:
                    data = f.read_chunk(frame=0, name='chunk2d');
                    # data.shape == [N,M]

            Read multiple frames::

                with GSDFile(name=filename, mode='rb') as f:
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

        chunk = self._find_chunk(frame, name);

        if chunk is None:
            raise KeyError("frame " + str(frame) + " / chunk " + name + " not found in: " + str(self.__file));

        logger.debug('read chunk: ' + str(self.__file) + ' - ' + str(frame) + ' - ' + name);

        size = chunk.N * chunk.M * gsd_type_mapping[chunk.type].itemsize;
        if size == 0 or chunk.location == 0:
            raise RuntimeError("Corrupt chunk: " + str(frame) + " / " + name + " in file" + str(self.__file));

        self.__file.seek(chunk.location, 0);
        data_raw = self.__file.read(size);

        if len(data_raw) != size:
            raise IOError;

        data_npy = numpy.fromstring(data_raw, dtype=gsd_type_mapping[chunk.type]);

        if chunk.M == 1:
            return data_npy;
        else:
            return data_npy.reshape([chunk.N, chunk.M]);

    def __enter__(self):
        return self;

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def name(self):
        return self.__file.name;

    @property
    def file(self):
        return self.__file;

    @property
    def mode(self):
        return 'rb';

    @property
    def gsd_version(self):
        v = self.__header.gsd_version;
        return (v >> 16, v & 0xffff);

    @property
    def schema_version(self):
        v = self.__header.schema_version;
        return (v >> 16, v & 0xffff);

    @property
    def schema(self):
        return self.__header.schema.rstrip(b'\x00').decode('utf-8');

    @property
    def application(self):
        return self.__header.application.rstrip(b'\x00').decode('utf-8');

    @property
    def  nframes(self):
        if not self.__is_open:
            raise ValueError("File is not open");

        if len(self.__index) == 0:
            return 0;
        else:
            return self.__index[-1].frame+1;
