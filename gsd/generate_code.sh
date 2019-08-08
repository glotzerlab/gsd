#!/bin/bash

set -u
set -e
set -x

cython -3 -I . fl.pyx -o fl.c

sha256sum fl.pyx | awk '{ print $1 }' > fl.pyx.sha256
