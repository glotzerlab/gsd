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


def write_frame(file, frame, write_keys, data):
    for key in write_keys:
        file.write_chunk(name=key, data=data)
    file.end_frame()


def write_file(file, nframes, N, write_keys):
    data = numpy.random.random(N)
    for i in range(0, nframes):
        write_frame(file, i, write_keys, data)


def compute_nframes(N, size, write_keys):
    bytes_per_frame = (32 + 8 * N) * len(write_keys)
    return int(math.ceil(size / bytes_per_frame))


def create_file(N, size, write_keys):
    """ Create the output file
    """

    # size of data to read in benchmarks
    bmark_read_size = 0.25 * 1024**3

    timings = {}

    nframes = compute_nframes(N, size, write_keys)
    print(f'Writing {nframes} frames with {len(write_keys)} keys per frame')

    # write the file and time how long it takes
    with gsd.fl.open(name='test.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
        start = time.time()
        write_file(f, nframes, N, write_keys)

    # ensure that all writes to disk are completed and drop file system cache
    # call(['sudo', '/bin/sync'])

    end = time.time()

    call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

    print((end-start)/1e-6 / nframes / len(write_keys), "us per key")

if __name__ == '__main__':
    names = [str(i) for i in range(65534)]

    create_file(1, 4*1024**3, names)
