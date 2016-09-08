.. Copyright (c) 2016 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

HOOMD Schema
============

HOOMD-blue supports a wide variety of per particle attributes and properties. Particles, bonds, and types can be
dynamically added and removed during simulation runs. The ``hoomd`` schema can handle all of these situations
in a reasonably space efficient and high performance manner. It is also backwards compatible with previous versions
of itself, as we only add new additional data chunks in new versions and do not change the interpretation
of the existing data chunks. Any newer reader will initialize new data chunks with default values when they are
not present in an older version file.

:Schema name: ``hoomd``
:Schema version: 1.0

Use-cases
---------

There are a few problems with XML, DCD, and other dump files that the GSD schema ``hoomd`` solves.

#. Every frame of GSD output is viable for restart from ``init.read_gsd``
#. No need for a separate topology file - everything is in one ``.gsd`` file.
#. Support varying numbers of particles, bonds, etc...
#. Support varying attributes (type, mass, etc...)
#. Support orientation, angular momentum, and other fields that DCD cannot.
#. Simple interface for dump - limited number of options that produce valid files
#. Binary format on disk
#. High performance file read and write

Data chunks
-----------

Each frame the ``hoomd`` schema may contain one or more data chunks. The layout and names of the chunks
closely match that of the binary snapshot API in HOOMD-blue itself (at least at the time of inception).
Data chunks are organized in categories. These categories have no meaning in the ``hoomd`` schema
specification, and are simply an organizational tool. Some file writers may implement options that act on
categories (i.e. write **attributes** out to every frame, or just frame 0).

Values are well defined for all fields at all frames. When a data chunk is present in frame *i*, it defines
the values for the frame. When it is not present, the data chunk of the same name at frame 0
defines the values for frame *i* (when *N* is equal between the frames). If the data chunk is not present in
frame 0, or *N* differs between frames, values are assumed default. Default values allow files sizes to
remain small. For example, a simulation with point particles where orientation is always (1,0,0,0) would
not write any orientation chunk to the file.

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

.. chunk:: configuration/box

    :Type: float
    :Size: 6x1
    :Default: [1,1,1,0,0,0]
    :Units: *varies*

    Simulation box. Each array element defines a different box property. See the hoomd documentation for
    a full description on how these box parameters map to a triclinic geometry.

    * `box[0:3]`: :math:`(l_x, l_y, l_z)` the box length in each direction, in length units
    * `box[3:]`: :math:`(xy, xz, yz)` the tilt factors, unitless values


Particle data
-------------

Within a single frame, the number of particles *N* and *NT* are fixed for all chunks. *N* and *NT* may vary from
one frame to the next. All values are stored in hoomd native units.

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

    Implicitly define *NT*, the number of particle types, for all data chunks ``particles/*``.
    *M* must be large enough to accommodate each type name as a null terminated UTF-8
    character string. Row *i* of the 2D matrix is the type name for particle type *i*.

.. chunk:: particles/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each particle. All id's must be less than *NT*. A particle with
    type *id* has a type name matching the corresponding row in :chunk:`particles/types`.

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

    Store the composite body associated with each particle. The value -1 indicates no body. The body field may be left
    out of input files, as hoomd will create the needed constituent particles.

.. chunk:: particles/moment_inertia

    :Type: float (32-bit)
    :Size: Nx3
    :Default: 0,0,0
    :Units: mass * length^2

    Store the moment_inertia of each particle :math:`(I_{xx}, I_{yy}, I_{zz})`. This inertia tensor
    is diagonal in the body frame of the particle. The default value is for point particles.

Properties
^^^^^^^^^^

.. chunk:: particles/position

    :Type: float (32-bit)
    :Size: Nx3
    :Default: 0,0,0
    :Units: length

    Store the position of each particle (*x*, *y*, *z*).

    All particles in the simulation are referenced by a tag. The position data chunk (and all other
    per particle data chunks) list particles in tag order. The first particle listed has tag 0,
    the second has tag 1, ..., and the last has tag N-1 where N is the number of particles in the
    simulation.

    All particles must be inside the box:

    * :math:`x > -l_x/2 + (xz-xy \cdot yz) \cdot z + xy  \cdot  y` and :math:`x < l_x/2 + (xz-xy \cdot yz) \cdot z + xy  \cdot  y`
    * :math:`y > -l_y/2 + yz  \cdot  z` and :math:`y < l_y/2 + yz \cdot z`
    * :math:`z > -l_z/2` and :math:`z < l_z/2`


.. chunk:: particles/orientation

    :Type: float (32-bit)
    :Size: Nx4
    :Default: 1,0,0,0
    :Units: unit quaternion

    Store the orientation of each particle. In scalar + vector notation, this is
    :math:`(r, a_x, a_y, a_z)`,
    where the quaternion is :math:`q = r + a_xi + a_yj + a_zk`. A unit quaternion
    has the property: :math:`\sqrt{r^2 + a_x^2 + a_y^2 + a_z^2} = 1`.

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

    Store the angular momentum of each particle as a quaternion. See the HOOMD documentation for information on how to
    convert to a vector representation.

.. chunk:: particles/image

    :Type: int32
    :Size: Nx3
    :Default: 0,0,0
    :Units: number

    Store the number of times each particle has wrapped around the box :math:`(i_x, i_y, i_z)`.
    In constant volume simulations, the unwrapped position in the particle's full trajectory
    is

    * :math:`x_u = x + i_x \cdot l_x + xy \cdot i_y \cdot l_y + xz \cdot i_z \cdot l_z`
    * :math:`y_u = y + i_y \cdot l_y + yz \cdot i_z * l_z`
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

    Implicitly define *NT*, the number of particle types, for all data chunks ``bonds/*``.
    *M* must be large enough to accommodate each type name as a null terminated UTF-8
    character string. Row *i* of the 2D matrix is the type name for particle type *i*.
    By default, there are 0 bond types.

.. chunk:: bonds/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each bond. All id's must be less than *NT*. A bond with
    type *id* has a type name matching the corresponding row in :chunk:`bonds/types`.

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

    Implicitly define *NT*, the number of particle types, for all data chunks ``angles/*``.
    *M* must be large enough to accommodate each type name as a null terminated UTF-8
    character string. Row *i* of the 2D matrix is the type name for particle type *i*.
    By default, there are 0 angle types.

.. chunk:: angles/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each angle. All id's must be less than *NT*. A angle with
    type *id* has a type name matching the corresponding row in :chunk:`angles/types`.

.. chunk:: angles/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
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

    Implicitly define *NT*, the number of particle types, for all data chunks ``dihedrals/*``.
    *M* must be large enough to accommodate each type name as a null terminated UTF-8
    character string. Row *i* of the 2D matrix is the type name for particle type *i*.
    By default, there are 0 dihedral types.

.. chunk:: dihedrals/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each dihedral. All id's must be less than *NT*. A dihedral with
    type *id* has a type name matching the corresponding row in :chunk:`dihedrals/types`.

.. chunk:: dihedrals/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
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

    Implicitly define *NT*, the number of particle types, for all data chunks ``impropers/*``.
    *M* must be large enough to accommodate each type name as a null terminated UTF-8
    character string. Row *i* of the 2D matrix is the type name for particle type *i*.
    By default, there are 0 improper types.

.. chunk:: impropers/typeid

    :Type: uint32
    :Size: Nx1
    :Default: 0
    :Units: number

    Store the type id of each improper. All id's must be less than *NT*. A improper with
    type *id* has a type name matching the corresponding row in :chunk:`impropers/types`.

.. chunk:: impropers/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
    :Units: number

    Store the particle tags in each improper.

.. chunk:: constraints/N

    :Type: uint32
    :Size: 1x1
    :Default: 0
    :Units: number

    Define *N*, the number of constraints, for all data chunks ``constraints/*``.

.. chunk:: constraints/value

    :Type: float
    :Size: Nx1
    :Default: 0
    :Units: length

    Store the distance of each constraint. Each constraint defines a fixed distance
    between two particles.

.. chunk:: constraints/group

    :Type: uint32
    :Size: Nx2
    :Default: 0,0
    :Units: number

    Store the particle tags in each constraint.

Restart data
------------

HOOMD restart files store additional information in ``restart/*`` data chunks.
The format of this data varies from class to class and is not defined in this
specification. All restart data is meant for internal use by hoomd only.
