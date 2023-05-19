.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

.. _fl-examples:

File layer examples
-------------------

The file layer python module `gsd.fl` allows direct low level access to read and
write **GSD** files of any schema. The **HOOMD** reader (`gsd.hoomd`) provides
higher level access to **HOOMD** schema files, see :ref:`hoomd-examples`.

View the page source to find unformatted example code.

Import the module
^^^^^^^^^^^^^^^^^

.. ipython:: python

    import gsd.fl

Open a gsd file
^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd",
                    mode='w',
                    application="My application",
                    schema="My Schema",
                    schema_version=[1,0])

Use `gsd.fl.open` to open a gsd file.

.. note::

    When creating a new file, you must specify the application name, schema
    name, and schema version.

.. warning::

    Opening a gsd file with a 'w' or 'x' mode overwrites any existing file with
    the given name.

Close a gsd file
^^^^^^^^^^^^^^^^

.. ipython:: python

    f.close()

Call the `close <gsd.fl.GSDFile.close>` method to close the file.

Write data
^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd",
                    mode='w',
                    application="My application",
                    schema="My Schema",
                    schema_version=[1,0]);
    f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32))
    f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32))
    f.end_frame()
    f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32))
    f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32))
    f.end_frame()
    f.close()

Add any number of named data chunks to each frame in the file with
`write_chunk <gsd.fl.GSDFile.write_chunk>`. The data must be a 1 or 2
dimensional numpy array of a simple numeric type (or a data type that will
automatically convert when passed to ``numpy.array(data)``. Call
`end_frame <gsd.fl.GSDFile.end_frame>` to end the frame and start the next one.

.. note::

    While supported, implicit conversion to numpy arrays creates a copy of the
    data in memory and adds conversion overhead.

.. warning::

    Call `end_frame <gsd.fl.GSDFile.end_frame>` to write the last frame before
    closing the file.

Read data
^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd", mode='r')
    f.read_chunk(frame=0, name='chunk1')
    f.read_chunk(frame=1, name='chunk2')
    f.close()

`read_chunk <gsd.fl.GSDFile.read_chunk>` reads the named chunk at the given
frame index in the file and returns it as a numpy array.

Test if a chunk exists
^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd", mode='r')
    f.chunk_exists(frame=0, name='chunk1')
    f.chunk_exists(frame=1, name='chunk2')
    f.chunk_exists(frame=2, name='chunk1')
    f.close()

`chunk_exists <gsd.fl.GSDFile.chunk_exists>` tests to see if a chunk by the
given name exists in the file at the given frame.

Discover chunk names
^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd", mode='r')
    f.find_matching_chunk_names('')
    f.find_matching_chunk_names('chunk')
    f.find_matching_chunk_names('chunk1')
    f.find_matching_chunk_names('other')

`find_matching_chunk_names <gsd.fl.GSDFile.find_matching_chunk_names>` finds all
chunk names present in a GSD file that start with the given string.

Read-only access
^^^^^^^^^^^^^^^^

.. ipython:: python
    :okexcept:

    f = gsd.fl.open(name="file.gsd", mode='r')
    if f.chunk_exists(frame=0, name='chunk1'):
        data = f.read_chunk(frame=0, name='chunk1')
    data
    # Fails because the file is open read only
    f.write_chunk(name='error', data=numpy.array([1]))
    f.close()

Writes fail when a file is opened in a read only mode.

Access file metadata
^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd", mode='r')
    f.name
    f.mode
    f.gsd_version
    f.application
    f.schema
    f.schema_version
    f.nframes
    f.close()

Read file metadata from properties of the file object.

Open a file in read/write mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd",
                    mode='w',
                    application="My application",
                    schema="My Schema",
                    schema_version=[1,0])
    f.write_chunk(name='double', data=numpy.array([1,2,3,4], dtype=numpy.float64));
    f.end_frame()
    f.nframes
    f.read_chunk(frame=0, name='double')

Open a file in read/write mode to allow both reading and writing.

Use as a context manager
^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.fl.open(name="file.gsd", mode='r') as f:
        data = f.read_chunk(frame=0, name='double');
    data

Use `gsd.fl.GSDFile` as a context manager for guaranteed file closure and
cleanup when exceptions occur.

Store string chunks
^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd",
                    mode='w',
                    application="My application",
                    schema="My Schema",
                    schema_version=[1,0])
    f.mode
    s = "This is a string"
    b = numpy.array([s], dtype=numpy.dtype((bytes, len(s)+1)))
    b = b.view(dtype=numpy.int8)
    b
    f.write_chunk(name='string', data=b)
    f.end_frame()
    r = f.read_chunk(frame=0, name='string')
    r
    r = r.view(dtype=numpy.dtype((bytes, r.shape[0])));
    r[0].decode('UTF-8')
    f.close()

To store a string in a gsd file, convert it to a numpy array of bytes and store
that data in the file. Decode the byte sequence to get back a string.

Truncate
^^^^^^^^

.. ipython:: python

    f = gsd.fl.open(name="file.gsd", mode='r+')
    f.nframes
    f.schema, f.schema_version, f.application
    f.truncate()
    f.nframes
    f.schema, f.schema_version, f.application
    f.close()

Truncating a gsd file removes all data chunks from it, but retains the same
schema, schema version, and application name. The file is not closed during this
process. This is useful when writing restart files on a Lustre file system when
file open operations need to be kept to a minimum.
