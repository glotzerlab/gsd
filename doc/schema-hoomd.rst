.. Copyright (c) 2016-2022 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

HOOMD Schema
============

HOOMD-blue supports a wide variety of per particle attributes and properties.
Particles, bonds, and types can be dynamically added and removed during
simulation runs. The ``hoomd`` schema can handle all of these situations in a
reasonably space efficient and high performance manner. It is also backwards
compatible with previous versions of itself, as we only add new additional data
chunks in new versions and do not change the interpretation of the existing data
chunks. Any newer reader will initialize new data chunks with default values
when they are not present in an older version file.

:Schema name: ``hoomd``
:Schema version: 1.4

.. seealso::

    `hoomd.State` for a full description of how HOOMD interprets this
    data.

Use-cases
---------

The GSD schema ``hoomd`` provides:

#. Every frame of GSD output is viable to restart a simulation
#. Support varying numbers of particles, bonds, etc...
#. Support varying attributes (type, mass, etc...)
#. Support orientation, angular momentum, and other fields.
#. Binary format on disk
#. High performance file read and write
#. Support logging computed quantities

Data chunks
-----------

Each frame the ``hoomd`` schema may contain one or more data chunks. The layout
and names of the chunksmatch that of the binary snapshot API in HOOMD-blue
itself. Data chunks are organized in categories. These categories have no
meaning in the ``hoomd`` schema specification, and are simply an organizational
tool. Some file writers may implement options that act on categories (i.e. write
**attributes** out to every frame, or just frame 0).

Values are well defined for all fields at all frames. When a data chunk is
present in frame *i*, it defines the values for the frame. When it is not
present, the data chunk of the same name at frame 0 defines the values for frame
*i* (when *N* is equal between the frames). If the data chunk is not present in
frame 0, or *N* differs between frames, values are default. Default values allow
files sizes to remain small. For example, a simulation with point particles
where orientation is always (1,0,0,0) would not write any orientation chunk to
the file.

*N* may be zero. When *N* is zero, an index entry may be written for a data
chunk with no actual data written to the file for that chunk.

================================= ========= ====== ==== ======= ================
Name                              Category  Type   Size Default Units
================================= ========= ====== ==== ======= ================
**Configuration**
:chunk:`configuration/step`                 uint64 1x1  0       number
:chunk:`configuration/dimensions`           uint8  1x1  3       number
:chunk:`configuration/box`                  float  6x1          *varies*
**Particle data**
:chunk:`particles/N`              attribute uint32 1x1  0       number
:chunk:`particles/types`          attribute int8   NTxM ['A']   UTF-8
:chunk:`particles/typeid`         attribute uint32 Nx1  0       number
:chunk:`particles/type_shapes`    attribute int8   NTxM         UTF-8
:chunk:`particles/mass`           attribute float  Nx1  1.0     mass
:chunk:`particles/charge`         attribute float  Nx1  0.0     charge
:chunk:`particles/diameter`       attribute float  Nx1  1.0     length
:chunk:`particles/body`           attribute int32  Nx1  -1      number
:chunk:`particles/moment_inertia` attribute float  Nx3  0,0,0   mass * length^2
:chunk:`particles/position`       property  float  Nx3  0,0,0   length
:chunk:`particles/orientation`    property  float  Nx4  1,0,0,0 unit quaternion
:chunk:`particles/velocity`       momentum  float  Nx3  0,0,0   length/time
:chunk:`particles/angmom`         momentum  float  Nx4  0,0,0,0 quaternion
:chunk:`particles/image`          momentum  int32  Nx3  0,0,0   number
**Bond data**
:chunk:`bonds/N`                  topology  uint32 1x1  0       number
:chunk:`bonds/types`              topology  int8   NTxM         UTF-8
:chunk:`bonds/typeid`             topology  uint32 Nx1  0       number
:chunk:`bonds/group`              topology  uint32 Nx2  0,0     number
**Angle data**
:chunk:`angles/N`                 topology  uint32 1x1  0       number
:chunk:`angles/types`             topology  int8   NTxM         UTF-8
:chunk:`angles/typeid`            topology  uint32 Nx1  0       number
:chunk:`angles/group`             topology  uint32 Nx3  0,0,0   number
**Dihedral data**
:chunk:`dihedrals/N`              topology  uint32 1x1  0       number
:chunk:`dihedrals/types`          topology  int8   NTxM         UTF-8
:chunk:`dihedrals/typeid`         topology  uint32 Nx1  0       number
:chunk:`dihedrals/group`          topology  uint32 Nx4  0,0,0,0 number
**Improper data**
:chunk:`impropers/N`              topology  uint32 1x1  0       number
:chunk:`impropers/types`          topology  int8   NTxM         UTF-8
:chunk:`impropers/typeid`         topology  uint32 Nx1  0       number
:chunk:`impropers/group`          topology  uint32 Nx4  0,0,0,0 number
**Constraint data**
:chunk:`constraints/N`            topology  uint32 1x1  0       number
:chunk:`constraints/value`        topology  float  Nx1  0       length
:chunk:`constraints/group`        topology  uint32 Nx2  0,0     number
**Special pairs data**
:chunk:`pairs/N`                  topology  uint32 1x1  0       number
:chunk:`pairs/types`              topology  int8   NTxM         utf-8
:chunk:`pairs/typeid`             topology  uint32 Nx1  0       number
:chunk:`pairs/group`              topology  uint32 Nx2  0,0     number
================================= ========= ====== ==== ======= ================


Configuration
-------------

.. chunk:: configuration/step

    :Type: uint64
    :Size: 1x1
    :Default: 0
    :Units: number

    Simulation time step.

.. chunk:: configuration/dimensions

    :Type: uint8
    :Size: 1x1
    :Default: 3
    :Units: number

    Number of dimensions in the simulation. Must be 2 or 3.

    .. note::
        When using `gsd.hoomd.Snapshot`, the object will try to intelligently default to a
        dimension. When setting a box with :math:`L_z = 0`, ``dimensions`` will default to
        2 otherwise 3. Explicit setting of this value by users always takes precedence.

.. chunk:: configuration/box

    :Type: float
    :Size: 6x1
    :Default: [1,1,1,0,0,0]
    :Units: *varies*

    Simulation box. Each array element defines a different box property. See the
    hoomd documentation for a full description on how these box parameters map
    to a triclinic geometry.

    * ``box[0:3]``: :math:`(l_x, l_y, l_z)` the box length in each direction, in length units
    * ``box[3:]``: :math:`(xy, xz, yz)` the tilt factors, dimensionless values


Particle data
-------------

Within a single frame, the number of particles *N* and *NT* are fixed for all
chunks. *N* and *NT* may vary from one frame to the next. All values are stored
in hoomd native units.

Attributes
^^^^^^^^^^

.. chunk:: particles/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of particles, for all data chunks ``particles/*``.

.. chunk:: particles/types

    :Type: int8
    :Size: NTxM
    :Default: ['A']
    :Units: UTF-8

    Implicitly define *NT*, the number of particle types, for all data chunks
    ``particles/*``. *M* must be large enough to accommodate each type name as a
    null terminated UTF-8 character string. Row *i* of the 2D matrix is the type
    name for particle type *i*.

.. chunk:: particles/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each particle. All id's must be less than *NT*. A
    particle with type *id* has a type name matching the corresponding row in
    :chunk:`particles/types`.

.. chunk:: particles/type_shapes

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Store a per-type shape definition for visualization. A dictionary is stored
    for each of the *NT* types, corresponding to a shape for visualization of
    that type. *M* must be large enough to accommodate the shape definition as
    a null-terminated UTF-8 JSON-encoded string. See: :ref:`shapes` for
    examples.

.. chunk:: particles/mass

    :Type: float (32-bit)
    :Size: Nx1
    :Default: 1.0
    :Units: mass

    Store the mass of each particle.

.. chunk:: particles/charge

    :Type: float (32-bit)
    :Size: Nx1
    :Default: 0.0
    :Units: charge

    Store the charge of each particle.

.. chunk:: particles/diameter

    :Type: float (32-bit)
    :Size: Nx1
    :Default: 1.0
    :Units: length

    Store the diameter of each particle.

.. chunk:: particles/body

    :Type: int32
    :Size: Nx1
    :Default: -1
    :Units: number

    Store the composite body associated with each particle. The value -1
    indicates no body. The body field may be left out of input files, as hoomd
    will create the needed constituent particles.

.. chunk:: particles/moment_inertia

    :Type: float (32-bit)
    :Size: Nx3
    :Default: 0,0,0
    :Units: mass * length^2

    Store the moment_inertia of each particle :math:`(I_{xx}, I_{yy}, I_{zz})`.
    This inertia tensor is diagonal in the body frame of the particle. The
    default value is for point particles.

Properties
^^^^^^^^^^

.. chunk:: particles/position

    :Type: float (32-bit)
    :Size: Nx3
    :Default: 0,0,0
    :Units: length

    Store the position of each particle (*x*, *y*, *z*).

    All particles in the simulation are referenced by a tag. The position data
    chunk (and all other per particle data chunks) list particles in tag order.
    The first particle listed has tag 0, the second has tag 1, ..., and the last
    has tag N-1 where N is the number of particles in the simulation.

    All particles must be inside the box:

    * :math:`-l_x/2 + (xz-xy \cdot yz) \cdot z + xy \cdot y \le x < l_x/2 + (xz-xy \cdot yz) \cdot z + xy \cdot  y`
    * :math:`-l_y/2 + yz \cdot z \le y < l_y/2 + yz \cdot z`
    * :math:`-l_z/2 \le z < l_z/2`

    Where :math:`l_x`, :math:`l_y`, :math:`l_z`, :math:`xy`, :math:`xz`, and :math:`yz` are the
    simulation box parameters (:chunk:`configuration/box`).

.. chunk:: particles/orientation

    :Type: float (32-bit)
    :Size: Nx4
    :Default: 1,0,0,0
    :Units: unit quaternion

    Store the orientation of each particle. In scalar + vector notation, this is
    :math:`(r, a_x, a_y, a_z)`,
    where the quaternion is :math:`q = r + a_xi + a_yj + a_zk`. A unit
    quaternion has the property: :math:`\sqrt{r^2 + a_x^2 + a_y^2 + a_z^2} = 1`.

Momenta
^^^^^^^^

.. chunk:: particles/velocity

    :Type: float (32-bit)
    :Size: Nx3
    :Default: 0,0,0
    :Units: length/time

    Store the velocity of each particle :math:`(v_x, v_y, v_z)`.

.. chunk:: particles/angmom

    :Type: float (32-bit)
    :Size: Nx4
    :Default: 0,0,0,0
    :Units: quaternion

    Store the angular momentum of each particle as a quaternion. See the HOOMD
    documentation for information on how to convert to a vector representation.

.. chunk:: particles/image

    :Type: int32
    :Size: Nx3
    :Default: 0,0,0
    :Units: number

    Store the number of times each particle has wrapped around the box
    :math:`(i_x, i_y, i_z)`. In constant volume simulations, the unwrapped
    position in the particle's full trajectory is

    * :math:`x_u = x + i_x \cdot l_x + xy \cdot i_y \cdot l_y + xz \cdot i_z \cdot l_z`
    * :math:`y_u = y + i_y \cdot l_y + yz \cdot i_z \cdot l_z`
    * :math:`z_u = z + i_z \cdot l_z`

Topology
--------

.. chunk:: bonds/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of bonds, for all data chunks ``bonds/*``.

.. chunk:: bonds/types

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Implicitly define *NT*, the number of bond types, for all data chunks
    ``bonds/*``. *M* must be large enough to accommodate each type name as a
    null terminated UTF-8 character string. Row *i* of the 2D matrix is the type
    name for bond type *i*. By default, there are 0 bond types.

.. chunk:: bonds/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each bond. All id's must be less than *NT*. A bond with
    type *id* has a type name matching the corresponding row in
    :chunk:`bonds/types`.

.. chunk:: bonds/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
    :Units: number

    Store the particle tags in each bond.

.. chunk:: angles/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of angles, for all data chunks ``angles/*``.

.. chunk:: angles/types

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Implicitly define *NT*, the number of angle types, for all data chunks
    ``angles/*``. *M* must be large enough to accommodate each type name as a
    null terminated UTF-8 character string. Row *i* of the 2D matrix is the type
    name for angle type *i*. By default, there are 0 angle types.

.. chunk:: angles/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each angle. All id's must be less than *NT*. A angle
    with type *id* has a type name matching the corresponding row in
    :chunk:`angles/types`.

.. chunk:: angles/group

    :Type: uint32
    :Size: Nx3
    :Default: 0,0,0
    :Units: number

    Store the particle tags in each angle.

.. chunk:: dihedrals/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of dihedrals, for all data chunks ``dihedrals/*``.

.. chunk:: dihedrals/types

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Implicitly define *NT*, the number of dihedral types, for all data chunks
    ``dihedrals/*``. *M* must be large enough to accommodate each type name as a
    null terminated UTF-8 character string. Row *i* of the 2D matrix is the type
    name for dihedral type *i*. By default, there are 0 dihedral types.

.. chunk:: dihedrals/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each dihedral. All id's must be less than *NT*. A
    dihedral with type *id* has a type name matching the corresponding row in
    :chunk:`dihedrals/types`.

.. chunk:: dihedrals/group

    :Type: uint32
    :Size: Nx4
    :Default: 0,0,0,0
    :Units: number

    Store the particle tags in each dihedral.

.. chunk:: impropers/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of impropers, for all data chunks ``impropers/*``.

.. chunk:: impropers/types

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Implicitly define *NT*, the number of improper types, for all data chunks
    ``impropers/*``. *M* must be large enough to accommodate each type name as a
    null terminated UTF-8 character string. Row *i* of the 2D matrix is the type
    name for improper type *i*. By default, there are 0 improper types.

.. chunk:: impropers/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each improper. All id's must be less than *NT*. A
    improper with type *id* has a type name matching the corresponding row in
    :chunk:`impropers/types`.

.. chunk:: impropers/group

    :Type: uint32
    :Size: Nx4
    :Default: 0,0,0,0
    :Units: number

    Store the particle tags in each improper.

.. chunk:: constraints/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of constraints, for all data chunks
    ``constraints/*``.

.. chunk:: constraints/value

    :Type: float
    :Size: Nx1
    :Default: 0
    :Units: length

    Store the distance of each constraint. Each constraint defines a fixed
    distance between two particles.

.. chunk:: constraints/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
    :Units: number

    Store the particle tags in each constraint.

.. chunk:: pairs/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of special pair interactions, for all data chunks
    ``pairs/*``.

    .. versionadded:: 1.1

.. chunk:: pairs/types

    :Type: int8
    :Size: NTxM
    :Default: *empty*
    :Units: UTF-8

    Implicitly define *NT*, the number of special pair types, for all data
    chunks ``pairs/*``. *M* must be large enough to accommodate each type name
    as a null terminated UTF-8 character string. Row *i* of the 2D matrix is the
    type name for particle type *i*. By default, there are 0 special pair types.

    .. versionadded:: 1.1

.. chunk:: pairs/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each special pair interaction. All id's must be less
    than *NT*. A pair with type *id* has a type name matching the corresponding
    row in :chunk:`pairs/types`.

    .. versionadded:: 1.1

.. chunk:: pairs/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
    :Units: number

    Store the particle tags in each special pair interaction.

    .. versionadded:: 1.1

Logged data
------------

Users may store logged data in ``log/*`` data chunks. Logged data encompasses
values computed at simulation time that are too expensive or cumbersome to
re-compute in post processing. This specification does not define specific chunk
names or define logged data. Users may select any valid name for logged data
chunks as appropriate for their workflow.

For any named logged data chunks present in any frame frame the file: If a chunk
is not present in a given frame i != 0, the implementation should provide the
quantity as read from frame 0 for that frame. GSD files that include a logged
data chunk only in some frames i != 0 and not in frame 0 are invalid.

By convention, per-particle and per-bond logged data should have a chunk name
starting with ``log/particles/`` and ``log/bonds``, respectively. Scalar,
vector, and string values may be stored under a different prefix starting with
``log/``. This specification may recognize additional conventions in later
versions without invalidating existing files.

========================================================== ====== ========= ================
Name                                                       Type   Size      Units
========================================================== ====== ========= ================
:chunk:`log/particles/user_defined`                        n/a    NxM       user-defined
:chunk:`log/bonds/user_defined`                            n/a    NxM       user-defined
:chunk:`log/user_defined`                                  n/a    NxM       user-defined
========================================================== ====== ========= ================

.. chunk:: log/particles/user_defined

    :Type: user-defined
    :Size: NxM
    :Units: user-defined

    This chunk is a place holder for any number of user defined per-particle
    quantities. *N* is the number of particles in this frame. *M*, the data
    type, the units, and the chunk name (after the prefix ``log/particles/``)
    are user-defined.

    .. versionadded:: 1.4

.. chunk:: log/bonds/user_defined

    :Type: user-defined
    :Size: NxM
    :Units: user-defined

    This chunk is a place holder for any number of user defined per-bond
    quantities. *N* is the number of bonds in this frame. *M*, the data type,
    the units, and the chunk name (after the prefix ``log/bonds/``) are
    user-defined.

    .. versionadded:: 1.4

.. chunk:: log/user_defined

    :Type: user-defined
    :Size: NxM
    :Units: user-defined

    This chunk is a place holder for any number of user defined quantities. *N*,
    *M*, the data type, the units, and the chunk name (after the prefix
    ``log/``) are user-defined.

    .. versionadded:: 1.4

State data
------------

HOOMD stores auxiliary state information in ``state/*`` data chunks. Auxiliary
state encompasses internal state to any integrator, updater, or other class that
is not part of the particle system state but is also not a fixed parameter. For
example, the internal degrees of freedom in integrator. Auxiliary state is
useful when restarting simulations.

HOOMD only stores state in GSD files when requested explicitly by the user. Only
a few of the documented state data chunks will be present in any GSD file and
not all state chunks are valid. Thus, state data chunks do not have default
values. If a chunk is not present in the file, that state does not have a
well-defined value.

.. note::

    HOOMD-blue >= v3.0.0 do not write state data.

========================================================== ====== ========= ================
Name                                                       Type   Size      Units
========================================================== ====== ========= ================
**HPMC integrator state**
:chunk:`state/hpmc/integrate/d`                            double 1x1       length
:chunk:`state/hpmc/integrate/a`                            double 1x1       number
:chunk:`state/hpmc/sphere/radius`                          float  NTx1      length
:chunk:`state/hpmc/sphere/orientable`                      uint8  NTx1      boolean
:chunk:`state/hpmc/ellipsoid/a`                            float  NTx1      length
:chunk:`state/hpmc/ellipsoid/b`                            float  NTx1      length
:chunk:`state/hpmc/ellipsoid/c`                            float  NTx1      length
:chunk:`state/hpmc/convex_polyhedron/N`                    uint32 NTx1      number
:chunk:`state/hpmc/convex_polyhedron/vertices`             float  sum(N)x3  length
:chunk:`state/hpmc/convex_spheropolyhedron/N`              uint32 NTx1      number
:chunk:`state/hpmc/convex_spheropolyhedron/vertices`       float  sum(N)x3  length
:chunk:`state/hpmc/convex_spheropolyhedron/sweep_radius`   float  NTx1      length
:chunk:`state/hpmc/convex_polygon/N`                       uint32 NTx1      number
:chunk:`state/hpmc/convex_polygon/vertices`                float  sum(N)x2  length
:chunk:`state/hpmc/convex_spheropolygon/N`                 uint32 NTx1      number
:chunk:`state/hpmc/convex_spheropolygon/vertices`          float  sum(N)x2  length
:chunk:`state/hpmc/convex_spheropolygon/sweep_radius`      float  NTx1      length
:chunk:`state/hpmc/simple_polygon/N`                       uint32 NTx1      number
:chunk:`state/hpmc/simple_polygon/vertices`                float  sum(N)x2  length
========================================================== ====== ========= ================

HPMC integrator state
^^^^^^^^^^^^^^^^^^^^^

*NT* is the number of particle types.

.. chunk:: state/hpmc/integrate/d

    :Type: double
    :Size: 1x1
    :Units: length

    *d* is the maximum trial move displacement.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/integrate/a

    :Type: double
    :Size: 1x1
    :Units: number

    *a* is the size of the maximum rotation move.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/sphere/radius

    :Type: float
    :Size: NTx1
    :Units: length

    Sphere radius for each particle type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/sphere/orientable

        :Type: uint8
        :Size: NTx1
        :Units: boolean

    Orientable flag for each particle type.

    .. versionadded:: 1.3

.. chunk:: state/hpmc/ellipsoid/a

    :Type: float
    :Size: NTx1
    :Units: length

    Size of the first ellipsoid semi-axis for each particle type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/ellipsoid/b

    :Type: float
    :Size: NTx1
    :Units: length

    Size of the second ellipsoid semi-axis for each particle type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/ellipsoid/c

    :Type: float
    :Size: NTx1
    :Units: length

    Size of the third ellipsoid semi-axis for each particle type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_polyhedron/N

    :Type: uint32
    :Size: NTx1
    :Units: number

    Number of vertices defined for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_polyhedron/vertices

    :Type: float
    :Size: sum(N)x3
    :Units: length

    Position of the vertices in the shape for all types. The shape for type 0 is
    the first N[0] vertices, the shape for type 1 is the next N[1] vertices, and
    so on...

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolyhedron/N

    :Type: uint32
    :Size: NTx1
    :Units: number

    Number of vertices defined for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolyhedron/vertices

    :Type: float
    :Size: sum(N)x3
    :Units: length

    Position of the vertices in the shape for all types. The shape for type 0 is
    the first N[0] vertices, the shape for type 1 is the next N[1] vertices, and
    so on...

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolyhedron/sweep_radius

    :Type: float
    :Size: NTx1
    :Units: length

    Sweep radius for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_polygon/N

    :Type: uint32
    :Size: NTx1
    :Units: number

    Number of vertices defined for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_polygon/vertices

    :Type: float
    :Size: sum(N)x2
    :Units: length

    Position of the vertices in the shape for all types. The shape for type 0 is
    the first N[0] vertices, the shape for type 1 is the next N[1] vertices, and
    so on...

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolygon/N

    :Type: uint32
    :Size: NTx1
    :Units: number

    Number of vertices defined for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolygon/vertices

    :Type: float
    :Size: sum(N)x2
    :Units: length

    Position of the vertices in the shape for all types. The shape for type 0 is
    the first N[0] vertices, the shape for type 1 is the next N[1] vertices, and
    so on...

    .. versionadded:: 1.2

.. chunk:: state/hpmc/convex_spheropolygon/sweep_radius

    :Type: float
    :Size: NTx1
    :Units: length

    Sweep radius for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/simple_polygon/N

    :Type: uint32
    :Size: NTx1
    :Units: number

    Number of vertices defined for each type.

    .. versionadded:: 1.2

.. chunk:: state/hpmc/simple_polygon/vertices

    :Type: float
    :Size: sum(N)x2
    :Units: length

    Position of the vertices in the shape for all types. The shape for type 0 is
    the first N[0] vertices, the shape for type 1 is the next N[1] vertices, and
    so on...

    .. versionadded:: 1.2
