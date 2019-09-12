# Copyright (c) 2016-2019 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

import gsd.fl
import gsd.pygsd
import numpy
import platform
import pytest

def test_create(tmp_path):
    gsd.fl.create(name=tmp_path / "test_create.gsd", application="test_create", schema="none", schema_version=[1,2]);

@pytest.mark.parametrize('typ', [numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64, numpy.int8, numpy.int16,
                                 numpy.int32, numpy.int64, numpy.float32, numpy.float64])
def test_dtype(tmp_path, typ):
    data1d = numpy.array([1,2,3,4,5,10012], dtype=typ);
    data2d = numpy.array([[10,20],[30,40],[50,80]], dtype=typ);

    gsd.fl.create(name=tmp_path / "test_dtype.gsd", application="test_dtype", schema="none", schema_version=[1,2]);

    with gsd.fl.open(name=tmp_path / "test_dtype.gsd", mode='wb', application="test_dtype", schema="none", schema_version=[1,2]) as f:
        f.write_chunk(name='data1d', data=data1d);
        f.write_chunk(name='data2d', data=data2d);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / "test_dtype.gsd", mode='rb', application="test_dtype", schema="none", schema_version=[1,2]) as f:
        read_data1d = f.read_chunk(frame=0, name='data1d');
        read_data2d = f.read_chunk(frame=0, name='data2d');

        assert data1d.dtype == read_data1d.dtype;
        numpy.testing.assert_array_equal(data1d, read_data1d);
        assert data2d.dtype == read_data2d.dtype;
        numpy.testing.assert_array_equal(data2d, read_data2d);

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / "test_dtype.gsd"), mode='rb')) as f:
        read_data1d = f.read_chunk(frame=0, name='data1d');
        read_data2d = f.read_chunk(frame=0, name='data2d');

        assert data1d.dtype == read_data1d.dtype;
        numpy.testing.assert_array_equal(data1d, read_data1d);
        assert data2d.dtype == read_data2d.dtype;
        numpy.testing.assert_array_equal(data2d, read_data2d);

def test_metadata(tmp_path):
    data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);

    with gsd.fl.open(name=tmp_path / 'test_metadata.gsd', mode='wb', application='test_metadata', schema='none', schema_version=[1,2]) as f:
        assert f.mode == 'wb';
        for i in range(150):
            f.write_chunk(name='data', data=data);
            f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_metadata.gsd', mode='rb', application='test_metadata', schema='none', schema_version=[1,2]) as f:
        assert f.name == str(tmp_path / 'test_metadata.gsd');
        assert f.mode == 'rb';
        assert f.application == 'test_metadata';
        assert f.schema == 'none';
        assert f.schema_version == (1,2);
        assert f.nframes == 150;
        assert f.gsd_version == (1,0);

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / 'test_metadata.gsd'), mode='rb')) as f:
        assert f.name == str(tmp_path / 'test_metadata.gsd');
        assert f.mode == 'rb';
        assert f.application == 'test_metadata';
        assert f.schema == 'none';
        assert f.schema_version == (1,2);
        assert f.nframes == 150;
        assert f.gsd_version == (1,0);

def test_append(tmp_path):
    with gsd.fl.open(name=tmp_path / 'test_append.gsd', mode='wb', application='test_append', schema='none', schema_version=[1,2]):
        pass

    data = numpy.array([10], dtype=numpy.int64);
    nframes = 257;

    with gsd.fl.open(name=tmp_path / 'test_append.gsd', mode='ab', application='test_append', schema='none', schema_version=[1,2]) as f:
        assert f.mode == 'ab';
        for i in range(nframes):
            data[0] = i;
            f.write_chunk(name='data1', data=data);
            data[0] = i*10
            f.write_chunk(name='data10', data=data);
            f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_append.gsd', mode='rb', application='test_append', schema='none', schema_version=[1,2]) as f:
        assert f.nframes == nframes;
        for i in range(nframes):
            data1 = f.read_chunk(frame=i, name='data1');
            data10 = f.read_chunk(frame=i, name='data10');
            assert data1[0] == i;
            assert data10[0] == i*10;

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / 'test_append.gsd'), mode='rb')) as f:
        assert f.nframes == nframes;
        for i in range(nframes):
            data1 = f.read_chunk(frame=i, name='data1');
            data10 = f.read_chunk(frame=i, name='data10');
            assert data1[0] == i;
            assert data10[0] == i*10;

def test_chunk_exists(tmp_path):
    data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
    with gsd.fl.open(name=tmp_path / 'test_chunk_exists.gsd', mode='wb', application='test_chunk_exists', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();
        f.write_chunk(name='abcdefg', data=data);
        f.end_frame();
        f.write_chunk(name='test', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_chunk_exists.gsd', mode='rb', application='test_chunk_exists', schema='none', schema_version=[1,2]) as f:
        assert f.chunk_exists(frame=0, name='chunk1');
        read_data = f.read_chunk(frame=0, name='chunk1');
        assert f.chunk_exists(frame=1, name='abcdefg');
        read_data = f.read_chunk(frame=1, name='abcdefg');
        assert f.chunk_exists(frame=2, name='test');
        read_data = f.read_chunk(frame=2, name='test');

        assert not f.chunk_exists(frame=1, name='chunk1');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=1, name='chunk1');
        assert not f.chunk_exists(frame=2, name='abcdefg');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=2, name='abcdefg');
        assert not f.chunk_exists(frame=0, name='test');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=0, name='test');

        assert not f.chunk_exists(frame=2, name='chunk1');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=2, name='chunk1');
        assert not f.chunk_exists(frame=0, name='abcdefg');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=0, name='abcdefg');
        assert not f.chunk_exists(frame=1, name='test');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=1, name='test');

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / 'test_chunk_exists.gsd'), mode='rb')) as f:
        assert f.chunk_exists(frame=0, name='chunk1');
        read_data = f.read_chunk(frame=0, name='chunk1');
        assert f.chunk_exists(frame=1, name='abcdefg');
        read_data = f.read_chunk(frame=1, name='abcdefg');
        assert f.chunk_exists(frame=2, name='test');
        read_data = f.read_chunk(frame=2, name='test');

        assert not f.chunk_exists(frame=1, name='chunk1');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=1, name='chunk1');
        assert not f.chunk_exists(frame=2, name='abcdefg');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=2, name='abcdefg');
        assert not f.chunk_exists(frame=0, name='test');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=0, name='test');

        assert not f.chunk_exists(frame=2, name='chunk1');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=2, name='chunk1');
        assert not f.chunk_exists(frame=0, name='abcdefg');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=0, name='abcdefg');
        assert not f.chunk_exists(frame=1, name='test');
        with pytest.raises(Exception) as cm:
            read_data = f.read_chunk(frame=1, name='test');

def test_readonly_errors(tmp_path):
    data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
    with gsd.fl.open(name=tmp_path / 'test_readonly_errors.gsd', mode='wb', application='test_readonly_errors', schema='none', schema_version=[1,2]) as f:
        for i in range(10):
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

    data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
    with gsd.fl.open(name=tmp_path / 'test_readonly_errors.gsd', mode='rb', application='test_readonly_errors', schema='none', schema_version=[1,2]) as f:
        with pytest.raises(Exception) as cm:
            f.end_frame();

        with pytest.raises(Exception) as cm:
            f.write_chunk(name='chunk1', data=data);

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / 'test_readonly_errors.gsd'), mode='rb')) as f:
        with pytest.raises(Exception) as cm:
            f.end_frame();

        with pytest.raises(Exception) as cm:
            f.write_chunk(name='chunk1', data=data);


def test_fileio_errors(tmp_path):
    # These test cause python to crash on windows....
    if platform.system() != "Windows":
        with pytest.raises(Exception) as cm:
            gsd.fl.open(name='/this/file/does/not/exist', application='test_readonly_errors', schema='none', schema_version=[1,2]);

        with open(str(tmp_path / 'test_fileio_errors.gsd'), 'wb') as f:
            f.write(b'test');

        with pytest.raises(RuntimeError) as cm:
            f = gsd.fl.open(name=tmp_path / 'test_fileio_errors.gsd', mode='rb', application='test_readonly_errors', schema='none', schema_version=[1,2]);

def test_dtype_errors(tmp_path):
    with pytest.raises(Exception) as cm:
        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.bool_);

        with gsd.fl.open(name=tmp_path / 'test_dtype_errors.gsd', mode='wb', application='test_dtype_errors', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

    with pytest.raises(Exception) as cm:
        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.float16);

        with gsd.fl.open(name=tmp_path / 'test_dtype_errors.gsd', mode='wb', application='test_dtype_errors', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

    with pytest.raises(Exception) as cm:
        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.complex64);

        with gsd.fl.open(name=tmp_path / 'test_dtype_errors.gsd', mode='wb', application='test_dtype_errors', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

    with pytest.raises(Exception) as cm:
        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.complex128);

        with gsd.fl.open(name=tmp_path / 'test_dtype_errors.gsd', mode='wb', application='test_dtype_errors', schema='none', schema_version=[1,2]) as f:
            f.write_chunk(name='chunk1', data=data);
            f.end_frame();

def test_truncate(tmp_path):
    data = numpy.ascontiguousarray(numpy.random.random(size=(1000,3)), dtype=numpy.float32);
    with gsd.fl.open(name=tmp_path / 'test_truncate.gsd', mode='wb', application='test_truncate', schema='none', schema_version=[1,2]) as f:
        assert f.mode == 'wb';
        for i in range(10):
            f.write_chunk(name='data', data=data);
            f.end_frame();

        assert f.nframes == 10;

        f.truncate();
        assert f.nframes == 0;
        assert f.application == 'test_truncate';
        assert f.schema == 'none';
        assert f.schema_version == (1,2);

        f.write_chunk(name='data', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_truncate.gsd', mode='rb', application='test_truncate', schema='none', schema_version=[1,2]) as f:
        assert f.name == str(tmp_path / 'test_truncate.gsd');
        assert f.mode == 'rb';
        assert f.application == 'test_truncate';
        assert f.schema == 'none';
        assert f.schema_version == (1,2);
        assert f.nframes == 1;

def test_namelen(tmp_path):
    app_long = 'abcdefga'*100;
    schema_long = 'ijklmnop'*100;
    chunk_long = '12345678'*100;

    with gsd.fl.open(name=tmp_path / 'test_namelen.gsd', mode='wb', application=app_long, schema=schema_long, schema_version=[1,2]) as f:
        assert f.application == app_long[0:63]
        assert f.schema == schema_long[0:63]

        data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);
        f.write_chunk(name=chunk_long, data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_namelen.gsd', mode='rb', application=app_long, schema=schema_long, schema_version=[1,2]) as f:
        data_read = f.read_chunk(0, name=chunk_long[0:63]);
        numpy.testing.assert_array_equal(data, data_read);

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / 'test_namelen.gsd'), mode='rb')) as f:
        data_read = f.read_chunk(0, name=chunk_long[0:63]);
        numpy.testing.assert_array_equal(data, data_read);

def test_open(tmp_path):
    data = numpy.array([1,2,3,4,5,10012], dtype=numpy.int64);

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='xb', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test_2.gsd', mode='xb+', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();
        f.read_chunk(0, name='chunk1');

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='wb', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='wb+', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();
        f.read_chunk(0, name='chunk1');

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='ab', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='rb', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.read_chunk(0, name='chunk1');
        f.read_chunk(1, name='chunk1');

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='rb+', application='test_open', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='chunk1', data=data);
        f.end_frame();
        f.read_chunk(0, name='chunk1');
        f.read_chunk(1, name='chunk1');
        f.read_chunk(2, name='chunk1');

def test_find_matching_chunk_names(tmp_path):
    data = numpy.array([1,2,3,4,5], dtype=numpy.float32);

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='xb', application='test_find_matching_chunk_names', schema='none', schema_version=[1,2]) as f:
        f.write_chunk(name='log/A', data=data);
        f.write_chunk(name='log/chunk2', data=data);
        f.end_frame();
        f.write_chunk(name='data/B', data=data);
        f.end_frame();

    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='rb', application='test_find_matching_chunk_names', schema='none', schema_version=[1,2]) as f:
        all_chunks = f.find_matching_chunk_names('');
        assert len(all_chunks) == 3;
        assert 'log/A' in all_chunks;
        assert 'log/chunk2' in all_chunks;
        assert 'data/B' in all_chunks;

        log_chunks = f.find_matching_chunk_names('log/');
        assert len(log_chunks) == 2;
        assert 'log/A' in log_chunks;
        assert 'log/chunk2' in log_chunks;

        data_chunks = f.find_matching_chunk_names('data/');
        assert len(data_chunks) == 1;
        assert 'data/B' in data_chunks;

        other_chunks = f.find_matching_chunk_names('other/');
        assert len(other_chunks) == 0;

    # test again with pygsd
    with gsd.pygsd.GSDFile(file=open(str(tmp_path / "test.gsd"), mode='rb')) as f:
        all_chunks = f.find_matching_chunk_names('');
        assert len(all_chunks) == 3;
        assert 'log/A' in all_chunks;
        assert 'log/chunk2' in all_chunks;
        assert 'data/B' in all_chunks;

        log_chunks = f.find_matching_chunk_names('log/');
        assert len(log_chunks) == 2;
        assert 'log/A' in log_chunks;
        assert 'log/chunk2' in log_chunks;

        data_chunks = f.find_matching_chunk_names('data/');
        assert len(data_chunks) == 1;
        assert 'data/B' in data_chunks;

        other_chunks = f.find_matching_chunk_names('other/');
        assert len(other_chunks) == 0;

def test_chunk_name_limit(tmp_path):
    with gsd.fl.open(name=tmp_path / 'test.gsd', mode='xb', application='test_chunk_name_limit', schema='none', schema_version=[1,2]) as f:
        for i in range(128):
            f.write_chunk(name=str(i), data=numpy.array([i], dtype=numpy.int32))

        # A bug in GSD limits files to 128 chunk names:
        # see https://github.com/glotzerlab/gsd/issues/43
        with pytest.raises(Exception) as cm:
            f.write_chunk(name='128', data=numpy.array([i], dtype=numpy.int32))
