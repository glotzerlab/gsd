.. Copyright (c) 2016-2020 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released
.. under the BSD 2-Clause License.

.. _hoomd-examples:

HOOMD
-----

`gsd.hoomd` provides high-level access to **HOOMD** schema **GSD** files.

View the page source to find unformatted example code.

Define a snapshot
^^^^^^^^^^^^^^^^^

.. ipython:: python

    s = gsd.hoomd.Snapshot()
    s.particles.N = 4
    s.particles.types = ['A', 'B']
    s.particles.typeid = [0,0,1,1]
    s.particles.position = [[0,0,0],[1,1,1], [-1,-1,-1], [1,-1,-1]]
    s.configuration.box = [3, 3, 3, 0, 0, 0]

`gsd.hoomd` represents the state of a single frame with an instance of
the class `gsd.hoomd.Snapshot`. Instantiate this class to create a
system configuration. All fields default to `None` and are only written into
the file if not `None` and do not match the data in the first frame or
defaults specified in the schema.

Create a hoomd gsd file
^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.hoomd.open(name='file.gsd', mode='wb')
    @suppress
    f.close()


Write frames to a gsd file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    def create_frame(i):
        s = gsd.hoomd.Snapshot()
        s.configuration.step = i
        s.particles.N = 4+i
        s.particles.position = numpy.random.random(size=(4+i,3))
        return s

    f = gsd.hoomd.open(name='test.gsd', mode='wb')
    f.extend( (create_frame(i) for i in range(10)) )
    f.append( create_frame(10) )
    len(f)
    @suppress
    f.close()

Use `gsd.hoomd.open` to open a **GSD** file with the high level interface
`gsd.hoomd.HOOMDTrajectory`. It behaves like a `list`, with
`append <gsd.hoomd.HOOMDTrajectory.append>` and
`extend <gsd.hoomd.HOOMDTrajectory.extend>` methods.

.. note:: `gsd.hoomd.HOOMDTrajectory` currently does not support files opened in
          append mode.

.. tip:: When using `extend <gsd.hoomd.HOOMDTrajectory.extend>`, pass in a
         generator or generator expression to avoid storing the entire
         trajectory in memory before writing it out.

Randomly index frames
^^^^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.hoomd.open(name='test.gsd', mode='rb')
    snap = f[5]
    snap.configuration.step
    snap.particles.N
    snap.particles.position
    @suppress
    f.close()

`gsd.hoomd.HOOMDTrajectory` supports random indexing of frames in the file.
Indexing into a trajectory returns a `gsd.hoomd.Snapshot`.

Slicing and selection
^^^^^^^^^^^^^^^^^^^^^

Use the slicing operator to select individual frames or a subset of a
trajectory.

.. ipython:: python

    f = gsd.hoomd.open(name='test.gsd', mode='rb')

    for s in f[5:-2]:
        print(s.configuration.step, end=' ')

    every_2nd_frame = f[::2]  # create a view of a trajectory subset
    for s in every_2nd_frame[:4]:
        print(s.configuration.step, end=' ')
    @suppress
    f.close()

Slicing a trajectory creates a trajectory view, which can then be queried for
length or sliced again. Selecting individual frames from a view works exactly
like selecting individual frames from the original trajectory object.

Pure python reader
^^^^^^^^^^^^^^^^^^

.. ipython:: python

    f = gsd.pygsd.GSDFile(open('test.gsd', 'rb'))
    t = gsd.hoomd.HOOMDTrajectory(f);
    t[3].particles.position
    @suppress
    f.close()

You can use **GSD** without needing to compile C code to read **GSD** files
using `gsd.pygsd.GSDFile` in combination with `gsd.hoomd.HOOMDTrajectory`. It
only supports the ``rb`` mode and does not read files as fast as the C
implementation. It takes in a python file-like object, so it can be used with
in-memory IO classes, and grid file classes that access data over the internet.

.. warning::

    `gsd.pygsd` is **slow**. Use `gsd.hoomd.open` whenever possible.

Access logged data
^^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.hoomd.open(name='example.gsd', mode='wb') as f:
        s = gsd.hoomd.Snapshot()
        s.particles.N = 4
        s.log['particles/net_force'] = numpy.array([[-1,2,-3],
                                        [0,2,-4],
                                        [-3,2,1],
                                        [1,2,3]], dtype=numpy.float32)
        s.log['value/potential_energy'] = [1.5]
        f.append(s)

Logged data is stored in the ``log`` dictionary as numpy arrays. Place data into
this dictionary directly without the 'log/' prefix and gsd will include it in
the output. Store per-particle quantities with the prefix ``particles/``. Choose
another prefix for other quantities.

.. ipython:: python

    f = gsd.hoomd.open(name='example.gsd', mode='rb')
    s = f[0]
    s.log['particles/net_force']
    s.log['value/potential_energy']
    @suppress
    f.close()

Read logged data from the ``log`` dictionary.

.. note::

    Logged data must be a convertible to a numpy array of a supported type.

    .. ipython:: python
        :okexcept:

        with gsd.hoomd.open(name='example.gsd', mode='wb') as f:
            s = gsd.hoomd.Snapshot()
            s.particles.N = 4
            s.log['invalid'] = dict(a=1, b=5)
            f.append(s)

Access state data
^^^^^^^^^^^^^^^^^

.. ipython:: python

    with gsd.hoomd.open(name='test2.gsd', mode='wb') as f:
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
        f.append(s)

State data is stored in the ``state`` dictionary as numpy arrays. Place data
into this dictionary directly without the 'state/' prefix and gsd will include
it in the output. Shape vertices are stored in a packed format. In this example,
type 'A' has 3 vertices (the first 3 in the list) and type 'B' has 4 (the next
4).

.. ipython:: python

    with gsd.hoomd.open(name='test2.gsd', mode='rb') as f:
        s = f[0]
        print(s.state['hpmc/convex_polygon/N'])
        print(s.state['hpmc/convex_polygon/vertices'])

Access read state data in the same way.

Use multiprocessing
^^^^^^^^^^^^^^^^^^^

.. ipython:: python

   import multiprocessing

   def cnt_part(args):
      t, frame = args
      return len(t[frame].particles.position)

   with gsd.hoomd.open(name='test.gsd', mode='rb') as t:
      with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
         result = pool.map(cnt_part, [(t, frame) for frame in range(len(t))])

    result

`gsd.hoomd.HOOMDTrajectory` can be pickled when in read mode to allow for
multiprocessing through pythons native multiprocessing library. Here
``cnt_part`` finds the number of particles in each frame and appends it to a
list.

Using the command line
^^^^^^^^^^^^^^^^^^^^^^

The GSD library provides a command line interface for reading files with
first-class support for reading HOOMD GSD files. The CLI opens a Python
interpreter with a file opened in a specified mode.

.. code-block:: console

   gsd read -s hoomd 'test.gsd'
