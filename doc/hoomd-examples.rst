.. _hoomd-examples:

HOOMD examples
--------------

:py:mod:`gsd.hoomd` provides high-level access to HOOMD schema GSD files.

View the page source to find unformatted example code that can be easily copied.

Define a snapshot
^^^^^^^^^^^^^^^^^

.. ipython:: python

    s = gsd.hoomd.Snapshot()
    s.particles.N = 4
    s.particles.types = ['A', 'B']
    s.particles.typeid = [0,0,1,1]
    s.particles.position = [[0,0,0],[1,1,1], [-1,-1,-1], [1,-1,-1]]
    s.configuration.box = [3, 3, 3, 0, 0, 0]

:py:mod:`gsd.hoomd` represents the state of a single frame with an instance of the
class :py:class:`gsd.hoomd.Snapshot`. Instantiate this class to create a system
configuration. All fields default to ``None`` and are only written into the file
if not ``None`` and do not match the data in the first frame, or defaults specified
in the schema.

Create a hoomd gsd file with one frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    gsd.hoomd.create(name='test.gsd', snapshot=s)

.. tip:: ``snapshot`` can be set to None to create a HOOMD schema GSD file with 0 frames.

Append frames to a gsd file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    def create_frame(i):
        s = gsd.hoomd.Snapshot()
        s.configuration.step = i
        s.particles.N = 4+i
        s.particles.position = numpy.random.random(size=(4+i,3))
        return s

    f = gsd.fl.GSDFile('test.gsd', 'wb')
    t = gsd.hoomd.HOOMDTrajectory(f)
    t.extend( (create_frame(i) for i in range(10)) )
    t.append( create_frame(11) )
    # length is 12 because create added one frame, extend added 10, and append added 1
    len(t)
    f.close()

Use :py:class:`gsd.hoomd.HOOMDTrajectory` to hoomd-schema gsd files :py:class:`gsd.fl.GSDFile`
with high level operations. It behaves like a python :py:class:`list`, with
:py:meth:`gsd.hoomd.HOOMDTrajectory.append` and :py:meth:`gsd.hoomd.HOOMDTrajectory.extend`
methods.

.. note:: :py:class:`gsd.hoomd.HOOMDTrajectory` currently doesn't support files opened in
          append mode.

.. tip:: When using :py:meth:`gsd.hoomd.HOOMDTrajectory.extend`, pass in a generator or
         generator expression to avoid storing the entire trajectory in RAM before
         writing it out.

Randomly index frames
^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile('test.gsd', 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f)
    snap = t[5]
    snap.configuration.step
    snap.particles.N
    snap.particles.position
    f.close()

:py:class:`gsd.hoomd.HOOMDTrajectory` supports random indexing of frames in the file. Indexing
into a trajectory returns a :py:class:`gsd.hoomd.Snapshot`.

Slicing
^^^^^^^

.. ipython:: python

    f = gsd.fl.GSDFile('test.gsd', 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f);
    for s in t[5:-2]:
        print(s.configuration.step, end=' ')

Slicing access works like you would expect it to.

Pure python reader
^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.pygsd.GSDFile(open('test.gsd', 'rb'))
    t = gsd.hoomd.HOOMDTrajectory(f);
    t[3].particles.position

You can use GSD without needing to compile C code to read GSD files. Just use
:py:class:`gsd.pygsd.GSDFile` instead of :py:class:`gsd.fl.GSDFile`. It only
supports the ``rb`` mode and does not read files as fast as the C implementation.
It takes in a python file-like object, so it can be used with in-memory IO classes,
grid file classes that access data over the internet, etc...
