#!/bin/bash

set -u
set -e
set -x

cython -2 -I . fl.pyx -o fl2.c
cython -3 -I . fl.pyx -o fl3.c

sha256sum fl.pyx | awk '{ print $1 }' > fl.pyx.sha256
