# GSD

GSD (General Simulation Data) is a file format specification and a library to read and write it. The package also
contains a python module that reads and writes [hoomd](https://glotzerlab.engin.umich.edu/hoomd-blue/) schema gsd
files with an easy to use syntax.

See the [full GSD documentation](http://gsd.readthedocs.io) at readthedocs.io.

## Overview

GSD files:

* Efficiently store many frames of data from simulation runs.
* High performance file read and write.
* Support arbitrary chunks of data in each frame (position, orientation, type, etc...).
* Append frames to an existing file with a monotonically increasing frame number.
* Resilient to job kills.
* Variable number of named chunks in each frame.
* Variable size of chunks in each frame.
* Each chunk identifies data type.
* Common use cases: NxM arrays in double, float, int, char types.
* Generic use case: binary blob of N bytes.
* Easy to integrate into other tools with python, or a C API (< 1k lines).
* Fast random access to frames.

## HOOMD examples

Create a hoomd gsd file.
```python
>>> s = gsd.hoomd.Snapshot()
>>> s.particles.N = 4
>>> s.particles.types = ['A', 'B']
>>> s.particles.typeid = [0,0,1,1]
>>> s.particles.position = [[0,0,0],[1,1,1], [-1,-1,-1], [1,-1,-1]]
>>> s.configuration.box = [3, 3, 3, 0, 0, 0]
>>> traj = gsd.hoomd.open(name='test.gsd', mode='wb')
>>> traj.append(s)
```

Append frames to a gsd file:
```python
>>> def create_frame(i):
...     s = gsd.hoomd.Snapshot();
...     s.configuration.step = i;
...     s.particles.N = 4+i;
...     s.particles.position = numpy.random.random(size=(4+i,3))
...     return s;
>>> with gsd.hoomd.open('test.gsd', 'ab') as t:
...     t.extend( (create_frame(i) for i in range(10)) )
...     print(len(t))
11
```

Randomly index frames:
```python
>>> with gsd.hoomd.open('test.gsd', 'rb') as t:
...     snap = t[5]
...     print(snap.configuration.step)
4
...     print(snap.particles.N)
8
...     print(snap.particles.position)
[[ 0.56993282  0.42243481  0.5502916 ]
 [ 0.36892486  0.38167036  0.27310368]
 [ 0.04739023  0.13603486  0.196539  ]
 [ 0.120232    0.91591144  0.99463677]
 [ 0.79806316  0.16991436  0.15228257]
 [ 0.13724308  0.14253527  0.02505   ]
 [ 0.39287439  0.82519054  0.01613089]
 [ 0.23150323  0.95167434  0.7715748 ]]
```

Slice frames:
```python
>>> with gsd.hoomd.open('test.gsd', 'rb') as t:
...     for s in t[5:-2]:
...         print(s.configuration.step, end=' ')
4 5 6 7
```

## File layer examples

```python
with gsd.fl.open(name='file.gsd', mode='wb') as f:
    f.write_chunk(name='position', data=numpy.array([[1,2,3],[4,5,6]], dtype=numpy.float32));
    f.write_chunk(name='angle', data=numpy.array([0, 1], dtype=numpy.float32));
    f.write_chunk(name='box', data=numpy.array([10, 10, 10], dtype=numpy.float32));
    f.end_frame()
```

```python
with gsd.fl.open(name='file.gsd', mode='rb') as f:
    for i in range(1,f.nframes):
        position = f.read_chunk(frame=i, name='position');
        do_something(position);
```
