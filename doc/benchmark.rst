.. Copyright (c) 2016-2020 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

Benchmarks
==========

The benchmark script :file:`scripts/benchmark-hoomd.py` runs a suite of I/O benchmarks that measure the time it takes
to write a file, read frames sequentially, and read frames randomly. This script only runs on linux and requires that
the user have no-password ``sudo`` access (set this only temporarily). It flushes filesystem buffers and clears the
cache to provide accurate timings. It is representative of typical use cases, storing position and orientation in
a hoomd schema GSD file at each frame. The benchmark runs at fixed file sizes with varying N (and varying number of
frames) in order to test small block and large block I/O.

SSD
---

Samsung SSD 840 EVO 120GB

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   2.063     45.23        64.77       50.13         0.545
128 MiB 128^2  1.091     175          304.1       226.3         1.93
128 MiB 1024^2 15.56     177.7        366.2       463.8         60.4
1 GiB   32^2   3.119     54.15        73.57       35.79         0.764
1 GiB   128^2  1.703     227          305.2       188.3         2.32
1 GiB   1024^2 8.414     175.8        425.5       474.5         59
16 GiB  32^2   5.401     58.3         70.02       26.22         1.04
16 GiB  128^2  5.286     134.5        330.7       152.4         2.87
16 GiB  1024^2 8.054     130          406.7       465.5         60.1
======= ====== ========= ============ =========== ============= ===========

NFS
---

10Gb Ethernet connection (Intel X520) through several 10Gb switches into a 100Gb campus backbone into a modern
multi-petabyte Isilon fileserver, mounted with NFSv3.

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   16.34     42.24        84.79       39.24         0.697
128 MiB 128^2  11.14     172.2        192.6       142.7         3.07
128 MiB 1024^2 10.16     163.5        161.1       186.3         150
1 GiB   32^2   18.54     56.64        76.98       18.41         1.49
1 GiB   128^2  10.93     227.6        197.1       70.84         6.18
1 GiB   1024^2 17.35     253.5        166.8       155.6         180
128 GiB 32^2   146.9     55.34        75.62       2.111         13
128 GiB 128^2  29.95     265.3        353.5       27.03         16.2
128 GiB 1024^2 34.83     319.3        225.9       116.7         240
======= ====== ========= ============ =========== ============= ===========

HDD
---

RAID 1 (mdadm) on two ST3000NM0033-9ZM178 drives.

======= ====== ========= ============ =========== ============= ===========
Size    N      Open (ms) Write (MB/s) Read (MB/s) Random (MB/s) Random (ms)
======= ====== ========= ============ =========== ============= ===========
128 MiB 32^2   36.43     12.92        59          11.63         2.35
128 MiB 128^2  29.68     72.22        175.5       48.23         9.07
128 MiB 1024^2 10.82     94.69        161.7       167.6         167
1 GiB   32^2   52.85     43.03        59.43       4.943         5.53
1 GiB   128^2  24.22     115.5        174         33.65         13
1 GiB   1024^2 31.61     123.6        153.7       151.8         184
128 GiB 32^2   113.3     46.26        58.36       2.085         13.1
128 GiB 128^2  90.05     141.8        146.6       21.82         20
128 GiB 1024^2 51.49     139.4        139.6       140.8         199
======= ====== ========= ============ =========== ============= ===========

