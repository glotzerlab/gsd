.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

.. _shapes:

Shape Visualization
===================

The chunk :chunk:`particles/type_shapes` stores information about shapes
corresponding to particle types. Shape definitions are stored for each type as a
UTF-8 encoded JSON string containing key-value pairs. The class of a shape is
defined by the ``type`` key. All other keys define properties of that shape.
Keys without a default value are required for a valid shape specification.

Empty (Undefined) Shape
-----------------------

An empty dictionary can be used for undefined shapes. A visualization
application may choose how to interpret this, e.g. by drawing nothing or drawing
spheres.

Example::

    {}

Spheres
-------

Type: ``Sphere``

Spheres' dimensionality (2D circles or 3D spheres) can be inferred from the
system box dimensionality.

=============== =============== ====== ==== ======= ======
Key             Description     Type   Size Default Units
=============== =============== ====== ==== ======= ======
diameter        Sphere diameter float  1x1          length
=============== =============== ====== ==== ======= ======

Example::

    {
        "type": "Sphere",
        "diameter": 2.0
    }

Ellipsoids
----------

Type: ``Ellipsoid``

The ellipsoid class has principal axes a, b, c corresponding to its radii in the
x, y, and z directions.

=============== ===================== ====== ==== ======= ======
Key             Description           Type   Size Default Units
=============== ===================== ====== ==== ======= ======
a               Radius in x direction float  1x1          length
b               Radius in y direction float  1x1          length
c               Radius in z direction float  1x1          length
=============== ===================== ====== ==== ======= ======

Example::

    {
        "type": "Ellipsoid",
        "a": 7.0,
        "b": 5.0,
        "c": 3.0
    }

Polygons
--------

Type: ``Polygon``

A simple polygon with its vertices specified in a counterclockwise order.
Spheropolygons can be represented using this shape type, through the
``rounding_radius`` key.

=============== =============== ===== ==== ======= ======
Key             Description     Type  Size Default Units
=============== =============== ===== ==== ======= ======
rounding_radius Rounding radius float 1x1  0.0     length
vertices        Shape vertices  float Nx2          length
=============== =============== ===== ==== ======= ======

Example::

    {
        "type": "Polygon",
        "rounding_radius": 0.1,
        "vertices": [[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5]]
    }

Convex Polyhedra
----------------

Type: ``ConvexPolyhedron``

A convex polyhedron with vertices specifying the convex hull of the shape.
Spheropolyhedra can be represented using this shape type, through the
``rounding_radius`` key.

=============== =============== ===== ==== ======= ======
Key             Description     Type  Size Default Units
=============== =============== ===== ==== ======= ======
rounding_radius Rounding radius float 1x1  0.0     length
vertices        Shape vertices  float Nx3          length
=============== =============== ===== ==== ======= ======

Example::

    {
        "type": "ConvexPolyhedron",
        "rounding_radius": 0.1,
        "vertices": [[0.5, 0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, 0.5]]
    }

General 3D Meshes
-----------------

Type: ``Mesh``

A list of lists of indices are used to specify faces. Faces must contain 3 or
more vertex indices. The vertex indices must be zero-based. Faces must be
defined with a counterclockwise winding order (to produce an "outward" normal).

=============== ================ ====== ==== ======= ======
Key             Description      Type   Size Default Units
=============== ================ ====== ==== ======= ======
vertices        Shape vertices   float  Nx3          length
indices         Vertices indices uint32              number
=============== ================ ====== ==== ======= ======


Example::

    {
        "type": "Mesh",
        "vertices": [[0.5, 0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, 0.5]],
        "indices": [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]
    }

Sphere Unions
-------------

Type: ``SphereUnion``

A collection of spheres, defined by their diameters and centers.

=============== ================ ===== ==== ======= ======
Key             Description      Type  Size Default Units
=============== ================ ===== ==== ======= ======
diameters       Sphere diameters float Nx1          length
centers         Sphere centers   float Nx3          length
=============== ================ ===== ==== ======= ======

Example::

    {
        "type": "SphereUnion",
        "centers": [[0, 0, 1.0], [0, 1.0, 0], [1.0, 0, 0]],
        "diameters": [0.5, 0.5, 0.5]
    }
