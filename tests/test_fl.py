# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.fl
import gsd.pygsd
import tempfile
import numpy
import platform
from nose.tools import ok_, eq_, assert_raises

def test_create():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+"/test_create.gsd", application="test_create", schema="none", schema_version=[1,2]);

def test_dtypes():
    for typ in [numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64, numpy.int8, numpy.int16, numpy.int32,
                numpy.int64, numpy.float32, numpy.float64]:
        yield check_dtype, typ

def check_dtype(typ):
    data1d = numpy.array([1,2,3,4,5,10012], dtype=typ);
    data2d = numpy.array([[10,20],[30,40],[50,80]], dtype=typ);

    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+"/test_dtype.gsd", application="test_dtype", schema="none", schema_version=[1,2]);

        with gsd.fl.GSDFile(name=d+"/test_dtype.gsd", mode='wb') as f:
            f.write_chunk(name='data1d', data=data1d);
            f.write_chunk(name='data2d', data=data2d);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+"/test_dtype.gsd", mode='rb') as f:
            read_data1d = f.read_chunk(frame=0, name='data1d');
            read_data2d = f.read_chunk(frame=0, name='data2d');

            eq_(data1d.dtype, read_data1d.dtype);
            numpy.testing.assert_array_equal(data1d, read_data1d);
            eq_(data2d.dtype, read_data2d.dtype);
            numpy.testing.assert_array_equal(data2d, read_data2d);

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+"/test_dtype.gsd", mode='rb')) as f:
            read_data1d = f.read_chunk(frame=0, name='data1d');
            read_data2d = f.read_chunk(frame=0, name='data2d');

            eq_(data1d.dtype, read_data1d.dtype);
            numpy.testing.assert_array_equal(data1d, read_data1d);
            eq_(data2d.dtype, read_data2d.dtype);
            numpy.testing.assert_array_equal(data2d, read_data2d);

def test_metadata():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_metadata.gsd', application='test_metadata', schema='none', schema_version=[1,2]);

        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);

        with gsd.fl.GSDFile(name=d+'/test_metadata.gsd', mode='wb') as f:
            eq_(f.mode, 'wb');
            for i in range(150):
                f.write_chunk(name='data', data=data);
                f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_metadata.gsd', mode='rb') as f:
            eq_(f.name, d+'/test_metadata.gsd');
            eq_(f.mode, 'rb');
            eq_(f.application, 'test_metadata');
            eq_(f.schema, 'none');
            eq_(f.schema_version, (1,2));
            eq_(f.nframes, 150);
            ok_(f.gsd_version == (1,0));

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+'/test_metadata.gsd', mode='rb')) as f:
            eq_(f.name, d+'/test_metadata.gsd');
            eq_(f.mode, 'rb');
            eq_(f.application, 'test_metadata');
            eq_(f.schema, 'none');
            eq_(f.schema_version, (1,2));
            eq_(f.nframes, 150);
            ok_(f.gsd_version == (1,0));

def test_append():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_append.gsd', application='test_append', schema='none', schema_version=[1,2]);

        data = numpy.array([10], dtype=numpy.int64);
        nframes = 257;

        with gsd.fl.GSDFile(name=d+'/test_append.gsd', mode='ab') as f:
            eq_(f.mode, 'ab');
            for i in range(nframes):
                data[0] = i;
                f.write_chunk(name='data1', data=data);
                data[0] = i*10
                f.write_chunk(name='data10', data=data);
                f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_append.gsd', mode='rb') as f:
            eq_(f.nframes, nframes);
            for i in range(nframes):
                data1 = f.read_chunk(frame=i, name='data1');
                data10 = f.read_chunk(frame=i, name='data10');
                eq_(data1[0], i);
                eq_(data10[0], i*10);

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+'/test_append.gsd', mode='rb')) as f:
            eq_(f.nframes, nframes);
            for i in range(nframes):
                data1 = f.read_chunk(frame=i, name='data1');
                data10 = f.read_chunk(frame=i, name='data10');
                eq_(data1[0], i);
                eq_(data10[0], i*10);

def test_chunk_exists():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_chunk_exists.gsd', application='test_chunk_exists', schema='none', schema_version=[1,2]);

        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
        with gsd.fl.GSDFile(name=d+'/test_chunk_exists.gsd', mode='wb') as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();
            f.write_chunk(name='abcdefg', data=data);
            f.end_frame();
            f.write_chunk(name='test', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_chunk_exists.gsd', mode='rb') as f:
            ok_(f.chunk_exists(frame=0, name='chunk1'));
            read_data = f.read_chunk(frame=0, name='chunk1');
            ok_(f.chunk_exists(frame=1, name='abcdefg'));
            read_data = f.read_chunk(frame=1, name='abcdefg');
            ok_(f.chunk_exists(frame=2, name='test'));
            read_data = f.read_chunk(frame=2, name='test');

            ok_(not f.chunk_exists(frame=1, name='chunk1'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=1, name='chunk1');
            ok_(not f.chunk_exists(frame=2, name='abcdefg'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=2, name='abcdefg');
            ok_(not f.chunk_exists(frame=0, name='test'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=0, name='test');

            ok_(not f.chunk_exists(frame=2, name='chunk1'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=2, name='chunk1');
            ok_(not f.chunk_exists(frame=0, name='abcdefg'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=0, name='abcdefg');
            ok_(not f.chunk_exists(frame=1, name='test'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=1, name='test');

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+'/test_chunk_exists.gsd', mode='rb')) as f:
            ok_(f.chunk_exists(frame=0, name='chunk1'));
            read_data = f.read_chunk(frame=0, name='chunk1');
            ok_(f.chunk_exists(frame=1, name='abcdefg'));
            read_data = f.read_chunk(frame=1, name='abcdefg');
            ok_(f.chunk_exists(frame=2, name='test'));
            read_data = f.read_chunk(frame=2, name='test');

            ok_(not f.chunk_exists(frame=1, name='chunk1'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=1, name='chunk1');
            ok_(not f.chunk_exists(frame=2, name='abcdefg'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=2, name='abcdefg');
            ok_(not f.chunk_exists(frame=0, name='test'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=0, name='test');

            ok_(not f.chunk_exists(frame=2, name='chunk1'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=2, name='chunk1');
            ok_(not f.chunk_exists(frame=0, name='abcdefg'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=0, name='abcdefg');
            ok_(not f.chunk_exists(frame=1, name='test'));
            with assert_raises(Exception) as cm:
                read_data = f.read_chunk(frame=1, name='test');

def test_readonly_errors():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_readonly_errors.gsd', application='test_readonly_errors', schema='none', schema_version=[1,2]);

        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
        with gsd.fl.GSDFile(name=d+'/test_readonly_errors.gsd', mode='wb') as f:
            for i in range(10):
                f.write_chunk(name='chunk1', data=data);
                f.end_frame();

        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
        with gsd.fl.GSDFile(name=d+'/test_readonly_errors.gsd', mode='rb') as f:
            with assert_raises(Exception) as cm:
                f.end_frame();

            with assert_raises(Exception) as cm:
                f.write_chunk(name='chunk1', data=data);

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+'/test_readonly_errors.gsd', mode='rb')) as f:
            with assert_raises(Exception) as cm:
                f.end_frame();

            with assert_raises(Exception) as cm:
                f.write_chunk(name='chunk1', data=data);


def test_fileio_errors():
    # These test cause python to crash on windows....
    if platform.system() != "Windows":
        with assert_raises(Exception) as cm:
            gsd.fl.create(name='/this/file/does/not/exist', application='test_readonly_errors', schema='none', schema_version=[1,2]);

        with tempfile.TemporaryDirectory() as d:
            with open(d+'/test_fileio_errors.gsd', 'wb') as f:
                f.write(b'test');

            with assert_raises(RuntimeError) as cm:
                f = gsd.fl.GSDFile(name=d+'/test_fileio_errors.gsd', mode='rb');

def test_dtype_errors():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_dtype_errors.gsd', application='test_dtype_errors', schema='none', schema_version=[1,2]);

        with assert_raises(Exception) as cm:
            data = numpy.array([1,2,3,4,5,10012], dtype=numpy.bool_);

            with gsd.fl.GSDFile(name=d+'/test_dtype_errors.gsd', mode='wb') as f:
                f.write_chunk(name='chunk1', data=data);
                f.end_frame();

        with assert_raises(Exception) as cm:
            data = numpy.array([1,2,3,4,5,10012], dtype=numpy.float16);

            with gsd.fl.GSDFile(name=d+'/test_dtype_errors.gsd', mode='wb') as f:
                f.write_chunk(name='chunk1', data=data);
                f.end_frame();

        with assert_raises(Exception) as cm:
            data = numpy.array([1,2,3,4,5,10012], dtype=numpy.complex64);

            with gsd.fl.GSDFile(name=d+'/test_dtype_errors.gsd', mode='wb') as f:
                f.write_chunk(name='chunk1', data=data);
                f.end_frame();

        with assert_raises(Exception) as cm:
            data = numpy.array([1,2,3,4,5,10012], dtype=numpy.complex128);

            with gsd.fl.GSDFile(name=d+'/test_dtype_errors.gsd', mode='wb') as f:
                f.write_chunk(name='chunk1', data=data);
                f.end_frame();

def test_truncate():
    with tempfile.TemporaryDirectory() as d:
        gsd.fl.create(name=d+'/test_truncate.gsd', application='test_truncate', schema='none', schema_version=[1,2]);

        data = numpy.ascontiguousarray(numpy.random.random(size=(1000,3)), dtype=numpy.float32);
        with gsd.fl.GSDFile(name=d+'/test_truncate.gsd', mode='wb') as f:
            eq_(f.mode, 'wb');
            for i in range(10):
                f.write_chunk(name='data', data=data);
                f.end_frame();

            eq_(f.nframes, 10);

            f.truncate();
            eq_(f.nframes, 0);
            eq_(f.application, 'test_truncate');
            eq_(f.schema, 'none');
            eq_(f.schema_version, (1,2));

            f.write_chunk(name='data', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_truncate.gsd', mode='rb') as f:
            eq_(f.name, d+'/test_truncate.gsd');
            eq_(f.mode, 'rb');
            eq_(f.application, 'test_truncate');
            eq_(f.schema, 'none');
            eq_(f.schema_version, (1,2));
            eq_(f.nframes, 1);

def test_namelen():
    with tempfile.TemporaryDirectory() as d:
        app_long = 'abcdefga'*100;
        schema_long = 'ijklmnop'*100;
        chunk_long = '12345678'*100;
        gsd.fl.create(name=d+'/test_namelen.gsd', application=app_long, schema=schema_long, schema_version=[1,2]);

        with gsd.fl.GSDFile(name=d+'/test_namelen.gsd', mode='wb') as f:
            eq_(f.application, app_long[0:63])
            eq_(f.schema, schema_long[0:63])

            data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
            f.write_chunk(name=chunk_long, data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_namelen.gsd', mode='rb') as f:
            data_read = f.read_chunk(0, name=chunk_long[0:63]);
            numpy.testing.assert_array_equal(data, data_read);

        # test again with pygsd
        with gsd.pygsd.GSDFile(file=open(d+'/test_namelen.gsd', mode='rb')) as f:
            data_read = f.read_chunk(0, name=chunk_long[0:63]);
            numpy.testing.assert_array_equal(data, data_read);

def test_open():
    with tempfile.TemporaryDirectory() as d:
        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='xb', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test_2.gsd', mode='xb+', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();
            f.read_chunk(0, name='chunk1');

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='wb', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='wb+', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();
            f.read_chunk(0, name='chunk1');

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='ab', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='rb', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.read_chunk(0, name='chunk1');
            f.read_chunk(1, name='chunk1');

        with gsd.fl.GSDFile(name=d+'/test.gsd', mode='rb+', application='test_open', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();
            f.read_chunk(0, name='chunk1');
            f.read_chunk(1, name='chunk1');
            f.read_chunk(2, name='chunk1');
