# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.hoomd
import numpy
import pytest

@pytest.mark.parametrize("N", [2**26, 2**27, 179000000])
def test_large_N(tmp_path, N):
    s = gsd.hoomd.Snapshot()
    s.particles.N = int(N)
    s.particles.position = numpy.zeros([N,3]);
    s.particles.position[:,0] = numpy.linspace(0, 1, num=N, endpoint=False, dtype=numpy.float32)
    s.particles.position[:,1] = numpy.linspace(1, 2, num=N, endpoint=False, dtype=numpy.float32)
    s.particles.position[:,2] = numpy.linspace(2, 3, num=N, endpoint=False, dtype=numpy.float32)

    with gsd.hoomd.open(name=tmp_path / "test_large_N.gsd",mode="wb") as f:
        f.append(s)

    with gsd.hoomd.open(name=tmp_path / "test_large_N.gsd",mode="rb") as f:
        numpy.testing.assert_array_equal(f[0].particles.position, s.particles.position)
