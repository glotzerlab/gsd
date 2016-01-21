.. Copyright (c) 2016 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

HOOMD Schema
============

HOOMD-blue now supports a wide variety of per particle attributes and properties. Particles, bonds, and types can be
dynamically added and removed during simulation runs. We need a file schema capable of handling all of these situations
in a reasonably space efficient and high performance manner. When there is a conflict, performance comes first.

For now, rigid body storage is not planned. With the flexibility of GSD, it should be easy to add later. When we know
what form the future rigid body support in hoomd will have.

Use-cases
---------

There are a few problems with XML, DCD, and other dump files that this design wants to solve.

# Every frame of GSD output should be viable for restart from ``init.read_gsd``, with the exception that dynamic
  properties can optionally be disabled.
# No need for a separate topology file - everything is in one ``.gsd`` file.
# Support varying numbers of particles, bonds, etc...
# Support varying attributes (type, mass, etc...)
# Support orientation, angular momentum, and other fields that
# Simple interface for dump - limited number of options that produce valid files

Storage.

* Store per particle quantities

    * Attributes

        * type
        * tag

    * Fixed attributes
        * mass
        * charge
        * diameter
        * moment_inertia

    * Properties

        * position
        * image
        * orientation

    * Dynamic properties

        * velocity
        * angular_momentum

* Store topology

    * bond
    * angle
    * dihedral
    * improper

* Other

    * Store simulation box
    * Store type name mappings
    * Store restart data from other classes

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
