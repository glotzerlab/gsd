# GSD Change Log

[TOC]

## v1.5.0

Released 2018-01-18

* Read and write HPMC shape state data.

## v1.4.0

Released 2017-12-04

* Support reading and writing chunks with 0 length. No schema changes are necessary to support this.

## v1.3.0

Released 2017-11-17

* Document `state` entries in the HOOMD schema
* No changes to the gsd format or reader code in v1.3

## v1.2.0

* Add gsd.hoomd.open() method which can create and open hoomd gsd files
* Add gsd.fl.open() method which can create and open gsd files
* The previous create/class GSDFile instantation is still supported
  for backward compatibility.

## v1.1

* add special pairs section pairs/ to HOOMD schema
* bump HOOMD schema version to 1.1

## v1.0.1

* Fix compile error on more strict POSIX sytstems.

## v1.0.0

Initial release.
