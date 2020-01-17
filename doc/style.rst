.. Copyright (c) 2016-2020 The Regents of the University of Michigan
.. This file is part of the General Simulation Data (GSD) project, released
.. under the BSD 2-Clause License.

Code style
==========

All code in GSD must follow a consistent style to ensure readability.
We provide configuration files for linters (specified below) so that developers
can automatically validate and format files.

Python
------

Python code in HOOMD should follow `PEP8
<https://www.python.org/dev/peps/pep-0008>`_ with the following choices:

* 80 character line widths.
* Hang closing brackets.
* Break before binary operators.

Tools
^^^^^

* Linter: `flake8 <http://flake8.pycqa.org/en/latest/>`_ with
  `pep8-naming <https://pypi.org/project/pep8-naming/>`_
* Autoformatter: `autopep8 <https://pypi.org/project/autopep8/>`_
* Run: ``flake8`` to see a list of violations.
* See ``setup.cfg`` for the **flake8** configuration (also used by
  **autopep8**).

Documentation
^^^^^^^^^^^^^

Python code should be documented with docstrings and added to the Sphinx
documentation index in ``doc/``. Docstrings should follow Google style
formatting for use in `Napoleon
<https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_.

C
---

* 100 character line width.
* Indent only with spaces.
* 4 spaces per indent level.
* Naming conventions:

    * Functions: lowercase with words separated by underscores
      ``function_name``.
    * Structures: lowercase with words separated by underscores
      ``struct_name``.
    * Constants: all upper-case with words separated by underscores
      ``SOME_CONSTANT``.

Tools
^^^^^

* Autoformatter: `clang-format <https://clang.llvm.org/docs/ClangFormat.html>`_.
* Run: ``./run-clang-format.py -r gsd`` to see needed changes.
* Run: ``clang-format -i gsd/gsd.c`` to apply the changes.
* Style configuration: See ``.clang-format``.

.. note::

    We plan to provide change the style once **clang-format** 10 is available.

Documentation
^^^^^^^^^^^^^

Documentation comments should be in Javadoc format and precede the item they
document for compatibility with Doxygen and most source code editors. Multi-line
documentation comment blocks start with ``/**`` and single line ones start with
``///``.

See ``gsd.h`` for an example.

Other file types
----------------

Use your best judgment and follow existing patterns when styling CMake,
restructured text, markdown, and other files. The following general guidelines
apply:

* 100 character line width.
* 4 spaces per indent level.
* 4 space indent.
