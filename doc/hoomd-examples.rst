.. _hoomd-examples:

HOOMD schema
------------

Create a gsd file
^^^^^^^^^^^^^^^^^

.. ipython:: python

    gsd.fl.create(name="file.gsd",
                  application="My application",
                  schema="My Schema",
                  schema_version=[1,0]);

Add data
^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='wb');
    f.write_chunk(name='chunk1', data=numpy.array([1,2,3,4], dtype=numpy.float32));
    f.write_chunk(name='chunk2', data=numpy.array([[5,6],[7,8]], dtype=numpy.float32));
    f.end_frame();
    f.write_chunk(name='chunk1', data=numpy.array([9,10,11,12], dtype=numpy.float32));
    f.write_chunk(name='chunk2', data=numpy.array([[13,14],[15,16]], dtype=numpy.float32));
    f.end_frame();
    f.close();


Read it back
^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile(name='file.gsd', mode='rb');
    f.read_chunk(frame=0, name='chunk1')
    f.read_chunk(frame=1, name='chunk2')
    f.close()

