# Copyright (c) 2016 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.fl
import tempfile
import numpy
from nose.tools import eq_

def test_create():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+"/test_create.gsd", application="test_create", schema="none", schema_version=[1,2]);

def test_dtypes():
    for typ in [numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64, numpy.int8, numpy.int16, numpy.int32,
                numpy.int64, numpy.float32, numpy.float64]:
        yield check_dtype, typ

def check_dtype(typ):
    data = numpy.array([1,2,3,4,5,10012], dtype=typ);

    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+"/test_dtype.gsd", application="test_dtype", schema="none", schema_version=[1,2]);

        with gsd.fl.GSDFile(name=d+"/test_dtype.gsd", mode='w') as f:
            f.write_chunk(name='data', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+"/test_dtype.gsd", mode='r') as f:
            read_data = f.read_chunk(frame=0, name='data');

            eq_(data.dtype, read_data.dtype);
            numpy.testing.assert_array_equal(data, read_data);

