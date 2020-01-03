import time
import gsd.fl
import gsd.pygsd
import gsd.hoomd
import os
import math
import random
import numpy
import sys
from subprocess import call, PIPE


def read_frame(file, frame, read_keys):
    for key in read_keys:
        file.read_chunk(frame=frame, name=key)


def read_sequential_file(file, read_keys, nframes_read):
    for i in range(1, nframes_read):
        read_frame(file, i, read_keys)


def read_random_file(file, read_keys, nframes_read):
    frames = list(range(0, nframes_read))
    random.shuffle(frames)

    for i, f in enumerate(frames[:]):
        read_frame(file, f, read_keys)

def read_file(read_keys):
    """ Run all benchmarks with the given options
    """

    start = time.time()
    with gsd.fl.open(name='test.gsd', mode='rb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
        end = time.time()

        print("Open time:", (end - start)/1e-3, "ms")

        nframes_read = min(f.nframes, 100)

        # Read the file sequentially and measure the time taken
        start = time.time()
        read_sequential_file(f, read_keys, nframes_read)
        end = time.time()

        print("Sequential read time:", (end - start)/1e-6/nframes_read/len(read_keys), "us / key")

        # # drop the file system cache
        call(['sudo', '/bin/sync'])
        call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

        # Read the file randomly and measure the time taken
        start = time.time()
        read_random_file(f, read_keys, nframes_read)
        end = time.time()

        print("Random read time:", (end - start)/1e-6/nframes_read/len(read_keys), "us / key")

if __name__ == '__main__':
    names = [str(i) for i in range(1000)]

    read_file(names)
