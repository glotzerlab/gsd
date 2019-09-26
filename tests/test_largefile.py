# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.hoomd
import numpy
import pytest

@pytest.mark.parametrize("N", [2**26, 2**27, 179000000])
def test_large_N(tmp_path, N):
    s = gsd.hoomd.Snapshot()
    s.particles.N = int(N)
    s.particles.position = a = numpy.linspace([0, 1, 2], [0+N, 1+N, 2+N], num=N, endpoint=False, dtype=numpy.float32)

    with gsd.hoomd.open(name=tmp_path / "test_large_N.gsd",mode="wb") as f:
        f.append(s)

    with gsd.hoomd.open(name=tmp_path / "test_large_N.gsd",mode="rb") as f:
        numpy.testing.assert_array_equal(f[0].particles.position, s.particles.position)
