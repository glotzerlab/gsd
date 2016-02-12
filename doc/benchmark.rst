.. Copyright (c) 2016 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

Benchmarks
==========

The benchmark script :file:`scripts/benchmark-hoomd.py` runs a suite of I/O benchmarks that measure the time it takes
to write a file, read frames sequentially, and read frames randomly. This script only runs on linux and requires that
the user have no-password `sudo` access (set this only temporarily). It flushes filesystem buffers and clears the
cache to provide accurate timings. It is representative of typical use cases, storing position and orientation in
a hoomd schema GSD file at each frame. The benchmark runs at fixed file sizes with varying N (and varying number of
frames) in order to test small block and large block I/O.

SSD
---

Samsung SSD 840 EVO 120GB

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   2.195     14.2         83.32       44.54         0.614
128 MiB 128^2  0.88      153.6        291.2       163.3         2.68
128 MiB 1024^2 12.41     106.8        388.6       466.8         60
1 GiB   32^2   9.476     51.13        75.54       36.98         0.739
1 GiB   128^2  1.591     178.8        349.5       207.3         2.11
1 GiB   1024^2 9.463     166.9        407.6       456.4         61.3
16 GiB  32^2   139.1     58.22        81          26.81         1.02
16 GiB  128^2  9.725     88.68        345.3       169.2         2.59
16 GiB  1024^2 17.29     124.5        96.71       235.9         119
======= ====== ========= ============ =========== ============= ===========


NFS
---

10Gb Ethernet connection (Intel X520) through several 10Gb switches into a 100Gb campus backbone into a modern
multi-petabyte Isilon fileserver, mounted with NFSv3.

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   9.144     47.9         67.09       42.95         0.637
128 MiB 128^2  5.619     176.9        197.9       174.6         2.51
128 MiB 1024^2 9.609     206.5        200.7       191.1         146
1 GiB   32^2   23.58     56.37        75.64       19.68         1.39
1 GiB   128^2  6.977     220.1        182.6       82.37         5.31
1 GiB   1024^2 9.208     234.3        199.1       169.2         166
128 GiB 32^2   2657      53.28        74.26       2.652         10.3
128 GiB 128^2  173.4     236.2        243.4       32.97         13.3
128 GiB 1024^2 22.1      302.1        313.8       144.4         194
======= ====== ========= ============ =========== ============= ===========

HDD
---

RAID 1 (mdadm) on two ST3000NM0033-9ZM178 drives.

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   15.27     32.37        59.56       10.65         2.57
128 MiB 128^2  12.78     45.9         149.7       51.01         8.58
128 MiB 1024^2 35.16     53.25        141.1       153.8         182
1 GiB   32^2   53.64     43.79        65.69       4.714         5.8
1 GiB   128^2  51.54     85.86        149.4       36.86         11.9
1 GiB   1024^2 17.72     105.1        159.6       149.5         187
128 GiB 32^2   3267      46.46        71.52       2.614         10.5
128 GiB 128^2  248.8     138.2        142.3       26.6          16.4
======= ====== ========= ============ =========== ============= ===========
