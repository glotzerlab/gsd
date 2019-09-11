.. _hoomd-examples:

HOOMD
-----

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

Create a hoomd gsd file
^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    gsd.hoomd.open(name='test.gsd', mode='wb')

Append frames to a gsd file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    def create_frame(i):
        s = gsd.hoomd.Snapshot()
        s.configuration.step = i
        s.particles.N = 4+i
        s.particles.position = numpy.random.random(size=(4+i,3))
        return s

    t = gsd.hoomd.open(name='test.gsd', mode='wb')
    t.extend( (create_frame(i) for i in range(10)) )
    t.append( create_frame(10) )
    len(t)

Use :py:func:`gsd.hoomd.open` to open a GSD file with the high level interface
:py:class:`gsd.hoomd.HOOMDTrajectory`. It behaves like a python :py:class:`list`, with
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

    t = gsd.hoomd.open(name='test.gsd', mode='rb')
    snap = t[5]
    snap.configuration.step
    snap.particles.N
    snap.particles.position

:py:class:`gsd.hoomd.HOOMDTrajectory` supports random indexing of frames in the file. Indexing
into a trajectory returns a :py:class:`gsd.hoomd.Snapshot`.

Slicing and selection
^^^^^^^^^^^^^^^^^^^^^

Use the slicing operator to select individual frames or a subset of a trajectory.

.. ipython:: python

    t = gsd.hoomd.open(name='test.gsd', mode='rb')

    for s in t[5:-2]:
        print(s.configuration.step, end=' ')

    every_2nd_frame = t[::2]  # create a view of a trajectory subset
    for s in every_2nd_frame[:4]:
        print(s.configuration.step, end=' ')

Slicing a trajectory creates a trajectory view, which can then be queried for
length or sliced again.
Selecting individual frames from a view works exactly like selecting individual
frames from the original trajectory object.

Pure python reader
^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.pygsd.GSDFile(open('test.gsd', 'rb'))
    t = gsd.hoomd.HOOMDTrajectory(f);
    t[3].particles.position

You can use GSD without needing to compile C code to read GSD files using
:py:class:`gsd.pygsd.GSDFile` in combination with :py:class:`gsd.hoomd.HOOMDTrajectory`. It only
supports the ``rb`` mode and does not read files as fast as the C implementation.
It takes in a python file-like object, so it can be used with in-memory IO classes, and
grid file classes that access data over the internet.

Access state data
^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.hoomd.open(name='test2.gsd', mode='wb') as t:
        s = gsd.hoomd.Snapshot()
        s.particles.types = ['A', 'B']
        s.state['hpmc/convex_polygon/N'] = [3, 4]
        s.state['hpmc/convex_polygon/vertices'] = [[-1, -1],
                                                   [1, -1],
                                                   [1, 1],
                                                   [-2, -2],
                                                   [2, -2],
                                                   [2, 2],
                                                   [-2, 2]]
        t.append(s)

State data is stored in the ``state`` dictionary as numpy arrays. Place data into this dictionary directly
without the 'state/' prefix and gsd will include it in the output. Shape vertices are stored in a packed
format. In this example, type 'A' has 3 vertices (the first 3 in the list) and type 'B' has 4 (the next 4).

.. ipython:: python

    with gsd.hoomd.open(name='test2.gsd', mode='rb') as t:
        s = t[0]
        print(s.state['hpmc/convex_polygon/N'])
        print(s.state['hpmc/convex_polygon/vertices'])

Access read state data in the same way.

Access logged data
^^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.hoomd.open(name='example.gsd', mode='wb') as t:
        s = gsd.hoomd.Snapshot()
        s.particles.N = 4
        s.log['particles/net_force'] = numpy.array([[-1,2,-3],
                                        [0,2,-4],
                                        [-3,2,1],
                                        [1,2,3]], dtype=numpy.float32)
        s.log['value/potential_energy'] = [1.5]
        t.append(s)

Logged data is stored in the ``log`` dictionary as numpy arrays. Place data into this dictionary directly
without the 'log/' prefix and gsd will include it in the output. Store per-particle quantities with the prefix
``particles/``. Choose another prefix for other quantities.

.. ipython:: python

    t = gsd.hoomd.open(name='example.gsd', mode='rb')
    s = t[0]
    s.log['particles/net_force']
    s.log['value/potential_energy']

Read logged data from the ``log`` dictionary.

Logged data must be a convertible to a numpy array of a supported type:

.. ipython:: python
    :okexcept:

    with gsd.hoomd.open(name='example.gsd', mode='wb') as t:
        s = gsd.hoomd.Snapshot()
        s.particles.N = 4
        s.log['invalid'] = dict(a=1, b=5)
        t.append(s)
