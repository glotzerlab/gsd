.. _fl-examples:

File layer examples
-------------------

The file layer python module :py:mod:`gsd.fl` allows direct low level access to read and write
gsd files of any schema. The hoomd reader (:py:mod:`gsd.hoomd`) provides higher level access to
hoomd schema files, see :ref:`hoomd-examples`.

View the page source to find unformatted example code that can be easily copied.

Create a gsd file
^^^^^^^^^^^^^^^^^

.. ipython:: python

    gsd.fl.create(name="file.gsd",
                  application="My application",
                  schema="My Schema",
                  schema_version=[1,0]);

.. warning:: Creating a gsd file overwrites any existing file with the given name.

Write data
^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='ab');
    f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
    f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32));
    f.end_frame();
    f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
    f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32));
    f.end_frame();
    f.close();

Instantiate a :py:class:`gsd.fl.GSDFile` object to access gsd files on disk.
Add any number of named data chunks to each frame in the file with
:py:meth:`gsd.fl.GSDFile.write_chunk()`. The data must be a 1 or 2
dimensional numpy array of a simple numeric type (or a data type that will automatically
convert when passed to ``numpy.array(data)``. Call :py:meth:`gsd.fl.GSDFile.end_frame()`
to end the frame and start the next one.

.. note:: While supported, implicit conversion to numpy arrays creates a 2nd copy of the data
          in memory and adds conversion overhead.

.. warning:: Make sure to call ``end_frame()`` before closing the file, or the last frame is lost.

Read data
^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
    f.read_chunk(frame=0, name='chunk1')
    f.read_chunk(frame=1, name='chunk2')

:py:meth:`gsd.fl.GSDFile.read_chunk` reads the named chunk at the given frame index in the file
and returns it as a numpy array.

Test if a chunk exists
^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
    f.chunk_exists(frame=0, name='chunk1')
    f.chunk_exists(frame=1, name='chunk2')
    f.chunk_exists(frame=2, name='chunk1')
    f.close()

:py:meth:`gsd.fl.GSDFile.chunk_exists` tests to see if a chunk by the given name exists in the file
at the given frame.

Read-only access
^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
    if f.chunk_exists(frame=0, name='chunk1'):
        data = f.read_chunk(frame=0, name='chunk1')
    data
    # Fails because the file is open read only
    @okexcept
    f.write_chunk(name='error', data=numpy.array([1]))

Files opened in read only (``rb``) mode can be read from, but not written to. The read-only
mode is tuned for high performance reads with minimal memory impact and can easily handle
files with tens of millions of data chunks.

Access file metadata
^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
    f.name
    f.mode
    f.gsd_version
    f.application
    f.schema
    f.schema_version
    f.nframes
    f.close()

Open a file in read/write mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb+');
    f.write_chunk(name='double', data=numpy.array([1,2,3,4], dtype=numpy.float64));
    f.end_frame()
    f.nframes
    f.read_chunk(frame=2, name='double')

Files in read/write mode (``rb+``) are inefficient. Only use this mode if you **must** read and
write to the same file, and only if you are working with relatively small files with fewer than
a million data chunks. Prefer append mode for writing and read-only mode for reading.

Write a file in append mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='ab');
    f.write_chunk(name='int', data=numpy.array([10,20], dtype=numpy.int16));
    f.end_frame()
    f.nframes
    @okexcept
    f.read_chunk(frame=2, name='double')
    f.close()

Append mode is extremely frugal with memory. It only caches data chunks for the frame about to
be committed and clears the cache on a call to :py:meth:`gsd.fl.GSDFile.end_frame()`. This is
especially useful on supercomputers where memory per node is limited, but you may want to
generate gsd files with millions of data chunks.

Use as a context manager
^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.fl.GSDFile(name='file.gsd', mode='rb') as f:
        data = f.read_chunk(frame=1, name='chunk1');
    data

:py:class:`gsd.fl.GSDFile` works as a context manager for guaranteed file closure and cleanup
when exceptions occur.

Store string chunks
^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb+')
    f.mode
    s = "This is a string"
    b = numpy.array([s], dtype=numpy.dtype((bytes, len(s)+1)))
    b = b.view(dtype=numpy.int8)
    b
    f.write_chunk(name='string', data=b)
    f.end_frame()
    r = f.read_chunk(frame=4, name='string')
    r
    r = r.view(dtype=numpy.dtype((bytes, r.shape[0])));
    r[0].decode('UTF-8')

To store a string in a gsd file, convert it to a numpy array of bytes and store that data in
the file. Decode the byte sequence to get back a string.

Truncate
^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='ab')
    f.nframes
    f.schema, f.schema_version, f.application
    f.truncate()
    f.nframes
    f.schema, f.schema_version, f.application

Truncating a gsd file removes all data chunks from it, but retains the same schema, schema
version, and applicaiton name. The file is not closed during this process. This is useful
when writing restart files on a Lustre file system when file open operations need to be
kept to a minimum.
