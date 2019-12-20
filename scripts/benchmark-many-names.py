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


def read_frame(file, frame, read_keys):
    for key in read_keys:
        file.read_chunk(frame=frame, name=key)


def write_file(file, nframes, N, write_keys):
    data = numpy.random.random(N)
    for i in range(0, nframes):
        write_frame(file, i, write_keys, data)


def read_sequential_file(file, nframes, nframes_read, read_keys):
    for i in range(0, nframes_read):
        read_frame(file, i, read_keys)


def read_random_file(file, nframes, nframes_read, read_keys):
    frames = list(range(0, nframes))
    random.shuffle(frames)

    for i, f in enumerate(frames[:nframes_read]):
        read_frame(file, f, read_keys)


def compute_nframes(N, size, write_keys):
    bytes_per_frame = (32 + 8 * N) * len(write_keys)
    return int(math.ceil(size / bytes_per_frame))


def compute_actual_size(N, nframes, write_keys):
    bytes_per_frame = (32 + 8 * N) * len(write_keys)
    return nframes * bytes_per_frame


def run_benchmarks(N, size, read_keys, write_keys):
    """ Run all benchmarks with the given options
    """

    # size of data to read in benchmarks
    bmark_read_size = 0.25 * 1024**3

    timings = {}

    nframes = compute_nframes(N, size, write_keys)
    actual_size = compute_actual_size(N, nframes, read_keys)
    nframes_read = int(nframes * bmark_read_size / actual_size)
    if nframes_read == 0:
        nframes_read = 1

    bmark_read_size = compute_actual_size(N, nframes_read, read_keys)
    if nframes_read > nframes:
        nframes_read = nframes
        bmark_read_size = actual_size



    # # if the file size is small, write it once to warm up the disk
    # if size < 64 * 1024**3:
    #     with gsd.fl.open(name='test.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0], ) as f:
    #         write_file(f, nframes, N, write_keys)

    # write it again and time this one
    with gsd.fl.open(name='test.gsd', mode='wb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
        start = time.time()
        write_file(f, nframes, N, write_keys)

    # ensure that all writes to disk are completed and drop file system cache
    call(['sudo', '/bin/sync'])
    call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

    end = time.time()

    timings['write'] = actual_size / 1024**2 / (end - start)
    timings['write_time'] = (end - start) / nframes / len(write_keys) / 1e-3

    # time how long it takes to open the file
    start = time.time()
    with gsd.fl.open(name='test.gsd', mode='rb', application="My application", schema="My Schema", schema_version=[1,0]) as f:
        end = time.time()

        timings['open_time'] = (end - start)

        # Read the file sequentially and measure the time taken
        start = time.time()
        read_sequential_file(f, nframes, nframes_read,
                             read_keys)
        end = time.time()

        timings['seq_read'] = bmark_read_size / 1024**2 / (end - start)
        timings['seq_read_time'] = (end - start) / nframes_read / len(read_keys) / 1e-3

        # drop the file system cache
        call(['sudo', '/bin/sync'])
        call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

        # Read the file randomly and measure the time taken
        start = time.time()
        read_random_file(f, nframes, nframes_read, read_keys)
        end = time.time()

        timings['random_read'] = bmark_read_size / 1024**2 / (end - start)
        timings['random_read_time'] = (end - start) / nframes_read / len(read_keys) / 1e-3

    os.unlink('test.gsd')
    return timings


def run_sweep(size, size_str, read_keys, write_keys):

    for i in [1,128,4096]:

        result = run_benchmarks(i, size, read_keys, write_keys)

        print("{0:<7} {1:<6} {2:<9.4g} {3:<11.3g} {4:<11.3g} {5:<11.3g}"
            .format(size_str, str(i),
                    result['open_time'] * 1000,
                    result['write_time'],
                    result['seq_read_time'],
                    result['random_read_time']))
        sys.stdout.flush()

write_keys = [str(i) for i in range(65535)]
#read_keys = [str(i) for i in range(65535)]
read_keys = ['0']

print("""
======= ====== ========= =========== =========== ==========
Size    N      Open (ms) Write (ms)  Read (ms)   Random (ms)
======= ====== ========= =========== =========== ==========""")

run_sweep(128 * 1024**2, "128 MiB", read_keys, write_keys)
# run_sweep(1 * 1024**3, "1 GiB", read_keys, write_keys)

print("======= ====== ========= ============ "
      "=========== ============= ===========")
