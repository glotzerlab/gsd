# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.fl
import gsd.hoomd
import tempfile
import numpy
from nose.tools import ok_, eq_, assert_raises

def test_create():
    with tempfile.TemporaryDirectory() as d:
        gsd.hoomd.create(name=d+"/test_create.gsd", snapshot=None);

        with gsd.fl.GSDFile(name=d+"/test_create.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(f.schema, 'hoomd');
            ok_(f.schema_version >= (1,0));

def test_append():
    with tempfile.TemporaryDirectory() as d:
        snap = gsd.hoomd.Snapshot();
        snap.particles.N = 10;
        gsd.hoomd.create(name=d+"/test_append.gsd", snapshot=snap);

        with gsd.fl.GSDFile(name=d+"/test_append.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            for i in range(5):
                snap.configuration.step=i+1;
                hf.append(snap);

        with gsd.fl.GSDFile(name=d+"/test_append.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(len(hf), 6);

def create_frame(i):
    snap = gsd.hoomd.Snapshot();
    snap.configuration.step = i+1;
    return snap

def test_extend():
    with tempfile.TemporaryDirectory() as d:
        snap = gsd.hoomd.Snapshot();
        snap.particles.N = 10;
        gsd.hoomd.create(name=d+"/test_extend.gsd", snapshot=snap);

        with gsd.fl.GSDFile(name=d+"/test_extend.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            hf.extend((create_frame(i) for i in range(5)));

        with gsd.fl.GSDFile(name=d+"/test_extend.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(len(hf), 6);

def test_defaults():
    with tempfile.TemporaryDirectory() as d:
        snap = gsd.hoomd.Snapshot();
        snap.particles.N = 2;
        snap.bonds.N = 3;
        snap.angles.N = 4;
        snap.dihedrals.N = 5;
        snap.impropers.N = 6;
        snap.constraints.N = 4;
        snap.pairs.N = 7;
        gsd.hoomd.create(name=d+"/test_defaults.gsd", snapshot=snap);

        with gsd.fl.GSDFile(name=d+"/test_defaults.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            s = hf.read_frame(0);

            eq_(s.configuration.step, 0);
            eq_(s.configuration.dimensions, 3);
            numpy.testing.assert_array_equal(s.configuration.box, numpy.array([1,1,1,0,0,0], dtype=numpy.float32));
            eq_(s.particles.N, 2);
            eq_(s.particles.types, ['A']);
            numpy.testing.assert_array_equal(s.particles.typeid, numpy.array([0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.particles.mass, numpy.array([1,1], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.diameter, numpy.array([1,1], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.body, numpy.array([-1,-1], dtype=numpy.int32));
            numpy.testing.assert_array_equal(s.particles.charge, numpy.array([0,0], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.moment_inertia, numpy.array([[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.position, numpy.array([[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.orientation, numpy.array([[1,0,0,0],[1,0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.velocity, numpy.array([[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.angmom, numpy.array([[0,0,0,0],[0,0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.image, numpy.array([[0,0,0],[0,0,0]], dtype=numpy.int32));

            eq_(s.bonds.N, 3);
            eq_(s.bonds.types, []);
            numpy.testing.assert_array_equal(s.bonds.typeid, numpy.array([0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.bonds.group, numpy.array([[0,0],[0,0],[0,0]], dtype=numpy.uint32));

            eq_(s.angles.N, 4);
            eq_(s.angles.types, []);
            numpy.testing.assert_array_equal(s.angles.typeid, numpy.array([0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.angles.group, numpy.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.uint32));

            eq_(s.dihedrals.N, 5);
            eq_(s.dihedrals.types, []);
            numpy.testing.assert_array_equal(s.dihedrals.typeid, numpy.array([0,0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.dihedrals.group, numpy.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype=numpy.uint32));

            eq_(s.impropers.N, 6);
            eq_(s.impropers.types, []);
            numpy.testing.assert_array_equal(s.impropers.typeid, numpy.array([0,0,0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.impropers.group, numpy.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype=numpy.uint32));

            eq_(s.constraints.N, 4);
            numpy.testing.assert_array_equal(s.constraints.value, numpy.array([0,0,0,0], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.constraints.group, numpy.array([[0,0],[0,0],[0,0], [0,0]], dtype=numpy.uint32));

            eq_(s.pairs.N, 7);
            eq_(s.pairs.types, []);
            numpy.testing.assert_array_equal(s.pairs.typeid, numpy.array([0]*7, dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.pairs.group, numpy.array([[0,0]]*7, dtype=numpy.uint32));

            eq_(len(s.state), 0)

def test_fallback():
    with tempfile.TemporaryDirectory() as d:
        snap0 = gsd.hoomd.Snapshot();
        snap0.configuration.step = 10000;
        snap0.configuration.dimensions = 2;
        snap0.configuration.box = [4,5,6,1.0,0.5,0.25];
        snap0.particles.N = 2;
        snap0.particles.types = ['A', 'B', 'C']
        snap0.particles.typeid = [1,2];
        snap0.particles.mass = [2,3];
        snap0.particles.diameter = [3,4];
        snap0.particles.body = [10, 20];
        snap0.particles.charge = [0.5, 0.25];
        snap0.particles.moment_inertia = [[1,2,3], [3,2,1]];
        snap0.particles.position = [[0.1, 0.2, 0.3], [-1.0, -2.0, -3.0]];
        snap0.particles.orientation = [[1, 0.1, 0.2, 0.3], [0, -1.0, -2.0, -3.0]];
        snap0.particles.velocity = [[1.1, 2.2, 3.3], [-3.3, -2.2, -1.1]];
        snap0.particles.angmom = [[1, 1.1, 2.2, 3.3], [-1, -3.3, -2.2, -1.1]];
        snap0.particles.image = [[10, 20, 30], [5, 6, 7]];

        snap0.bonds.N = 1;
        snap0.bonds.types = ['bondA', 'bondB']
        snap0.bonds.typeid = [1];
        snap0.bonds.group = [[0,1]];

        snap0.angles.N = 1;
        snap0.angles.typeid = [2];
        snap0.angles.types = ['angleA', 'angleB']
        snap0.angles.group = [[0,1, 0]];

        snap0.dihedrals.N = 1;
        snap0.dihedrals.typeid = [3];
        snap0.dihedrals.types = ['dihedralA', 'dihedralB']
        snap0.dihedrals.group = [[0,1, 1, 0]];

        snap0.impropers.N = 1;
        snap0.impropers.typeid = [4];
        snap0.impropers.types = ['improperA', 'improperB']
        snap0.impropers.group = [[1, 0, 0, 1]];

        snap0.constraints.N = 1;
        snap0.constraints.value = [1.1];
        snap0.constraints.group = [[0,1]];

        snap0.pairs.N = 1;
        snap0.pairs.types = ['pairA', 'pairB']
        snap0.pairs.typeid = [1];
        snap0.pairs.group = [[0,3]];

        snap1 = gsd.hoomd.Snapshot();
        snap1.particles.N = 2;
        snap1.particles.position = [[-2, -1, 0], [1, 3.0, 0.5]];

        snap2 = gsd.hoomd.Snapshot();
        snap2.particles.N = 3;
        snap2.particles.types = ['q', 's'];
        snap2.bonds.N = 3;
        snap2.angles.N = 4;
        snap2.dihedrals.N = 5;
        snap2.impropers.N = 6;
        snap2.constraints.N = 4;
        snap2.pairs.N = 7;

        gsd.hoomd.create(name=d+"/test_fallback.gsd");

        with gsd.fl.GSDFile(name=d+"/test_fallback.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            hf.extend([snap0, snap1, snap2]);

        with gsd.fl.GSDFile(name=d+"/test_fallback.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(len(hf), 3);
            s = hf.read_frame(0);

            eq_(s.configuration.step, snap0.configuration.step);
            eq_(s.configuration.dimensions, snap0.configuration.dimensions);
            numpy.testing.assert_array_equal(s.configuration.box, snap0.configuration.box);
            eq_(s.particles.N, snap0.particles.N);
            eq_(s.particles.types, snap0.particles.types);
            numpy.testing.assert_array_equal(s.particles.typeid, snap0.particles.typeid);
            numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass);
            numpy.testing.assert_array_equal(s.particles.diameter, snap0.particles.diameter);
            numpy.testing.assert_array_equal(s.particles.body, snap0.particles.body);
            numpy.testing.assert_array_equal(s.particles.charge, snap0.particles.charge);
            numpy.testing.assert_array_equal(s.particles.moment_inertia, snap0.particles.moment_inertia);
            numpy.testing.assert_array_equal(s.particles.position, snap0.particles.position);
            numpy.testing.assert_array_equal(s.particles.orientation, snap0.particles.orientation);
            numpy.testing.assert_array_equal(s.particles.velocity, snap0.particles.velocity);
            numpy.testing.assert_array_equal(s.particles.angmom, snap0.particles.angmom);
            numpy.testing.assert_array_equal(s.particles.image, snap0.particles.image);

            eq_(s.bonds.N, snap0.bonds.N);
            eq_(s.bonds.types, snap0.bonds.types);
            numpy.testing.assert_array_equal(s.bonds.typeid, snap0.bonds.typeid);
            numpy.testing.assert_array_equal(s.bonds.group, snap0.bonds.group);

            eq_(s.angles.N, snap0.angles.N);
            eq_(s.angles.types, snap0.angles.types);
            numpy.testing.assert_array_equal(s.angles.typeid, snap0.angles.typeid);
            numpy.testing.assert_array_equal(s.angles.group, snap0.angles.group);

            eq_(s.dihedrals.N, snap0.dihedrals.N);
            eq_(s.dihedrals.types, snap0.dihedrals.types);
            numpy.testing.assert_array_equal(s.dihedrals.typeid, snap0.dihedrals.typeid);
            numpy.testing.assert_array_equal(s.dihedrals.group, snap0.dihedrals.group);

            eq_(s.impropers.N, snap0.impropers.N);
            eq_(s.impropers.types, snap0.impropers.types);
            numpy.testing.assert_array_equal(s.impropers.typeid, snap0.impropers.typeid);
            numpy.testing.assert_array_equal(s.impropers.group, snap0.impropers.group);

            eq_(s.constraints.N, snap0.constraints.N);
            numpy.testing.assert_array_equal(s.constraints.value, snap0.constraints.value);
            numpy.testing.assert_array_equal(s.constraints.group, snap0.constraints.group);

            eq_(s.pairs.N, snap0.pairs.N);
            eq_(s.pairs.types, snap0.pairs.types);
            numpy.testing.assert_array_equal(s.pairs.typeid, snap0.pairs.typeid);
            numpy.testing.assert_array_equal(s.pairs.group, snap0.pairs.group);

            # test that everything but position remained the same in frame 1
            s = hf.read_frame(1);

            eq_(s.configuration.step, snap0.configuration.step);
            eq_(s.configuration.dimensions, snap0.configuration.dimensions);
            numpy.testing.assert_array_equal(s.configuration.box, snap0.configuration.box);
            eq_(s.particles.N, snap0.particles.N);
            eq_(s.particles.types, snap0.particles.types);
            numpy.testing.assert_array_equal(s.particles.typeid, snap0.particles.typeid);
            numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass);
            numpy.testing.assert_array_equal(s.particles.diameter, snap0.particles.diameter);
            numpy.testing.assert_array_equal(s.particles.body, snap0.particles.body);
            numpy.testing.assert_array_equal(s.particles.charge, snap0.particles.charge);
            numpy.testing.assert_array_equal(s.particles.moment_inertia, snap0.particles.moment_inertia);
            numpy.testing.assert_array_equal(s.particles.position, snap1.particles.position);
            numpy.testing.assert_array_equal(s.particles.orientation, snap0.particles.orientation);
            numpy.testing.assert_array_equal(s.particles.velocity, snap0.particles.velocity);
            numpy.testing.assert_array_equal(s.particles.angmom, snap0.particles.angmom);
            numpy.testing.assert_array_equal(s.particles.image, snap0.particles.image);

            eq_(s.bonds.N, snap0.bonds.N);
            eq_(s.bonds.types, snap0.bonds.types);
            numpy.testing.assert_array_equal(s.bonds.typeid, snap0.bonds.typeid);
            numpy.testing.assert_array_equal(s.bonds.group, snap0.bonds.group);

            eq_(s.angles.N, snap0.angles.N);
            eq_(s.angles.types, snap0.angles.types);
            numpy.testing.assert_array_equal(s.angles.typeid, snap0.angles.typeid);
            numpy.testing.assert_array_equal(s.angles.group, snap0.angles.group);

            eq_(s.dihedrals.N, snap0.dihedrals.N);
            eq_(s.dihedrals.types, snap0.dihedrals.types);
            numpy.testing.assert_array_equal(s.dihedrals.typeid, snap0.dihedrals.typeid);
            numpy.testing.assert_array_equal(s.dihedrals.group, snap0.dihedrals.group);

            eq_(s.impropers.N, snap0.impropers.N);
            eq_(s.impropers.types, snap0.impropers.types);
            numpy.testing.assert_array_equal(s.impropers.typeid, snap0.impropers.typeid);
            numpy.testing.assert_array_equal(s.impropers.group, snap0.impropers.group);

            eq_(s.constraints.N, snap0.constraints.N);
            numpy.testing.assert_array_equal(s.constraints.value, snap0.constraints.value);
            numpy.testing.assert_array_equal(s.constraints.group, snap0.constraints.group);

            eq_(s.pairs.N, snap0.pairs.N);
            eq_(s.pairs.types, snap0.pairs.types);
            numpy.testing.assert_array_equal(s.pairs.typeid, snap0.pairs.typeid);
            numpy.testing.assert_array_equal(s.pairs.group, snap0.pairs.group);

            # check that the third frame goes back to defaults because it has a different N
            s = hf.read_frame(2);

            eq_(s.particles.N, 3);
            eq_(s.particles.types, ['q', 's']);
            numpy.testing.assert_array_equal(s.particles.typeid, numpy.array([0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.particles.mass, numpy.array([1,1,1], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.diameter, numpy.array([1,1,1], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.body, numpy.array([-1,-1,-1], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.charge, numpy.array([0,0,0], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.moment_inertia, numpy.array([[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.position, numpy.array([[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.orientation, numpy.array([[1,0,0,0],[1,0,0,0],[1,0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.velocity, numpy.array([[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.angmom, numpy.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.particles.image, numpy.array([[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.int32));

            eq_(s.bonds.N, 3);
            eq_(s.bonds.types, snap0.bonds.types);
            numpy.testing.assert_array_equal(s.bonds.typeid, numpy.array([0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.bonds.group, numpy.array([[0,0],[0,0],[0,0]], dtype=numpy.uint32));

            eq_(s.angles.N, 4);
            eq_(s.angles.types, snap0.angles.types);
            numpy.testing.assert_array_equal(s.angles.typeid, numpy.array([0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.angles.group, numpy.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]], dtype=numpy.uint32));

            eq_(s.dihedrals.N, 5);
            eq_(s.dihedrals.types, snap0.dihedrals.types);
            numpy.testing.assert_array_equal(s.dihedrals.typeid, numpy.array([0,0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.dihedrals.group, numpy.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype=numpy.uint32));

            eq_(s.impropers.N, 6);
            eq_(s.impropers.types, snap0.impropers.types);
            numpy.testing.assert_array_equal(s.impropers.typeid, numpy.array([0,0,0,0,0,0], dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.impropers.group, numpy.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype=numpy.uint32));

            eq_(s.constraints.N, 4);
            numpy.testing.assert_array_equal(s.constraints.value, numpy.array([0,0,0,0], dtype=numpy.float32));
            numpy.testing.assert_array_equal(s.constraints.group, numpy.array([[0,0],[0,0],[0,0], [0,0]], dtype=numpy.uint32));

            eq_(s.pairs.N, 7);
            eq_(s.pairs.types, snap0.pairs.types);
            numpy.testing.assert_array_equal(s.pairs.typeid, numpy.array([0]*7, dtype=numpy.uint32));
            numpy.testing.assert_array_equal(s.pairs.group, numpy.array([[0,0]]*7, dtype=numpy.uint32));


def test_fallback2():
    with tempfile.TemporaryDirectory() as d:
        snap0 = gsd.hoomd.Snapshot();
        snap0.configuration.step = 1;
        snap0.configuration.dimensions = 3;
        snap0.particles.N = 2;
        snap0.particles.mass = [2,3];

        snap1 = gsd.hoomd.Snapshot();
        snap1.configuration.step = 2;
        snap1.particles.N = 2;
        snap1.particles.position = [[1,2,3],[4,5,6]];

        gsd.hoomd.create(name=d+"/test_fallback2.gsd");

        with gsd.fl.GSDFile(name=d+"/test_fallback2.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            hf.extend([snap0, snap1]);

        with gsd.fl.GSDFile(name=d+"/test_fallback2.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(len(hf), 2);

            s = hf.read_frame(1);
            numpy.testing.assert_array_equal(s.particles.mass, snap0.particles.mass);

def test_iteration():
    with tempfile.TemporaryDirectory() as d:

        with gsd.hoomd.open(name=d+"/test_iteration.gsd", mode='wb') as hf:
            hf.extend((create_frame(i) for i in range(20)));

        with gsd.hoomd.open(name=d+"/test_iteration.gsd", mode='rb') as hf:
            step = hf[-1].configuration.step;
            eq_(step, 20);

            step = hf[-2].configuration.step;
            eq_(step, 19);

            step = hf[-3].configuration.step;
            eq_(step, 18);

            step = hf[0].configuration.step;
            eq_(step, 1);

            step = hf[-20].configuration.step;
            eq_(step, 1);

            with assert_raises(IndexError) as cm:
                step = hf[-21].configuration.step;

            with assert_raises(IndexError) as cm:
                step = hf[20]

            snaps = hf[5:10];
            steps = [snap.configuration.step for snap in snaps];
            eq_(steps, [6,7,8,9,10]);

            snaps = hf[15:50];
            steps = [snap.configuration.step for snap in snaps];
            eq_(steps, [16,17,18,19,20]);

            snaps = hf[15:-3];
            steps = [snap.configuration.step for snap in snaps];
            eq_(steps, [16,17]);

def test_slicing_and_iteration():
    with tempfile.TemporaryDirectory() as d:

        with gsd.hoomd.open(name=d+"/test_slicing.gsd", mode='wb') as hf:
            hf.extend((create_frame(i) for i in range(20)));

        with gsd.hoomd.open(name=d+"/test_slicing.gsd", mode='rb') as hf:
            # Test len()-function on trajectory and sliced trajectory.
            eq_(len(hf), 20)
            eq_(len(hf[:10]), 10)

            # Test len()-function with explicit iterator.
            eq_(len(iter(hf)), len(hf))
            eq_(len(iter(hf[:10])), len(hf[:10]))

            # Test iteration with implicit iterator.
            # All iterations are run twice to check for issues
            # with iterator exhaustion.
            eq_(len(list(hf)), len(hf))
            eq_(len(list(hf)), len(hf))
            eq_(len(list(hf[:10])), len(hf[:10]))
            eq_(len(list(hf[:10])), len(hf[:10]))

            # Test iteration with explicit iterator.
            hf_iter = iter(hf)
            eq_(len(hf_iter), len(hf))  # sanity check
            eq_(len(list(hf_iter)), len(hf))
            eq_(len(list(hf_iter)), len(hf))

            # Test iteration with explicit sliced iterator.
            hf_iter = iter(hf[:10])
            eq_(len(hf_iter), 10)  # sanity check
            eq_(len(list(hf_iter)), 10)
            eq_(len(list(hf_iter)), 10)

            # Test frame selection
            with assert_raises(IndexError):
                hf[len(hf)]
            eq_(hf[0].configuration.step, hf[0].configuration.step)
            eq_(hf[len(hf) - 1].configuration.step, hf[-1].configuration.step)


def test_view_slicing_and_iteration():
    with tempfile.TemporaryDirectory() as d:

        with gsd.hoomd.open(name=d+"/test_slicing.gsd", mode='wb') as hf:
            hf.extend((create_frame(i) for i in range(40)));

        with gsd.hoomd.open(name=d+"/test_slicing.gsd", mode='rb') as hf:
            view = hf[::2]

            # Test len()-function on trajectory and sliced view.
            eq_(len(view), 20)
            eq_(len(view[:10]), 10)
            eq_(len(view[::2]), 10)

            # Test len()-function with explicit iterator.
            eq_(len(iter(view)), len(view))
            eq_(len(iter(view[:10])), len(view[:10]))

            # Test iteration with implicit iterator.
            # All iterations are run twice to check for issues
            # with iterator exhaustion.
            eq_(len(list(view)), len(view))
            eq_(len(list(view)), len(view))
            eq_(len(list(view[:10])), len(view[:10]))
            eq_(len(list(view[:10])), len(view[:10]))
            eq_(len(list(view[::2])), len(view[::2]))
            eq_(len(list(view[::2])), len(view[::2]))

            # Test iteration with explicit iterator.
            view_iter = iter(view)
            eq_(len(view_iter), len(view))  # sanity check
            eq_(len(list(view_iter)), len(view))
            eq_(len(list(view_iter)), len(view))

            # Test iteration with explicit sliced iterator.
            view_iter = iter(view[:10])
            eq_(len(view_iter), 10)  # sanity check
            eq_(len(list(view_iter)), 10)
            eq_(len(list(view_iter)), 10)

            # Test frame selection
            with assert_raises(IndexError):
                view[len(view)]
            eq_(view[0].configuration.step, view[0].configuration.step)
            eq_(view[len(view) - 1].configuration.step, view[-1].configuration.step)

def test_truncate():
    with tempfile.TemporaryDirectory() as d:
        gsd.hoomd.create(name=d+"/test_iteration.gsd");

        with gsd.fl.GSDFile(name=d+"/test_iteration.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            hf.extend((create_frame(i) for i in range(20)));

            eq_(len(hf), 20);
            s = hf[10];
            ok_(hf._initial_frame is not None);

            hf.truncate();
            eq_(len(hf), 0);
            ok_(hf._initial_frame is None);

def test_state():
    with tempfile.TemporaryDirectory() as d:
        snap0 = gsd.hoomd.Snapshot();

        snap0.state['hpmc/sphere/radius'] = [2.0]
        snap0.state['hpmc/sphere/orientable'] = [1]


        snap1 = gsd.hoomd.Snapshot();

        snap1.state['hpmc/convex_polyhedron/N'] = [3]
        snap1.state['hpmc/convex_polyhedron/vertices'] = [[-1, -1, -1],
                                                          [0, 1, 1],
                                                          [1, 0, 0]];

        gsd.hoomd.create(name=d+"/test_state.gsd");

        with gsd.fl.GSDFile(name=d+"/test_state.gsd", mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            hf.extend([snap0, snap1]);

        with gsd.fl.GSDFile(name=d+"/test_state.gsd", mode='rb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f);
            eq_(len(hf), 2);
            s = hf.read_frame(0);

            numpy.testing.assert_array_equal(s.state['hpmc/sphere/radius'], snap0.state['hpmc/sphere/radius']);
            numpy.testing.assert_array_equal(s.state['hpmc/sphere/orientable'], snap0.state['hpmc/sphere/orientable']);

            s = hf.read_frame(1);

            numpy.testing.assert_array_equal(s.state['hpmc/convex_polyhedron/N'], snap1.state['hpmc/convex_polyhedron/N']);
            numpy.testing.assert_array_equal(s.state['hpmc/convex_polyhedron/vertices'], snap1.state['hpmc/convex_polyhedron/vertices']);
