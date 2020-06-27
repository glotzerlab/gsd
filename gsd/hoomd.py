# Copyright (c) 2016-2020 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under
# the BSD 2-Clause License.

"""Read and write HOOMD schema GSD files.

The main package :py:mod:`gsd.hoomd` is a reference implementation of the
GSD schema ``hoomd``. It is a simple, but high performance and memory
efficient, reader and writer for the schema. See :ref:`hoomd-examples`
for full examples.

* `open` - Open a hoomd schema GSD file.
* `HOOMDTrajectory` - Read and write hoomd schema GSD files.
* `Snapshot` - Store the state of a single frame.

    * `ConfigurationData` - Store configuration data in a snapshot.
    * `ParticleData` - Store particle data in a snapshot.
    * `BondData` - Store topology data in a snapshot.
"""

import numpy
from collections import OrderedDict
import logging
import json

try:
    from gsd import fl
except ImportError:
    fl = None

try:
    import gsd
except ImportError:
    gsd = None

logger = logging.getLogger('gsd.hoomd')


class ConfigurationData(object):
    """Store configuration data.

    Use the `Snapshot.configuration` attribute of a to access the configuration.

    Attributes:
        step (int): Time step of this frame (:chunk:`configuration/step`).

        dimensions (int): Number of dimensions
            (:chunk:`configuration/dimensions`).

        box ((6, 1) `numpy.ndarray` of ``numpy.float32``):
            Box dimensions (:chunk:`configuration/box`)
            [lx, ly, lz, xy, xz, yz].
    """

    _default_value = OrderedDict()
    _default_value['step'] = numpy.uint64(0)
    _default_value['dimensions'] = numpy.uint8(3)
    _default_value['box'] = numpy.array([1, 1, 1, 0, 0, 0], dtype=numpy.float32)

    def __init__(self):
        self.step = None
        self.dimensions = None
        self.box = None

    def validate(self):
        """Validate all attributes.

        Convert every array attribute to a `numpy.ndarray` of the proper
        type and check that all attributes have the correct dimensions.

        Ignore any attributes that are ``None``.

        Warning:
            Array attributes that are not contiguous numpy arrays will be
            replaced with contiguous numpy arrays of the appropriate type.
        """
        logger.debug('Validating ConfigurationData')

        if self.box is not None:
            self.box = numpy.ascontiguousarray(self.box, dtype=numpy.float32)
            self.box = self.box.reshape([6])


class ParticleData(object):
    """Store particle data chunks.

    Use the `Snapshot.particles` attribute of a to access the particles.

    Instances resulting from file read operations will always store array
    quantities in `numpy.ndarray` objects of the defined types. User created
    snapshots may provide input data that can be converted to a `numpy.ndarray`.

    Attributes:
        N (int): Number of particles in the snapshot (:chunk:`particles/N`).

        types (`typing.List` [str]):
            Names of the particle types (:chunk:`particles/types`).

        position ((*N*, 3) `numpy.ndarray` of ``numpy.float32``):
            Particle position (:chunk:`particles/position`).

        orientation ((*N*, 4) `numpy.ndarray` of ``numpy.float32``):
            Particle orientation. (:chunk:`particles/orientation`).

        typeid ((*N*, ) `numpy.ndarray` of ``numpy.uint32``):
            Particle type id (:chunk:`particles/typeid`).

        mass ((*N*, ) `numpy.ndarray` of ``numpy.float32``):
            Particle mass (:chunk:`particles/mass`).

        charge ((*N*, ) `numpy.ndarray` of ``numpy.float32``):
            Particle charge (:chunk:`particles/charge`).

        diameter ((*N*, ) `numpy.ndarray` of ``numpy.float32``):
            Particle diameter (:chunk:`particles/diameter`).

        body ((*N*, ) `numpy.ndarray` of ``numpy.int32``):
            Particle body (:chunk:`particles/body`).

        moment_inertia ((*N*, 3) `numpy.ndarray` of ``numpy.float32``):
            Particle moment of inertia (:chunk:`particles/moment_inertia`).

        velocity ((*N*, 3) `numpy.ndarray` of ``numpy.float32``):
            Particle velocity (:chunk:`particles/velocity`).

        angmom ((*N*, 4) `numpy.ndarray` of ``numpy.float32``):
            Particle angular momentum (:chunk:`particles/angmom`).

        image ((*N*, 3) `numpy.ndarray` of ``numpy.int32``):
            Particle image (:chunk:`particles/image`).

        type_shapes (`typing.List` [`typing.Dict`]): Shape specifications for
            visualizing particle types (:chunk:`particles/type_shapes`).
    """

    _default_value = OrderedDict()
    _default_value['N'] = numpy.uint32(0)
    _default_value['types'] = ['A']
    _default_value['typeid'] = numpy.uint32(0)
    _default_value['mass'] = numpy.float32(1.0)
    _default_value['charge'] = numpy.float32(0)
    _default_value['diameter'] = numpy.float32(1.0)
    _default_value['body'] = numpy.int32(-1)
    _default_value['moment_inertia'] = numpy.array([0, 0, 0],
                                                   dtype=numpy.float32)
    _default_value['position'] = numpy.array([0, 0, 0], dtype=numpy.float32)
    _default_value['orientation'] = numpy.array([1, 0, 0, 0],
                                                dtype=numpy.float32)
    _default_value['velocity'] = numpy.array([0, 0, 0], dtype=numpy.float32)
    _default_value['angmom'] = numpy.array([0, 0, 0, 0], dtype=numpy.float32)
    _default_value['image'] = numpy.array([0, 0, 0], dtype=numpy.int32)
    _default_value['type_shapes'] = [{}]

    def __init__(self):
        self.N = 0
        self.position = None
        self.orientation = None
        self.types = None
        self.typeid = None
        self.mass = None
        self.charge = None
        self.diameter = None
        self.body = None
        self.moment_inertia = None
        self.velocity = None
        self.angmom = None
        self.image = None
        self.type_shapes = None

    def validate(self):
        """Validate all attributes.

        Convert every array attribute to a `numpy.ndarray` of the proper
        type and check that all attributes have the correct dimensions.

        Ignore any attributes that are ``None``.

        Warning:
            Array attributes that are not contiguous numpy arrays will be
            replaced with contiguous numpy arrays of the appropriate type.
        """
        logger.debug('Validating ParticleData')

        if self.position is not None:
            self.position = numpy.ascontiguousarray(self.position,
                                                    dtype=numpy.float32)
            self.position = self.position.reshape([self.N, 3])
        if self.orientation is not None:
            self.orientation = numpy.ascontiguousarray(self.orientation,
                                                       dtype=numpy.float32)
            self.orientation = self.orientation.reshape([self.N, 4])
        if self.typeid is not None:
            self.typeid = numpy.ascontiguousarray(self.typeid,
                                                  dtype=numpy.uint32)
            self.typeid = self.typeid.reshape([self.N])
        if self.mass is not None:
            self.mass = numpy.ascontiguousarray(self.mass, dtype=numpy.float32)
            self.mass = self.mass.reshape([self.N])
        if self.charge is not None:
            self.charge = numpy.ascontiguousarray(self.charge,
                                                  dtype=numpy.float32)
            self.charge = self.charge.reshape([self.N])
        if self.diameter is not None:
            self.diameter = numpy.ascontiguousarray(self.diameter,
                                                    dtype=numpy.float32)
            self.diameter = self.diameter.reshape([self.N])
        if self.body is not None:
            self.body = numpy.ascontiguousarray(self.body, dtype=numpy.int32)
            self.body = self.body.reshape([self.N])
        if self.moment_inertia is not None:
            self.moment_inertia = numpy.ascontiguousarray(self.moment_inertia,
                                                          dtype=numpy.float32)
            self.moment_inertia = self.moment_inertia.reshape([self.N, 3])
        if self.velocity is not None:
            self.velocity = numpy.ascontiguousarray(self.velocity,
                                                    dtype=numpy.float32)
            self.velocity = self.velocity.reshape([self.N, 3])
        if self.angmom is not None:
            self.angmom = numpy.ascontiguousarray(self.angmom,
                                                  dtype=numpy.float32)
            self.angmom = self.angmom.reshape([self.N, 4])
        if self.image is not None:
            self.image = numpy.ascontiguousarray(self.image, dtype=numpy.int32)
            self.image = self.image.reshape([self.N, 3])


class BondData(object):
    """Store bond data chunks.

    Use the `Snapshot.bonds`, `Snapshot.angles`, `Snapshot.dihedrals`,
    `Snapshot.impropers`, and `Snapshot.pairs` attributes to access the bonds.

    Instances resulting from file read operations will always store array
    quantities in `numpy.ndarray` objects of the defined types. User created
    snapshots may provide input data that can be converted to a `numpy.ndarray`.

    Note:

        *M* varies depending on the type of bond. `BondData` represents all
        types of bonds.

        ======== ===
        Type     *M*
        ======== ===
        Bond      2
        Angle     3
        Dihedral  4
        Improper  4
        Pair      2
        ======== ===

    Attributes:
        N (int): Number of particles in the snapshot
          (:chunk:`bonds/N`, :chunk:`angles/N`, :chunk:`dihedrals/N`,
          :chunk:`impropers/N`, :chunk:`pairs/N`).

        types (`typing.List` [str]): Names of the particle types
          (:chunk:`bonds/types`, :chunk:`angles/types`,
          :chunk:`dihedrals/types`, :chunk:`impropers/types`,
          :chunk:`pairs/types`).

        typeid ((*N*, 3) `numpy.ndarray` of ``numpy.uint32``):
          Bond type id (:chunk:`bonds/typeid`,
          :chunk:`angles/typeid`, :chunk:`dihedrals/typeid`,
          :chunk:`impropers/typeid`, :chunk:`pairs/types`).

        group ((*N*, *M*) `numpy.ndarray` of ``numpy.uint32``):
          Tags of the particles in the bond (:chunk:`bonds/group`,
          :chunk:`angles/group`, :chunk:`dihedrals/group`,
          :chunk:`impropers/group`, :chunk:`pairs/group`).
    """

    def __init__(self, M):
        self.M = M
        self.N = 0
        self.types = None
        self.typeid = None
        self.group = None

        self._default_value = OrderedDict()
        self._default_value['N'] = numpy.uint32(0)
        self._default_value['types'] = []
        self._default_value['typeid'] = numpy.uint32(0)
        self._default_value['group'] = numpy.array([0] * M, dtype=numpy.int32)

    def validate(self):
        """Validate all attributes.

        Convert every array attribute to a `numpy.ndarray` of the proper
        type and check that all attributes have the correct dimensions.

        Ignore any attributes that are ``None``.

        Warning:
            Array attributes that are not contiguous numpy arrays will be
            replaced with contiguous numpy arrays of the appropriate type.
        """
        logger.debug('Validating BondData')

        if self.typeid is not None:
            self.typeid = numpy.ascontiguousarray(self.typeid,
                                                  dtype=numpy.uint32)
            self.typeid = self.typeid.reshape([self.N])
        if self.group is not None:
            self.group = numpy.ascontiguousarray(self.group, dtype=numpy.int32)
            self.group = self.group.reshape([self.N, self.M])


class ConstraintData(object):
    """Store constraint data chunks.

    Use the `Snapshot.constraints` attribute to access the constraints.

    Instances resulting from file read operations will always store array
    quantities in `numpy.ndarray` objects of the defined types. User created
    snapshots may provide input data that can be converted to a `numpy.ndarray`.

    Attributes:
        N (int): Number of particles in the snapshot (:chunk:`constraints/N`).

        value ((*N*, ) `numpy.ndarray` of ``numpy.float32``):
            Constraint length (:chunk:`constraints/value`).

        group ((*N*, *2*) `numpy.ndarray` of ``numpy.uint32``):
            Tags of the particles in the constraint
            (:chunk:`constraints/group`).
    """

    def __init__(self):
        self.M = 2
        self.N = 0
        self.value = None
        self.group = None

        self._default_value = OrderedDict()
        self._default_value['N'] = numpy.uint32(0)
        self._default_value['value'] = numpy.float32(0)
        self._default_value['group'] = numpy.array([0] * self.M,
                                                   dtype=numpy.int32)

    def validate(self):
        """Validate all attributes.

        Convert every array attribute to a `numpy.ndarray` of the proper
        type and check that all attributes have the correct dimensions.

        Ignore any attributes that are ``None``.

        Warning:
            Array attributes that are not contiguous numpy arrays will be
            replaced with contiguous numpy arrays of the appropriate type.
        """
        logger.debug('Validating ConstraintData')

        if self.value is not None:
            self.value = numpy.ascontiguousarray(self.value,
                                                 dtype=numpy.float32)
            self.value = self.value.reshape([self.N])
        if self.group is not None:
            self.group = numpy.ascontiguousarray(self.group, dtype=numpy.int32)
            self.group = self.group.reshape([self.N, self.M])


class Snapshot(object):
    """Snapshot of a system state.

    Attributes:
        configuration (`ConfigurationData`): Configuration data.

        particles (`ParticleData`): Particles.

        bonds (`BondData`): Bonds.

        angles (`BondData`): Angles.

        dihedrals (`BondData`): Dihedrals.

        impropers (`BondData`): Impropers.

        pairs (`BondData`): Special pair.

        constraints (`ConstraintData`): Distance constraints.

        state (typing.Dict): State data.

        log (typing.Dict): Logged data (values must be `numpy.ndarray` or
            `array_like`)
    """

    def __init__(self):
        self.configuration = ConfigurationData()
        self.particles = ParticleData()
        self.bonds = BondData(2)
        self.angles = BondData(3)
        self.dihedrals = BondData(4)
        self.impropers = BondData(4)
        self.constraints = ConstraintData()
        self.pairs = BondData(2)
        self.state = {}
        self.log = {}

        self._valid_state = [
            'hpmc/integrate/d',
            'hpmc/integrate/a',
            'hpmc/sphere/radius',
            'hpmc/sphere/orientable',
            'hpmc/ellipsoid/a',
            'hpmc/ellipsoid/b',
            'hpmc/ellipsoid/c',
            'hpmc/convex_polyhedron/N',
            'hpmc/convex_polyhedron/vertices',
            'hpmc/convex_spheropolyhedron/N',
            'hpmc/convex_spheropolyhedron/vertices',
            'hpmc/convex_spheropolyhedron/sweep_radius',
            'hpmc/convex_polygon/N',
            'hpmc/convex_polygon/vertices',
            'hpmc/convex_spheropolygon/N',
            'hpmc/convex_spheropolygon/vertices',
            'hpmc/convex_spheropolygon/sweep_radius',
            'hpmc/simple_polygon/N',
            'hpmc/simple_polygon/vertices',
        ]

    def validate(self):
        """Validate all contained snapshot data."""
        logger.debug('Validating Snapshot')

        self.configuration.validate()
        self.particles.validate()
        self.bonds.validate()
        self.angles.validate()
        self.dihedrals.validate()
        self.impropers.validate()
        self.constraints.validate()
        self.pairs.validate()

        # validate HPMC state
        if self.particles.types is not None:
            NT = len(self.particles.types)
        else:
            NT = 1

        if 'hpmc/integrate/d' in self.state:
            self.state['hpmc/integrate/d'] = \
                numpy.ascontiguousarray(self.state['hpmc/integrate/d'],
                                        dtype=numpy.float64)
            self.state['hpmc/integrate/d'] = \
                self.state['hpmc/integrate/d'].reshape([1])

        if 'hpmc/integrate/a' in self.state:
            self.state['hpmc/integrate/a'] = \
                numpy.ascontiguousarray(self.state['hpmc/integrate/a'],
                                        dtype=numpy.float64)
            self.state['hpmc/integrate/a'] = \
                self.state['hpmc/integrate/a'].reshape([1])

        if 'hpmc/sphere/radius' in self.state:
            self.state['hpmc/sphere/radius'] = \
                numpy.ascontiguousarray(self.state['hpmc/sphere/radius'],
                                        dtype=numpy.float32)
            self.state['hpmc/sphere/radius'] = \
                self.state['hpmc/sphere/radius'].reshape([NT])

        if 'hpmc/sphere/orientable' in self.state:
            self.state['hpmc/sphere/orientable'] = \
                numpy.ascontiguousarray(self.state['hpmc/sphere/orientable'],
                                        dtype=numpy.uint8)
            self.state['hpmc/sphere/orientable'] = \
                self.state['hpmc/sphere/orientable'].reshape([NT])

        if 'hpmc/ellipsoid/a' in self.state:
            self.state['hpmc/ellipsoid/a'] = \
                numpy.ascontiguousarray(self.state['hpmc/ellipsoid/a'],
                                        dtype=numpy.float32)
            self.state['hpmc/ellipsoid/a'] = \
                self.state['hpmc/ellipsoid/a'].reshape([NT])
            self.state['hpmc/ellipsoid/b'] = \
                numpy.ascontiguousarray(self.state['hpmc/ellipsoid/b'],
                                        dtype=numpy.float32)
            self.state['hpmc/ellipsoid/b'] = \
                self.state['hpmc/ellipsoid/b'].reshape([NT])
            self.state['hpmc/ellipsoid/c'] = \
                numpy.ascontiguousarray(self.state['hpmc/ellipsoid/c'],
                                        dtype=numpy.float32)
            self.state['hpmc/ellipsoid/c'] = \
                self.state['hpmc/ellipsoid/c'].reshape([NT])

        if 'hpmc/convex_polyhedron/N' in self.state:
            self.state['hpmc/convex_polyhedron/N'] = \
                numpy.ascontiguousarray(self.state['hpmc/convex_polyhedron/N'],
                                        dtype=numpy.uint32)
            self.state['hpmc/convex_polyhedron/N'] = \
                self.state['hpmc/convex_polyhedron/N'].reshape([NT])
            sumN = numpy.sum(self.state['hpmc/convex_polyhedron/N'])

            self.state['hpmc/convex_polyhedron/vertices'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_polyhedron/vertices'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_polyhedron/vertices'] = \
                self.state['hpmc/convex_polyhedron/vertices'].reshape([sumN, 3])

        if 'hpmc/convex_spheropolyhedron/N' in self.state:
            self.state['hpmc/convex_spheropolyhedron/N'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolyhedron/N'],
                    dtype=numpy.uint32)
            self.state['hpmc/convex_spheropolyhedron/N'] = \
                self.state['hpmc/convex_spheropolyhedron/N'].reshape([NT])
            sumN = numpy.sum(self.state['hpmc/convex_spheropolyhedron/N'])

            self.state['hpmc/convex_spheropolyhedron/sweep_radius'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolyhedron/sweep_radius'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_spheropolyhedron/sweep_radius'] = \
                self.state[
                    'hpmc/convex_spheropolyhedron/sweep_radius'].reshape([NT])

            self.state['hpmc/convex_spheropolyhedron/vertices'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolyhedron/vertices'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_spheropolyhedron/vertices'] = \
                self.state[
                    'hpmc/convex_spheropolyhedron/vertices'].reshape([sumN, 3])

        if 'hpmc/convex_polygon/N' in self.state:
            self.state['hpmc/convex_polygon/N'] = \
                numpy.ascontiguousarray(self.state['hpmc/convex_polygon/N'],
                                        dtype=numpy.uint32)
            self.state['hpmc/convex_polygon/N'] = \
                self.state['hpmc/convex_polygon/N'].reshape([NT])
            sumN = numpy.sum(self.state['hpmc/convex_polygon/N'])

            self.state['hpmc/convex_polygon/vertices'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_polygon/vertices'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_polygon/vertices'] = \
                self.state['hpmc/convex_polygon/vertices'].reshape([sumN, 2])

        if 'hpmc/convex_spheropolygon/N' in self.state:
            self.state['hpmc/convex_spheropolygon/N'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolygon/N'],
                    dtype=numpy.uint32)
            self.state['hpmc/convex_spheropolygon/N'] = \
                self.state['hpmc/convex_spheropolygon/N'].reshape([NT])
            sumN = numpy.sum(self.state['hpmc/convex_spheropolygon/N'])

            self.state['hpmc/convex_spheropolygon/sweep_radius'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolygon/sweep_radius'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_spheropolygon/sweep_radius'] = \
                self.state[
                    'hpmc/convex_spheropolygon/sweep_radius'].reshape([NT])

            self.state['hpmc/convex_spheropolygon/vertices'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/convex_spheropolygon/vertices'],
                    dtype=numpy.float32)
            self.state['hpmc/convex_spheropolygon/vertices'] = \
                self.state[
                    'hpmc/convex_spheropolygon/vertices'].reshape([sumN, 2])

        if 'hpmc/simple_polygon/N' in self.state:
            self.state['hpmc/simple_polygon/N'] = \
                numpy.ascontiguousarray(self.state['hpmc/simple_polygon/N'],
                                        dtype=numpy.uint32)
            self.state['hpmc/simple_polygon/N'] = \
                self.state['hpmc/simple_polygon/N'].reshape([NT])
            sumN = numpy.sum(self.state['hpmc/simple_polygon/N'])

            self.state['hpmc/simple_polygon/vertices'] = \
                numpy.ascontiguousarray(
                    self.state['hpmc/simple_polygon/vertices'],
                    dtype=numpy.float32)
            self.state['hpmc/simple_polygon/vertices'] = \
                self.state[
                    'hpmc/simple_polygon/vertices'].reshape([sumN, 2])

        for k in self.state:
            if k not in self._valid_state:
                raise RuntimeError('Not a valid state: ' + k)


class _HOOMDTrajectoryIterable(object):
    """Iterable over a HOOMDTrajectory object."""

    def __init__(self, trajectory, indices):
        self._trajectory = trajectory
        self._indices = indices
        self._indices_iterator = iter(indices)

    def __next__(self):
        return self._trajectory[next(self._indices_iterator)]

    next = __next__  # Python 2.7 compatibility

    def __iter__(self):
        return type(self)(self._trajectory, self._indices)

    def __len__(self):
        return len(self._indices)


class _HOOMDTrajectoryView(object):
    """A view of a HOOMDTrajectory object.

    Enables the slicing and iteration over a subset of a trajectory
    instance.
    """

    def __init__(self, trajectory, indices):
        self._trajectory = trajectory
        self._indices = indices

    def __iter__(self):
        return _HOOMDTrajectoryIterable(self._trajectory, self._indices)

    def __len__(self):
        return len(self._indices)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return type(self)(self._trajectory, self._indices[key])
        else:
            return self._trajectory[self._indices[key]]


class HOOMDTrajectory(object):
    """Read and write hoomd gsd files.

    Args:
        file (`gsd.fl.GSDFile`): File to access.

    Open hoomd GSD files with `open`.
    """

    def __init__(self, file):
        if file.mode == 'ab':
            raise ValueError('Append mode not yet supported')

        self._file = file
        self._initial_frame = None

        logger.info('opening HOOMDTrajectory: ' + str(self.file))

        if self.file.schema != 'hoomd':
            raise RuntimeError('GSD file is not a hoomd schema file: '
                               + str(self.file))
        valid = False
        version = self.file.schema_version
        if (version < (2, 0) and version >= (1, 0)):
            valid = True
        if not valid:
            raise RuntimeError('Incompatible hoomd schema version '
                               + str(version) + ' in: ' + str(self.file))

        logger.info('found ' + str(len(self)) + ' frames')

    @property
    def file(self):
        """:class:`gsd.fl.GSDFile`: The underlying file handle."""
        return self._file

    def __len__(self):
        """The number of frames in the trajectory."""
        return self.file.nframes

    def append(self, snapshot):
        """Append a snapshot to a hoomd gsd file.

        Args:
            snapshot (:py:class:`Snapshot`): Snapshot to append.

        Write the given snapshot to the file at the current frame and increase
        the frame counter. Do not write any fields that are ``None``. For all
        non-``None`` fields, scan them and see if they match the initial frame
        or the default value. If the given data differs, write it out to the
        frame. If it is the same, do not write it out as it can be instantiated
        either from the value at the initial frame or the default value.
        """
        logger.debug('Appending snapshot to hoomd trajectory: '
                     + str(self.file))

        snapshot.validate()

        # want the initial frame specified as a reference to detect if chunks
        # need to be written
        if self._initial_frame is None and len(self) > 0:
            self.read_frame(0)

        for path in [
                'configuration',
                'particles',
                'bonds',
                'angles',
                'dihedrals',
                'impropers',
                'constraints',
                'pairs',
        ]:
            container = getattr(snapshot, path)
            for name in container._default_value:
                if self._should_write(path, name, snapshot):
                    logger.debug('writing data chunk: ' + path + '/' + name)
                    data = getattr(container, name)

                    if name == 'N':
                        data = numpy.array([data], dtype=numpy.uint32)
                    if name == 'step':
                        data = numpy.array([data], dtype=numpy.uint64)
                    if name == 'dimensions':
                        data = numpy.array([data], dtype=numpy.uint8)
                    if name in ('types', 'type_shapes'):
                        if name == 'type_shapes':
                            data = [
                                json.dumps(shape_dict) for shape_dict in data
                            ]
                        wid = max(len(w) for w in data) + 1
                        b = numpy.array(data, dtype=numpy.dtype((bytes, wid)))
                        data = b.view(dtype=numpy.int8).reshape(len(b), wid)

                    self.file.write_chunk(path + '/' + name, data)

        # write state data
        for state, data in snapshot.state.items():
            self.file.write_chunk('state/' + state, data)

        # write log data
        for log, data in snapshot.log.items():
            self.file.write_chunk('log/' + log, data)

        self.file.end_frame()

    def truncate(self):
        """Remove all frames from the file."""
        self.file.truncate()
        self._initial_frame = None

    def close(self):
        """Close the file."""
        self.file.close()
        del self._initial_frame

    def _should_write(self, path, name, snapshot):
        """Test if we should write a given data chunk.

        Args:
            path (str): Path part of the data chunk.
            name (str): Name part of the data chunk.
            snapshot (:py:class:`Snapshot`): Snapshot data is from.

        Returns:
            False if the data matches that in the initial frame. False
            if the data matches all default values. True otherwise.
        """
        container = getattr(snapshot, path)
        data = getattr(container, name)

        if data is None:
            return False

        if self._initial_frame is not None:
            initial_container = getattr(self._initial_frame, path)
            initial_data = getattr(initial_container, name)
            if numpy.array_equal(initial_data, data):
                logger.debug('skipping data chunk, matches frame 0: ' + path
                             + '/' + name)
                return False

        if numpy.array_equiv(data, container._default_value[name]):
            logger.debug('skipping data chunk, default value: ' + path + '/'
                         + name)
            return False

        return True

    def extend(self, iterable):
        """Append each item of the iterable to the file.

        Args:
            iterable: An iterable object the provides :py:class:`Snapshot`
                instances. This could be another HOOMDTrajectory, a generator
                that modifies snapshots, or a simple list of snapshots.
        """
        for item in iterable:
            self.append(item)

    def read_frame(self, idx):
        """Read the frame at the given index from the file.

        Args:
            idx (int): Frame index to read.

        Returns:
            `Snapshot` with the frame data

        Replace any data chunks not present in the given frame with either data
        from frame 0, or initialize from default values if not in frame 0. Cache
        frame 0 data to avoid file read overhead. Return any default data as
        non-writable numpy arrays.
        """
        if idx >= len(self):
            raise IndexError

        logger.debug('reading frame ' + str(idx) + ' from: ' + str(self.file))

        if self._initial_frame is None and idx != 0:
            self.read_frame(0)

        snap = Snapshot()
        # read configuration first
        if self.file.chunk_exists(frame=idx, name='configuration/step'):
            step_arr = self.file.read_chunk(frame=idx,
                                            name='configuration/step')
            snap.configuration.step = step_arr[0]
        else:
            if self._initial_frame is not None:
                snap.configuration.step = self._initial_frame.configuration.step
            else:
                snap.configuration.step = \
                    snap.configuration._default_value['step']

        if self.file.chunk_exists(frame=idx, name='configuration/dimensions'):
            dimensions_arr = self.file.read_chunk(
                frame=idx, name='configuration/dimensions')
            snap.configuration.dimensions = dimensions_arr[0]
        else:
            if self._initial_frame is not None:
                snap.configuration.dimensions = \
                    self._initial_frame.configuration.dimensions
            else:
                snap.configuration.dimensions = \
                    snap.configuration._default_value['dimensions']

        if self.file.chunk_exists(frame=idx, name='configuration/box'):
            snap.configuration.box = self.file.read_chunk(
                frame=idx, name='configuration/box')
        else:
            if self._initial_frame is not None:
                snap.configuration.box = self._initial_frame.configuration.box
            else:
                snap.configuration.box = \
                    snap.configuration._default_value['box']

        # then read all groups that have N, types, etc...
        for path in [
                'particles',
                'bonds',
                'angles',
                'dihedrals',
                'impropers',
                'constraints',
                'pairs',
        ]:
            container = getattr(snap, path)
            if self._initial_frame is not None:
                initial_frame_container = getattr(self._initial_frame, path)

            container.N = 0
            if self.file.chunk_exists(frame=idx, name=path + '/N'):
                N_arr = self.file.read_chunk(frame=idx, name=path + '/N')
                container.N = N_arr[0]
            else:
                if self._initial_frame is not None:
                    container.N = initial_frame_container.N

            # type names
            if 'types' in container._default_value:
                if self.file.chunk_exists(frame=idx, name=path + '/types'):
                    tmp = self.file.read_chunk(frame=idx, name=path + '/types')
                    tmp = tmp.view(dtype=numpy.dtype((bytes, tmp.shape[1])))
                    tmp = tmp.reshape([tmp.shape[0]])
                    container.types = list(a.decode('UTF-8') for a in tmp)
                else:
                    if self._initial_frame is not None:
                        container.types = initial_frame_container.types
                    else:
                        container.types = container._default_value['types']

            # type shapes
            if ('type_shapes' in container._default_value
                    and path == 'particles'):
                if self.file.chunk_exists(frame=idx,
                                          name=path + '/type_shapes'):
                    tmp = self.file.read_chunk(frame=idx,
                                               name=path + '/type_shapes')
                    tmp = tmp.view(dtype=numpy.dtype((bytes, tmp.shape[1])))
                    tmp = tmp.reshape([tmp.shape[0]])
                    container.type_shapes = \
                        list(json.loads(json_string.decode('UTF-8'))
                             for json_string in tmp)
                else:
                    if self._initial_frame is not None:
                        container.type_shapes = \
                            initial_frame_container.type_shapes
                    else:
                        container.type_shapes = \
                            container._default_value['type_shapes']

            for name in container._default_value:
                if name in ('N', 'types', 'type_shapes'):
                    continue

                # per particle/bond quantities
                if self.file.chunk_exists(frame=idx, name=path + '/' + name):
                    container.__dict__[name] = self.file.read_chunk(
                        frame=idx, name=path + '/' + name)
                else:
                    if (self._initial_frame is not None
                            and initial_frame_container.N == container.N):
                        # read default from initial frame
                        container.__dict__[name] = \
                            initial_frame_container.__dict__[name]
                    else:
                        # initialize from default value
                        tmp = numpy.array([container._default_value[name]])
                        s = list(tmp.shape)
                        s[0] = container.N
                        container.__dict__[name] = numpy.empty(shape=s,
                                                               dtype=tmp.dtype)
                        container.__dict__[name][:] = tmp

                    container.__dict__[name].flags.writeable = False

        # read state data
        for state in snap._valid_state:
            if self.file.chunk_exists(frame=idx, name='state/' + state):
                snap.state[state] = self.file.read_chunk(frame=idx,
                                                         name='state/' + state)

        # read log data
        logged_data_names = self.file.find_matching_chunk_names('log/')
        for log in logged_data_names:
            if self.file.chunk_exists(frame=idx, name=log):
                snap.log[log[4:]] = self.file.read_chunk(frame=idx, name=log)
            else:
                if self._initial_frame is not None:
                    snap.log[log[4:]] = self._initial_frame.log[log[4:]]

        # store initial frame
        if self._initial_frame is None and idx == 0:
            self._initial_frame = snap

        return snap

    def __getitem__(self, key):
        """Index trajectory frames.

        The index can be a positive integer, negative integer, or slice and is
        interpreted the same as `list` indexing.

        Warning:
            As you loop over frames, each frame is read from the file when it is
            reached in the iteration. Multiple passes may lead to multiple disk
            reads if the file does not fit in cache.
        """
        if isinstance(key, slice):
            return _HOOMDTrajectoryView(self, range(*key.indices(len(self))))
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self) or key < 0:
                raise IndexError()
            return self.read_frame(key)
        else:
            raise TypeError

    def __iter__(self):
        """Iterate over HOOMD trajectories."""
        return _HOOMDTrajectoryIterable(self, range(len(self)))

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file when the context manager exits."""
        self.file.close()


def open(name, mode='rb'):
    """Open a hoomd schema GSD file.

    The return value of `open` can be used as a context manager.

    Args:
        name (str): File name to open.
        mode (str): File open mode.

    Returns:
        An `HOOMDTrajectory` instance that accesses the file *name* with the
        given mode.

    Valid values for mode:

    +------------------+---------------------------------------------+
    | mode             | description                                 |
    +==================+=============================================+
    | ``'rb'``         | Open an existing file for reading.          |
    +------------------+---------------------------------------------+
    | ``'rb+'``        | Open an existing file for reading and       |
    |                  | writing.                                    |
    +------------------+---------------------------------------------+
    | ``'wb'``         | Open a file for writing. Creates the file   |
    |                  | if needed, or overwrites an existing file.  |
    +------------------+---------------------------------------------+
    | ``'wb+'``        | Open a file for reading and writing.        |
    |                  | Creates the file if needed, or overwrites   |
    |                  | an existing file.                           |
    +------------------+---------------------------------------------+
    | ``'xb'``         | Create a gsd file exclusively and opens it  |
    |                  | for writing.                                |
    |                  | Raise an :py:exc:`FileExistsError`          |
    |                  | exception if it already exists.             |
    +------------------+---------------------------------------------+
    | ``'xb+'``        | Create a gsd file exclusively and opens it  |
    |                  | for reading and writing.                    |
    |                  | Raise an :py:exc:`FileExistsError`          |
    |                  | exception if it already exists.             |
    +------------------+---------------------------------------------+
    | ``'ab'``         | Open an existing file for writing.          |
    |                  | Does *not* create or overwrite existing     |
    |                  | files.                                      |
    +------------------+---------------------------------------------+

    """
    if fl is None:
        raise RuntimeError("file layer module is not available")
    if gsd is None:
        raise RuntimeError("gsd module is not available")

    gsdfileobj = fl.open(name=str(name),
                         mode=mode,
                         application='gsd.hoomd ' + gsd.__version__,
                         schema='hoomd',
                         schema_version=[1, 4])

    return HOOMDTrajectory(gsdfileobj)
