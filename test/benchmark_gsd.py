import time
import gsd
import os
import math
import numpy
import random
import array
import sys
from subprocess import call, PIPE

def write_frame(file, frame, position, orientation):
    gsd.libgsd.gsd_write_chunk(file, "pos", 3, position.shape[0], position.shape[1], frame, position);
    gsd.libgsd.gsd_write_chunk(file, "ori", 3, orientation.shape[0], orientation.shape[1], frame, orientation);
    gsd.libgsd.gsd_end_frame(file);

def read_frame(file, frame, position, orientation):
    pos_chunk = gsd.libgsd.gsd_find_chunk(file, frame, "pos");
    gsd.libgsd.gsd_read_chunk(file, position, pos_chunk);

    orientation_chunk = gsd.libgsd.gsd_find_chunk(file, frame, "ori");
    gsd.libgsd.gsd_read_chunk(file, orientation, orientation_chunk);

def write_random_file(file, nframes, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps);
    if step == 0:
        step = 1;

    for i in range(0,nframes):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr)

        write_frame(file, i, position, orientation);

def read_sequential_file(file, nframes, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps);
    if step == 0:
        step = 1;

    for i in range(0,nframes):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr)

        read_frame(file, i, position, orientation);

def read_random_file(file, nframes, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps);
    if step == 0:
        step = 1;

    frames = list(range(0,nframes));
    random.shuffle(frames);

    for i,f in enumerate(frames):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr)
        read_frame(file, f, position, orientation);

def compute_nframes(N, size):
    bytes_per_frame = (3+4)*4 * N;
    return int(math.ceil(size / bytes_per_frame));

def compute_actual_size(N, nframes):
    bytes_per_frame = (3+4)*4 * N;
    return nframes * bytes_per_frame;

## Run all benchmarks with the given options
def run_benchmarks(N, size):
    timings = {}
    position = numpy.random.random((N,3)).astype('float32');
    orientation = numpy.random.random((N,4)).astype('float32');

    nframes = compute_nframes(N, size);
    actual_size = compute_actual_size(N, nframes);

    # first, write the file and time how long it takes
    print("Writing file: ", file=sys.stderr)
    start = time.time();
    gsd.libgsd.gsd_create('test.gsd', 'test', 'test', 1);
    file = gsd.libgsd.gsd_open('test.gsd', 1);
    write_random_file(file, nframes, N, position, orientation);
    gsd.libgsd.gsd_close(file);
    end = time.time();

    timings['write'] = actual_size / 1024**2 / (end - start);

    call(['sudo', '/bin/sync']);
    call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE);

    # time how long it takes to open the file
    print("Opening file... ", file=sys.stderr, end='')
    start = time.time();
    file = gsd.libgsd.gsd_open('test.gsd', 2);
    end = time.time();
    print(end - start, "s", file=sys.stderr);

    timings['open_time'] = (end - start);

    # Read the file sequentially and measure the time taken
    print("Sequential read file:", file=sys.stderr)
    start = time.time();
    read_sequential_file(file, nframes, N, position, orientation);
    end = time.time();

    timings['seq_read'] = actual_size / 1024**2 / (end - start);

    # If the size is small, read the file again (cached)
    if size < 10*1024**3:
        print("Sequential read file: (cached)", file=sys.stderr)
        start = time.time();
        read_sequential_file(file, nframes, N, position, orientation);
        end = time.time();

        timings['seq_cache_read'] = actual_size / 1024**2 / (end - start);
    else:
        timings['seq_cache_read'] = 0;

    # Read the file randomly and measure the time taken
    print("Random read file:", file=sys.stderr)
    start = time.time();
    read_random_file(file, nframes, N, position, orientation);
    end = time.time();

    timings['random_read'] = actual_size / 1024**2 / (end - start);
    timings['random_read_time'] = (end - start) / nframes / 1e-3;

    gsd.libgsd.gsd_close(file);
    os.unlink('test.gsd')
    return timings

def run_sweep(size, size_str):

    #if size < 10*1024**3:
    if True:

        result = run_benchmarks(32*32, size)

        print("| {0} | {1} | {2:.3g} | {3:.4g} | {4:.4g} | {5:.4g} | {6:.4g} | {7:.2g} |".format(size_str, "32^2", result['open_time'], result['write'], result['seq_read'], result['seq_cache_read'], result['random_read'], result['random_read_time']));
        sys.stdout.flush();

    result = run_benchmarks(100*100, size)

    print("| {0} | {1} | {2:.3g} | {3:.4g} | {4:.4g} | {5:.4g} | {6:.4g} | {7:.2g} |".format(size_str, "100^2", result['open_time'], result['write'], result['seq_read'], result['seq_cache_read'], result['random_read'], result['random_read_time']));
    sys.stdout.flush();

    result = run_benchmarks(1000*1000, size)

    print("| {0} | {1} | {2:.3g} | {3:.4g} | {4:.4g} | {5:.4g} | {6:.4g} | {7:.2g} |".format(size_str, "1000^2", result['open_time'], result['write'], result['seq_read'], result['seq_cache_read'], result['random_read'], result['random_read_time']));
    sys.stdout.flush();


print("""
| Size | N   | Open time (s) | Write (MB/s) | Seq read (MB/s) | Seq read cached (MB/s) | Random read (MB/s) | Random read time (ms) |
| :--- | :-- | :-----------   | :---------   | :-----------    | :-----------           | :-----------       | :-----------          |""");

run_sweep(100*1024**2, "100 MiB");
run_sweep(1*1024**3, "1 GiB");
run_sweep(128*1024**3, "128 GiB");
