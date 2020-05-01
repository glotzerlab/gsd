# Copyright (c) 2016-2020 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under
# the BSD 2-Clause License.

"""Test the gsd.hoomd API."""

import gsd.fl
import gsd.hoomd
import numpy
import pickle
import pytest


def test_create(tmp_path):
    """Test that gsd files can be created."""
    with gsd.hoomd.open(name=tmp_path / "test_create.gsd", mode='wb') as hf:
        assert hf.file.schema == 'hoomd'
        assert hf.file.schema_version >= (1, 0)


def test_append(tmp_path, open_mode):
    """Test that gsd files can be appended to."""
    snap = gsd.hoomd.Snapshot()
    snap.particles.N = 10

    with gsd.hoomd.open(name=tmp_path / "test_append.gsd",
                        mode=open_mode.write) as hf:
        for i in range(5):
            snap.configuration.step = i + 1
            hf.append(snap)

    with gsd.hoomd.open(name=tmp_path / "test_append.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 5


def create_frame(i):
    """Helper function to create snapshot objects."""
    snap = gsd.hoomd.Snapshot()
    snap.configuration.step = i + 1
    return snap


def test_extend(tmp_path, open_mode):
    """Test that the extend method works."""
    snap = gsd.hoomd.Snapshot()
    snap.particles.N = 10

    with gsd.hoomd.open(name=tmp_path / "test_extend.gsd",
                        mode=open_mode.write) as hf:
        hf.extend((create_frame(i) for i in range(5)))

    with gsd.hoomd.open(name=tmp_path / "test_extend.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 5


def test_defaults(tmp_path, open_mode):
    """Test that the property defaults are properly set."""
    snap = gsd.hoomd.Snapshot()
    snap.particles.N = 2
    snap.bonds.N = 3
    snap.angles.N = 4
    snap.dihedrals.N = 5
    snap.impropers.N = 6
    snap.constraints.N = 4
    snap.pairs.N = 7

    with gsd.hoomd.open(name=tmp_path / "test_defaults.gsd",
                        mode=open_mode.write) as hf:
        hf.append(snap)

    with gsd.hoomd.open(name=tmp_path / "test_defaults.gsd",
                        mode=open_mode.read) as hf:
        s = hf.read_frame(0)

        assert s.configuration.step == 0
        assert s.configuration.dimensions == 3
        numpy.testing.assert_array_equal(
            s.configuration.box,
            numpy.array([1, 1, 1, 0, 0, 0], dtype=numpy.float32))
        assert s.particles.N == 2
        assert s.particles.types == ['A']
        assert s.particles.type_shapes == [{}]
        numpy.testing.assert_array_equal(
            s.particles.typeid, numpy.array([0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.particles.mass, numpy.array([1, 1], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.diameter, numpy.array([1, 1], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.body, numpy.array([-1, -1], dtype=numpy.int32))
        numpy.testing.assert_array_equal(
            s.particles.charge, numpy.array([0, 0], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.moment_inertia,
            numpy.array([[0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.position,
            numpy.array([[0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.orientation,
            numpy.array([[1, 0, 0, 0], [1, 0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.velocity,
            numpy.array([[0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.angmom,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.image,
            numpy.array([[0, 0, 0], [0, 0, 0]], dtype=numpy.int32))

        assert s.bonds.N == 3
        assert s.bonds.types == []
        numpy.testing.assert_array_equal(
            s.bonds.typeid, numpy.array([0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.bonds.group,
            numpy.array([[0, 0], [0, 0], [0, 0]], dtype=numpy.uint32))

        assert s.angles.N == 4
        assert s.angles.types == []
        numpy.testing.assert_array_equal(
            s.angles.typeid, numpy.array([0, 0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.angles.group,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.dihedrals.N == 5
        assert s.dihedrals.types == []
        numpy.testing.assert_array_equal(
            s.dihedrals.typeid, numpy.array([0, 0, 0, 0, 0],
                                            dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.dihedrals.group,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                         [0, 0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.impropers.N == 6
        assert s.impropers.types == []
        numpy.testing.assert_array_equal(
            s.impropers.typeid,
            numpy.array([0, 0, 0, 0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.impropers.group,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                         [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.constraints.N == 4
        numpy.testing.assert_array_equal(
            s.constraints.value, numpy.array([0, 0, 0, 0], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.constraints.group,
            numpy.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype=numpy.uint32))

        assert s.pairs.N == 7
        assert s.pairs.types == []
        numpy.testing.assert_array_equal(
            s.pairs.typeid, numpy.array([0] * 7, dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.pairs.group, numpy.array([[0, 0]] * 7, dtype=numpy.uint32))

        assert len(s.state) == 0


def test_fallback(tmp_path, open_mode):
    """Test that properties fall back to defaults when the N changes."""
    snap0 = gsd.hoomd.Snapshot()
    snap0.configuration.step = 10000
    snap0.configuration.dimensions = 2
    snap0.configuration.box = [4, 5, 6, 1.0, 0.5, 0.25]
    snap0.particles.N = 2
    snap0.particles.types = ['A', 'B', 'C']
    snap0.particles.type_shapes = [
        {
            "type": "Sphere",
            "diameter": 2.0
        },
        {
            "type": "Sphere",
            "diameter": 3.0
        },
        {
            "type": "Sphere",
            "diameter": 4.0
        },
    ]
    snap0.particles.typeid = [1, 2]
    snap0.particles.mass = [2, 3]
    snap0.particles.diameter = [3, 4]
    snap0.particles.body = [10, 20]
    snap0.particles.charge = [0.5, 0.25]
    snap0.particles.moment_inertia = [[1, 2, 3], [3, 2, 1]]
    snap0.particles.position = [[0.1, 0.2, 0.3], [-1.0, -2.0, -3.0]]
    snap0.particles.orientation = [[1, 0.1, 0.2, 0.3], [0, -1.0, -2.0, -3.0]]
    snap0.particles.velocity = [[1.1, 2.2, 3.3], [-3.3, -2.2, -1.1]]
    snap0.particles.angmom = [[1, 1.1, 2.2, 3.3], [-1, -3.3, -2.2, -1.1]]
    snap0.particles.image = [[10, 20, 30], [5, 6, 7]]

    snap0.bonds.N = 1
    snap0.bonds.types = ['bondA', 'bondB']
    snap0.bonds.typeid = [1]
    snap0.bonds.group = [[0, 1]]

    snap0.angles.N = 1
    snap0.angles.typeid = [2]
    snap0.angles.types = ['angleA', 'angleB']
    snap0.angles.group = [[0, 1, 0]]

    snap0.dihedrals.N = 1
    snap0.dihedrals.typeid = [3]
    snap0.dihedrals.types = ['dihedralA', 'dihedralB']
    snap0.dihedrals.group = [[0, 1, 1, 0]]

    snap0.impropers.N = 1
    snap0.impropers.typeid = [4]
    snap0.impropers.types = ['improperA', 'improperB']
    snap0.impropers.group = [[1, 0, 0, 1]]

    snap0.constraints.N = 1
    snap0.constraints.value = [1.1]
    snap0.constraints.group = [[0, 1]]

    snap0.pairs.N = 1
    snap0.pairs.types = ['pairA', 'pairB']
    snap0.pairs.typeid = [1]
    snap0.pairs.group = [[0, 3]]

    snap0.log['value'] = [1, 2, 4, 10, 12, 18, 22]

    snap1 = gsd.hoomd.Snapshot()
    snap1.particles.N = 2
    snap1.particles.position = [[-2, -1, 0], [1, 3.0, 0.5]]

    snap2 = gsd.hoomd.Snapshot()
    snap2.particles.N = 3
    snap2.particles.types = ['q', 's']
    snap2.particles.type_shapes = \
        [{}, {"type": "Ellipsoid", "a": 7.0, "b": 5.0, "c": 3.0}]
    snap2.bonds.N = 3
    snap2.angles.N = 4
    snap2.dihedrals.N = 5
    snap2.impropers.N = 6
    snap2.constraints.N = 4
    snap2.pairs.N = 7

    with gsd.hoomd.open(name=tmp_path / "test_fallback.gsd",
                        mode=open_mode.write) as hf:
        hf.extend([snap0, snap1, snap2])

    with gsd.hoomd.open(name=tmp_path / "test_fallback.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 3
        s = hf.read_frame(0)

        assert s.configuration.step == snap0.configuration.step
        assert s.configuration.dimensions == snap0.configuration.dimensions
        numpy.testing.assert_array_equal(s.configuration.box,
                                         snap0.configuration.box)
        assert s.particles.N == snap0.particles.N
        assert s.particles.types == snap0.particles.types
        assert s.particles.type_shapes == snap0.particles.type_shapes
        numpy.testing.assert_array_equal(s.particles.typeid,
                                         snap0.particles.typeid)
        numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass)
        numpy.testing.assert_array_equal(s.particles.diameter,
                                         snap0.particles.diameter)
        numpy.testing.assert_array_equal(s.particles.body, snap0.particles.body)
        numpy.testing.assert_array_equal(s.particles.charge,
                                         snap0.particles.charge)
        numpy.testing.assert_array_equal(s.particles.moment_inertia,
                                         snap0.particles.moment_inertia)
        numpy.testing.assert_array_equal(s.particles.position,
                                         snap0.particles.position)
        numpy.testing.assert_array_equal(s.particles.orientation,
                                         snap0.particles.orientation)
        numpy.testing.assert_array_equal(s.particles.velocity,
                                         snap0.particles.velocity)
        numpy.testing.assert_array_equal(s.particles.angmom,
                                         snap0.particles.angmom)
        numpy.testing.assert_array_equal(s.particles.image,
                                         snap0.particles.image)

        assert s.bonds.N == snap0.bonds.N
        assert s.bonds.types == snap0.bonds.types
        numpy.testing.assert_array_equal(s.bonds.typeid, snap0.bonds.typeid)
        numpy.testing.assert_array_equal(s.bonds.group, snap0.bonds.group)

        assert s.angles.N == snap0.angles.N
        assert s.angles.types == snap0.angles.types
        numpy.testing.assert_array_equal(s.angles.typeid, snap0.angles.typeid)
        numpy.testing.assert_array_equal(s.angles.group, snap0.angles.group)

        assert s.dihedrals.N == snap0.dihedrals.N
        assert s.dihedrals.types == snap0.dihedrals.types
        numpy.testing.assert_array_equal(s.dihedrals.typeid,
                                         snap0.dihedrals.typeid)
        numpy.testing.assert_array_equal(s.dihedrals.group,
                                         snap0.dihedrals.group)

        assert s.impropers.N == snap0.impropers.N
        assert s.impropers.types == snap0.impropers.types
        numpy.testing.assert_array_equal(s.impropers.typeid,
                                         snap0.impropers.typeid)
        numpy.testing.assert_array_equal(s.impropers.group,
                                         snap0.impropers.group)

        assert s.constraints.N == snap0.constraints.N
        numpy.testing.assert_array_equal(s.constraints.value,
                                         snap0.constraints.value)
        numpy.testing.assert_array_equal(s.constraints.group,
                                         snap0.constraints.group)

        assert s.pairs.N == snap0.pairs.N
        assert s.pairs.types == snap0.pairs.types
        numpy.testing.assert_array_equal(s.pairs.typeid, snap0.pairs.typeid)
        numpy.testing.assert_array_equal(s.pairs.group, snap0.pairs.group)
        assert 'value' in s.log
        numpy.testing.assert_array_equal(s.log['value'], snap0.log['value'])

        # test that everything but position remained the same in frame 1
        s = hf.read_frame(1)

        assert s.configuration.step == snap0.configuration.step
        assert s.configuration.dimensions == snap0.configuration.dimensions
        numpy.testing.assert_array_equal(s.configuration.box,
                                         snap0.configuration.box)
        assert s.particles.N == snap0.particles.N
        assert s.particles.types == snap0.particles.types
        assert s.particles.type_shapes == snap0.particles.type_shapes
        numpy.testing.assert_array_equal(s.particles.typeid,
                                         snap0.particles.typeid)
        numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass)
        numpy.testing.assert_array_equal(s.particles.diameter,
                                         snap0.particles.diameter)
        numpy.testing.assert_array_equal(s.particles.body, snap0.particles.body)
        numpy.testing.assert_array_equal(s.particles.charge,
                                         snap0.particles.charge)
        numpy.testing.assert_array_equal(s.particles.moment_inertia,
                                         snap0.particles.moment_inertia)
        numpy.testing.assert_array_equal(s.particles.position,
                                         snap1.particles.position)
        numpy.testing.assert_array_equal(s.particles.orientation,
                                         snap0.particles.orientation)
        numpy.testing.assert_array_equal(s.particles.velocity,
                                         snap0.particles.velocity)
        numpy.testing.assert_array_equal(s.particles.angmom,
                                         snap0.particles.angmom)
        numpy.testing.assert_array_equal(s.particles.image,
                                         snap0.particles.image)

        assert s.bonds.N == snap0.bonds.N
        assert s.bonds.types == snap0.bonds.types
        numpy.testing.assert_array_equal(s.bonds.typeid, snap0.bonds.typeid)
        numpy.testing.assert_array_equal(s.bonds.group, snap0.bonds.group)

        assert s.angles.N == snap0.angles.N
        assert s.angles.types == snap0.angles.types
        numpy.testing.assert_array_equal(s.angles.typeid, snap0.angles.typeid)
        numpy.testing.assert_array_equal(s.angles.group, snap0.angles.group)

        assert s.dihedrals.N == snap0.dihedrals.N
        assert s.dihedrals.types == snap0.dihedrals.types
        numpy.testing.assert_array_equal(s.dihedrals.typeid,
                                         snap0.dihedrals.typeid)
        numpy.testing.assert_array_equal(s.dihedrals.group,
                                         snap0.dihedrals.group)

        assert s.impropers.N == snap0.impropers.N
        assert s.impropers.types == snap0.impropers.types
        numpy.testing.assert_array_equal(s.impropers.typeid,
                                         snap0.impropers.typeid)
        numpy.testing.assert_array_equal(s.impropers.group,
                                         snap0.impropers.group)

        assert s.constraints.N == snap0.constraints.N
        numpy.testing.assert_array_equal(s.constraints.value,
                                         snap0.constraints.value)
        numpy.testing.assert_array_equal(s.constraints.group,
                                         snap0.constraints.group)

        assert s.pairs.N == snap0.pairs.N
        assert s.pairs.types == snap0.pairs.types
        numpy.testing.assert_array_equal(s.pairs.typeid, snap0.pairs.typeid)
        numpy.testing.assert_array_equal(s.pairs.group, snap0.pairs.group)

        assert 'value' in s.log
        numpy.testing.assert_array_equal(s.log['value'], snap0.log['value'])

        # check that the third frame goes back to defaults because it has a
        # different N
        s = hf.read_frame(2)

        assert s.particles.N == 3
        assert s.particles.types == ['q', 's']
        assert s.particles.type_shapes == snap2.particles.type_shapes
        numpy.testing.assert_array_equal(
            s.particles.typeid, numpy.array([0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.particles.mass, numpy.array([1, 1, 1], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.diameter, numpy.array([1, 1, 1], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.body, numpy.array([-1, -1, -1], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.charge, numpy.array([0, 0, 0], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.moment_inertia,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.position,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.orientation,
            numpy.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
                        dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.velocity,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.angmom,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.particles.image,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=numpy.int32))

        assert s.bonds.N == 3
        assert s.bonds.types == snap0.bonds.types
        numpy.testing.assert_array_equal(
            s.bonds.typeid, numpy.array([0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.bonds.group,
            numpy.array([[0, 0], [0, 0], [0, 0]], dtype=numpy.uint32))

        assert s.angles.N == 4
        assert s.angles.types == snap0.angles.types
        numpy.testing.assert_array_equal(
            s.angles.typeid, numpy.array([0, 0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.angles.group,
            numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.dihedrals.N == 5
        assert s.dihedrals.types == snap0.dihedrals.types
        numpy.testing.assert_array_equal(
            s.dihedrals.typeid, numpy.array([0, 0, 0, 0, 0],
                                            dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.dihedrals.group,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                         [0, 0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.impropers.N == 6
        assert s.impropers.types == snap0.impropers.types
        numpy.testing.assert_array_equal(
            s.impropers.typeid,
            numpy.array([0, 0, 0, 0, 0, 0], dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.impropers.group,
            numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                         [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=numpy.uint32))

        assert s.constraints.N == 4
        numpy.testing.assert_array_equal(
            s.constraints.value, numpy.array([0, 0, 0, 0], dtype=numpy.float32))
        numpy.testing.assert_array_equal(
            s.constraints.group,
            numpy.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype=numpy.uint32))

        assert s.pairs.N == 7
        assert s.pairs.types == snap0.pairs.types
        numpy.testing.assert_array_equal(
            s.pairs.typeid, numpy.array([0] * 7, dtype=numpy.uint32))
        numpy.testing.assert_array_equal(
            s.pairs.group, numpy.array([[0, 0]] * 7, dtype=numpy.uint32))

        assert 'value' in s.log
        numpy.testing.assert_array_equal(s.log['value'], snap0.log['value'])


def test_fallback2(tmp_path, open_mode):
    """Test additional fallback behaviors."""
    snap0 = gsd.hoomd.Snapshot()
    snap0.configuration.step = 1
    snap0.configuration.dimensions = 3
    snap0.particles.N = 2
    snap0.particles.mass = [2, 3]

    snap1 = gsd.hoomd.Snapshot()
    snap1.configuration.step = 2
    snap1.particles.N = 2
    snap1.particles.position = [[1, 2, 3], [4, 5, 6]]

    with gsd.hoomd.open(name=tmp_path / "test_fallback2.gsd",
                        mode=open_mode.write) as hf:
        hf.extend([snap0, snap1])

    with gsd.hoomd.open(name=tmp_path / "test_fallback2.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 2

        s = hf.read_frame(1)
        numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass)


def test_iteration(tmp_path, open_mode):
    """Test the iteration protocols for hoomd trajectories."""
    with gsd.hoomd.open(name=tmp_path / "test_iteration.gsd",
                        mode=open_mode.write) as hf:
        hf.extend((create_frame(i) for i in range(20)))

    with gsd.hoomd.open(name=tmp_path / "test_iteration.gsd",
                        mode=open_mode.read) as hf:
        step = hf[-1].configuration.step
        assert step == 20

        step = hf[-2].configuration.step
        assert step == 19

        step = hf[-3].configuration.step
        assert step == 18

        step = hf[0].configuration.step
        assert step == 1

        step = hf[-20].configuration.step
        assert step == 1

        with pytest.raises(IndexError):
            step = hf[-21].configuration.step

        with pytest.raises(IndexError):
            step = hf[20]

        snaps = hf[5:10]
        steps = [snap.configuration.step for snap in snaps]
        assert steps == [6, 7, 8, 9, 10]

        snaps = hf[15:50]
        steps = [snap.configuration.step for snap in snaps]
        assert steps == [16, 17, 18, 19, 20]

        snaps = hf[15:-3]
        steps = [snap.configuration.step for snap in snaps]
        assert steps == [16, 17]


def test_slicing_and_iteration(tmp_path, open_mode):
    """Test that hoomd trajectories can be sliced."""
    with gsd.hoomd.open(name=tmp_path / "test_slicing.gsd",
                        mode=open_mode.write) as hf:
        hf.extend((create_frame(i) for i in range(20)))

    with gsd.hoomd.open(name=tmp_path / "test_slicing.gsd",
                        mode=open_mode.read) as hf:
        # Test len()-function on trajectory and sliced trajectory.
        assert len(hf) == 20
        assert len(hf[:10]) == 10

        # Test len()-function with explicit iterator.
        assert len(iter(hf)) == len(hf)
        assert len(iter(hf[:10])) == len(hf[:10])

        # Test iteration with implicit iterator.
        # All iterations are run twice to check for issues
        # with iterator exhaustion.
        assert len(list(hf)) == len(hf)
        assert len(list(hf)) == len(hf)
        assert len(list(hf[:10])) == len(hf[:10])
        assert len(list(hf[:10])) == len(hf[:10])

        # Test iteration with explicit iterator.
        hf_iter = iter(hf)
        assert len(hf_iter) == len(hf)  # sanity check
        assert len(list(hf_iter)) == len(hf)
        assert len(list(hf_iter)) == len(hf)

        # Test iteration with explicit sliced iterator.
        hf_iter = iter(hf[:10])
        assert len(hf_iter) == 10  # sanity check
        assert len(list(hf_iter)) == 10
        assert len(list(hf_iter)) == 10

        # Test frame selection
        with pytest.raises(IndexError):
            hf[len(hf)]
        assert hf[0].configuration.step == hf[0].configuration.step
        assert hf[len(hf) - 1].configuration.step == hf[-1].configuration.step


def test_view_slicing_and_iteration(tmp_path, open_mode):
    """Test that trajectories can be sliced."""
    with gsd.hoomd.open(name=tmp_path / "test_slicing.gsd",
                        mode=open_mode.write) as hf:
        hf.extend((create_frame(i) for i in range(40)))

    with gsd.hoomd.open(name=tmp_path / "test_slicing.gsd",
                        mode=open_mode.read) as hf:
        view = hf[::2]

        # Test len()-function on trajectory and sliced view.
        assert len(view) == 20
        assert len(view[:10]) == 10
        assert len(view[::2]) == 10

        # Test len()-function with explicit iterator.
        assert len(iter(view)) == len(view)
        assert len(iter(view[:10])) == len(view[:10])

        # Test iteration with implicit iterator.
        # All iterations are run twice to check for issues
        # with iterator exhaustion.
        assert len(list(view)) == len(view)
        assert len(list(view)) == len(view)
        assert len(list(view[:10])) == len(view[:10])
        assert len(list(view[:10])) == len(view[:10])
        assert len(list(view[::2])) == len(view[::2])
        assert len(list(view[::2])) == len(view[::2])

        # Test iteration with explicit iterator.
        view_iter = iter(view)
        assert len(view_iter) == len(view)  # sanity check
        assert len(list(view_iter)) == len(view)
        assert len(list(view_iter)) == len(view)

        # Test iteration with explicit sliced iterator.
        view_iter = iter(view[:10])
        assert len(view_iter) == 10  # sanity check
        assert len(list(view_iter)) == 10
        assert len(list(view_iter)) == 10

        # Test frame selection
        with pytest.raises(IndexError):
            view[len(view)]
        assert view[0].configuration.step == view[0].configuration.step
        assert view[len(view)
                    - 1].configuration.step == view[-1].configuration.step


def test_truncate(tmp_path):
    """Test the truncate API."""
    with gsd.hoomd.open(name=tmp_path / "test_iteration.gsd", mode='wb') as hf:
        hf.extend((create_frame(i) for i in range(20)))

        assert len(hf) == 20
        s = hf[10]  # noqa
        assert hf._initial_frame is not None

        hf.truncate()
        assert len(hf) == 0
        assert hf._initial_frame is None


def test_state(tmp_path, open_mode):
    """Test the state chunks."""
    snap0 = gsd.hoomd.Snapshot()

    snap0.state['hpmc/sphere/radius'] = [2.0]
    snap0.state['hpmc/sphere/orientable'] = [1]

    snap1 = gsd.hoomd.Snapshot()

    snap1.state['hpmc/convex_polyhedron/N'] = [3]
    snap1.state['hpmc/convex_polyhedron/vertices'] = [[-1, -1, -1], [0, 1, 1],
                                                      [1, 0, 0]]

    with gsd.hoomd.open(name=tmp_path / "test_state.gsd",
                        mode=open_mode.write) as hf:
        hf.extend([snap0, snap1])

    with gsd.hoomd.open(name=tmp_path / "test_state.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 2
        s = hf.read_frame(0)

        numpy.testing.assert_array_equal(s.state['hpmc/sphere/radius'],
                                         snap0.state['hpmc/sphere/radius'])
        numpy.testing.assert_array_equal(s.state['hpmc/sphere/orientable'],
                                         snap0.state['hpmc/sphere/orientable'])

        s = hf.read_frame(1)

        numpy.testing.assert_array_equal(
            s.state['hpmc/convex_polyhedron/N'],
            snap1.state['hpmc/convex_polyhedron/N'])
        numpy.testing.assert_array_equal(
            s.state['hpmc/convex_polyhedron/vertices'],
            snap1.state['hpmc/convex_polyhedron/vertices'])


def test_log(tmp_path, open_mode):
    """Test the log chunks."""
    snap0 = gsd.hoomd.Snapshot()

    snap0.log['particles/net_force'] = [[1, 2, 3], [4, 5, 6]]
    snap0.log['particles/pair_lj_energy'] = [0, -5, -8, -3]
    snap0.log['value/potential_energy'] = [10]
    snap0.log['value/pressure'] = [-3]

    snap1 = gsd.hoomd.Snapshot()

    snap1.log['particles/pair_lj_energy'] = [1, 2, -4, -10]
    snap1.log['value/pressure'] = [5]

    with gsd.hoomd.open(name=tmp_path / "test_log.gsd",
                        mode=open_mode.write) as hf:
        hf.extend([snap0, snap1])

    with gsd.hoomd.open(name=tmp_path / "test_log.gsd",
                        mode=open_mode.read) as hf:
        assert len(hf) == 2
        s = hf.read_frame(0)

        numpy.testing.assert_array_equal(s.log['particles/net_force'],
                                         snap0.log['particles/net_force'])
        numpy.testing.assert_array_equal(s.log['particles/pair_lj_energy'],
                                         snap0.log['particles/pair_lj_energy'])
        numpy.testing.assert_array_equal(s.log['value/potential_energy'],
                                         snap0.log['value/potential_energy'])
        numpy.testing.assert_array_equal(s.log['value/pressure'],
                                         snap0.log['value/pressure'])

        s = hf.read_frame(1)

        # unspecified entries pull from frame 0
        numpy.testing.assert_array_equal(s.log['particles/net_force'],
                                         snap0.log['particles/net_force'])
        numpy.testing.assert_array_equal(s.log['value/potential_energy'],
                                         snap0.log['value/potential_energy'])

        # specified entries are different in frame 1
        numpy.testing.assert_array_equal(s.log['particles/pair_lj_energy'],
                                         snap1.log['particles/pair_lj_energy'])
        numpy.testing.assert_array_equal(s.log['value/pressure'],
                                         snap1.log['value/pressure'])


def test_pickle(tmp_path, open_mode):
    """Test that hoomd trajectory objects can be pickled."""
    with gsd.hoomd.open(name=tmp_path / "test_pickling.gsd",
                        mode=open_mode.write) as traj:
        traj.extend((create_frame(i) for i in range(20)))
        with pytest.raises(pickle.PickleError):
            pkl = pickle.dumps(traj)
    with gsd.hoomd.open(name=tmp_path / "test_pickling.gsd",
                        mode=open_mode.read) as traj:
        pkl = pickle.dumps(traj)
        with pickle.loads(pkl) as hf:
            assert len(hf) == 20
