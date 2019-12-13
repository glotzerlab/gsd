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

# import logging
# logging.basicConfig(level=logging.DEBUG)


def write_frame(file, frame, position, orientation):
    snap = gsd.hoomd.Snapshot()
    snap.particles.N = position.shape[0]
    snap.configuration.step = frame * 10
    position[0][0] = frame
    orientation[0][0] = frame
    snap.particles.position = position
    snap.particles.orientation = orientation
    file.append(snap)


def read_frame(file, frame, position, orientation):
    snap = file[frame] # noqa


def write_file(file, nframes, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps)
    if step == 0:
        step = 1

    for i in range(0, nframes):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr, flush=True)

        write_frame(file, i, position, orientation)


def read_sequential_file(file, nframes, nframes_read, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps)
    if step == 0:
        step = 1

    for i in range(0, nframes_read):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr, flush=True)

        read_frame(file, i, position, orientation)


def read_random_file(file, nframes, nframes_read, N, position, orientation):
    steps = compute_actual_size(N, nframes) / (250 * 1024**2)
    step = int(nframes / steps)
    if step == 0:
        step = 1

    frames = list(range(0, nframes))
    random.shuffle(frames)

    for i, f in enumerate(frames[:nframes_read]):
        if i % step == 0:
            print(i, "/", nframes, file=sys.stderr, flush=True)
        read_frame(file, f, position, orientation)


def compute_nframes(N, size):
    bytes_per_frame = (3 + 4) * 4 * N
    return int(math.ceil(size / bytes_per_frame))


def compute_actual_size(N, nframes):
    bytes_per_frame = (3 + 4) * 4 * N
    return nframes * bytes_per_frame

# Run all benchmarks with the given options


def run_benchmarks(N, size):
    bmark_read_size = 0.25 * 1024**3

    timings = {}
    position = numpy.random.random((N, 3)).astype('float32')
    orientation = numpy.random.random((N, 4)).astype('float32')

    nframes = compute_nframes(N, size)
    actual_size = compute_actual_size(N, nframes)
    nframes_read = int(nframes * bmark_read_size / actual_size)
    bmark_read_size = compute_actual_size(N, nframes_read)
    if nframes_read > nframes:
        nframes_read = nframes
        bmark_read_size = actual_size

    # first, write the file and time how long it takes
    print("Writing file: ", file=sys.stderr, flush=True)

    # if the file size is small, write it once to warm up the disk
    if size < 64 * 1024**3:
        gsd.hoomd.create(name='test.gsd')
        with gsd.fl.GSDFile(name='test.gsd', mode='wb') as f:
            hf = gsd.hoomd.HOOMDTrajectory(f)
            write_file(hf, nframes, N, position, orientation)

    # write it again and time this one
    gsd.hoomd.create(name='test.gsd')
    with gsd.fl.GSDFile(name='test.gsd', mode='wb') as f:
        hf = gsd.hoomd.HOOMDTrajectory(f)
        start = time.time()
        write_file(hf, nframes, N, position, orientation)

    # ensure that all writes to disk are completed and drop file system cache
    call(['sudo', '/bin/sync'])
    call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

    end = time.time()

    timings['write'] = actual_size / 1024**2 / (end - start)

    # time how long it takes to open the file
    print("Opening file... ", file=sys.stderr, flush=True, end='')
    start = time.time()
    with gsd.fl.GSDFile(name='test.gsd', mode='rb') as f:
        # with gsd.pygsd.GSDFile(open('test.gsd', mode='rb')) as f:
        hf = gsd.hoomd.HOOMDTrajectory(f)
        end = time.time()

        print(end - start, "s", file=sys.stderr, flush=True)

        timings['open_time'] = (end - start)

        # Read the file sequentially and measure the time taken
        print("Sequential read file:", file=sys.stderr, flush=True)
        start = time.time()
        read_sequential_file(hf, nframes, nframes_read,
                             N, position, orientation)
        end = time.time()

        timings['seq_read'] = bmark_read_size / 1024**2 / (end - start)

        # drop the file system cache
        call(['sudo', '/bin/sync'])
        call(['sudo', '/sbin/sysctl', 'vm.drop_caches=3'], stdout=PIPE)

        # Read the file randomly and measure the time taken
        print("Random read file:", file=sys.stderr, flush=True)
        start = time.time()
        read_random_file(hf, nframes, nframes_read, N, position, orientation)
        end = time.time()

        timings['random_read'] = bmark_read_size / 1024**2 / (end - start)
        timings['random_read_time'] = (end - start) / nframes_read / 1e-3

    os.unlink('test.gsd')
    return timings


def run_sweep(size, size_str):

    # if size < 10*1024**3:
    if True:
        result = run_benchmarks(32 * 32, size)

        print("{0:<7} {1:<6} {2:<9.4g} {3:<12.4g} "
              "{4:<11.4g} {5:<13.4g} {6:<11.3g}"
              .format(size_str, "32^2",
                      result['open_time'] * 1000,
                      result['write'],
                      result['seq_read'],
                      result['random_read'],
                      result['random_read_time']))
        sys.stdout.flush()

    result = run_benchmarks(128 * 128, size)

    print("{0:<7} {1:<6} {2:<9.4g} {3:<12.4g} {4:<11.4g} {5:<13.4g} {6:<11.3g}"
          .format(size_str, "128^2",
                  result['open_time'] * 1000,
                  result['write'],
                  result['seq_read'],
                  result['random_read'],
                  result['random_read_time']))
    sys.stdout.flush()

    result = run_benchmarks(1024 * 1024, size)

    print("{0:<7} {1:<6} {2:<9.4g} {3:<12.4g} {4:<11.4g} {5:<13.4g} {6:<11.3g}"
          .format(size_str, "1024^2",
                  result['open_time'] * 1000,
                  result['write'],
                  result['seq_read'],
                  result['random_read'],
                  result['random_read_time']))
    sys.stdout.flush()


print("""
======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========""")

run_sweep(128 * 1024**2, "128 MiB")
run_sweep(1 * 1024**3, "1 GiB")
# run_sweep(128*1024**3, "128 GiB");

print("======= ====== ========= ============ "
      "=========== ============= ===========")
