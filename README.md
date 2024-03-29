# GSD

The **GSD** file format is the native file format for [HOOMD-blue](https://glotzerlab.engin.umich.edu/hoomd-blue/).
**GSD** files store trajectories of the **HOOMD-blue** system state in a binary file with efficient random access to
frames. **GSD** allows all particle and topology properties to vary from one frame to the next. Use the **GSD** Python
API to specify the initial condition for a **HOOMD-blue** simulation or analyze trajectory output with a script. Read a
**GSD** trajectory with a visualization tool to explore the behavior of the simulation.

## Resources

* [GSD documentation](http://gsd.readthedocs.io): Tutorials, Python API, C API, usage information, and format
  specification.
* [Installation Guide](INSTALLING.rst): Instructions for installing and compiling **GSD**.
* [HOOMD-blue](https://glotzerlab.engin.umich.edu/hoomd-blue/): Simulation engine that reads and writes **GSD** files.
* [GSD discussion board](https://github.com/glotzerlab/gsd/discussions/):
  Ask the **GSD** community for help.
* [freud](https://freud.readthedocs.io): A powerful set of tools for analyzing trajectories.
* [OVITO](https://www.ovito.org/): The Open Visualization Tool works with **GSD** files.
* [gsd-vmd plugin](https://github.com/mphoward/gsd-vmd): VMD plugin to support **GSD** files.

## HOOMD examples

Create a hoomd gsd file.
```python
>>> s = gsd.hoomd.Frame()
>>> s.particles.N = 4
>>> s.particles.types = ['A', 'B']
>>> s.particles.typeid = [0,0,1,1]
>>> s.particles.position = [[0,0,0],[1,1,1], [-1,-1,-1], [1,-1,-1]]
>>> s.configuration.box = [3, 3, 3, 0, 0, 0]
>>> traj = gsd.hoomd.open(name='test.gsd', mode='w')
>>> traj.append(s)
```

Append frames to a gsd file:
```python
>>> def create_frame(i):
...     s = gsd.hoomd.Frame();
...     s.configuration.step = i;
...     s.particles.N = 4+i;
...     s.particles.position = numpy.random.random(size=(4+i,3))
...     return s;
>>> with gsd.hoomd.open('test.gsd', 'a') as t:
...     t.extend( (create_frame(i) for i in range(10)) )
...     print(len(t))
11
```

Randomly index frames:
```python
>>> with gsd.hoomd.open('test.gsd', 'r') as t:
...     frame = t[5]
...     print(frame.configuration.step)
4
...     print(frame.particles.N)
8
...     print(frame.particles.position)
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
>>> with gsd.hoomd.open('test.gsd', 'r') as t:
...     for s in t[5:-2]:
...         print(s.configuration.step, end=' ')
4 5 6 7
```

## File layer examples

```python
with gsd.fl.open(name='file.gsd', mode='w') as f:
    f.write_chunk(name='position', data=numpy.array([[1,2,3],[4,5,6]], dtype=numpy.float32));
    f.write_chunk(name='angle', data=numpy.array([0, 1], dtype=numpy.float32));
    f.write_chunk(name='box', data=numpy.array([10, 10, 10], dtype=numpy.float32));
    f.end_frame()
```

```python
with gsd.fl.open(name='file.gsd', mode='r') as f:
    for i in range(1,f.nframes):
        position = f.read_chunk(frame=i, name='position');
        do_something(position);
```
