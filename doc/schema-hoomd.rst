.. Copyright (c) 2016 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

HOOMD Schema
============

HOOMD-blue supports a wide variety of per particle attributes and properties. Particles, bonds, and types can be
dynamically added and removed during simulation runs. The ``hoomd`` schema can handle all of these situations
in a reasonably space efficient and high performance manner.

:Schema name: ``hoomd``
:Schema version: 0.1

.. warning::
    This schema is a draft version subject to testing. No backward or forward compatibility is planned with a final
    1.0 schema.

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
match that of the binary snapshot API in HOOMD-blue itself (at least at the time of inception).
Data chunks are organized in categories. These categories have no meaning in the ``hoomd`` schema
specification, and are simply an organizational tool. Some file writers may implement options that act on
categories (i.e. write **attributes** out to every frame, or just frame 0).


========================== ========= ====== ==== ======= ================
Name                       Category  Type   Size Default Units
========================== ========= ====== ==== ======= ================
**Configuration**
configuration/step         -         uint64 1x1  0       number
configuration/dimensions   -         uint8  1x1  3       number
configuration/box          -         float  3x3  -       *varies*
**Particle data**
particles/N                attribute uint32 1x1  0       number
particles/typename         attribute int8   NTxM A,B,... UTF-8
particles/typeid           attribute uint32 Nx1  0       number
particles/mass             attribute float  Nx1  1.0     mass
particles/charge           attribute float  Nx1  0.0     charge
particles/diameter         attribute float  Nx1  1.0     length
particles/moment_inertia   attribute float  Nx3  0,0,0   mass * length^2
particles/position         property  float  Nx3  0,0,0   length
particles/orientation      property  float  Nx4  1,0,0,0 unit quaternion
particles/velocity         momentum  float  Nx3  0,0,0   length/time
particles/angmom           momentum  float  Nx4  0,0,0,0 quaternion (??)
particles/image            momentum  int32  Nx3  0,0,0   number
**Bond data**
bonds/N                    topology  uint32 1x1  0       number
bonds/typename             topology  int8   NTxM A,B,... UTF-8
bonds/typeid               topology  uint32 Nx1  0       number
bonds/group                topology  uint32 Nx2  0,0     number
**Angle data**
angles/N                   topology  uint32 1x1  0       number
angles/typename            topology  int8   NTxM A,B,... UTF-8
angles/typeid              topology  uint32 Nx1  0       number
angles/group               topology  uint32 Nx3  0,0     number
**Dihedral data**
dihedrals/N                topology  uint32 1x1  0       number
dihedrals/typename         topology  int8   NTxM A,B,... UTF-8
dihedrals/typeid           topology  uint32 Nx1  0       number
dihedrals/group            topology  uint32 Nx4  0,0     number
**Improper data**
impropers/N                topology  uint32 1x1  0       number
impropers/typename         topology  int8   NTxM A,B,... UTF-8
impropers/typeid           topology  uint32 Nx1  0       number
impropers/group            topology  uint32 Nx4  0,0     number
========================== ========= ====== ==== ======= ================

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

.. chunk:: particles/typename

    :Type: int8
    :Size: NTxM
    :Default: A,B,...
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
    type *id* has a type name matching the corresponding row in :chunk:`particles/typename`.

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
    :Units: quaternion (??)

    Store the angular momentum of each particle. TODO: document format.

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
    * :math:`z_u = z + i_z * l_z
`.

Topology
--------

    * bond
    * angle
    * dihedral
    * improper

Restart data
------------

    * restart data from other classes

Variable N support is implemented by always storing particle tag information. Particles may be added or removed between
frames. Within the limits of tag recycling, particles with the same tag from frame to frame are the same particle.
However, because tags are recycled, attributes such as type, moment_inertia, etc... cannot always be determined from
previous frames. These need to be output new on each frame. In the more typical case of constant N, however, it would
be a waste of disk space to do so. To keep this simple, the GSD hoomd schema will come in two variants. "hoomd" will
always write out all quantities on every frame. "hoomd.fixed" only supports fixed N, fixed number of bonds, fixed
topology, etc... and only writes out attributes and properties on each frame (with the option of including dynamic
properties). Fixed attributes and topology are only written to the 0 frame.

Default values and compression are needed to keep file sizes down. Even "hoomd.fixed" could be very wasteful if (for example)
you only have simulations of spheres and don't need to write out orientation. User intervention should not be required
to choose what to output, most of the time users won't think about it or get it right. The output writer in hoomd
will do this in a smart way. First, every per particle property will have an assigned default value. If that property
is not present in the gsd file, the reader should treat every particle as having the default value. The number of
particles is determined from (TODO....). The HOOMD dump writer for GSD will be intelligent. It will scan the particle
properties each time it writes. If all values are at the default, it will skip writing the properties.

Still, in the "hpmc" schema - topology fields will waste a lot of space for every frame. There is not much that can
be done about this and still maintain the flexibility of varying N or varying topology. Perhaps, compression can
reduce the size of this data significantly because of the repeated values. The library liblzg looks to be a promising
candidate for an embedded compression library. It's decompression performance is extremely fast. Some benchmarks will
help decide if that is worthwhile. In any case, I'm not sure if it will make sense to compress the data while writing
it from HOOMD. Ideas for scalable writes are not compatible with this idea. Or reads, for that matter....... Maybe
we just need to live without compression. The only way it could work in a scalable fashion is if we compressed small
chunks of data - possibly requiring a single list of bonds or types to be broken up into multiple compressed chunks.

Not everything can be automatically determined, though. We don't want to force users to store velocity if they don't
want it..... Or do we? With the current plan, position (12b) + image (6b) + type (2b) + tag (4b) = 24b. Adding velocity
only increases by another 12b (50%). That is only 36b/particle or 36MB for a 1 million particle frame. Disk space and
memory are plentiful, what's a little extra storage to fully ensure that every frame is restartable, and the user
may find that velocity data is useful.

This leaves only one option to users when they want to write a gsd file: Used the fixed schema or not.
