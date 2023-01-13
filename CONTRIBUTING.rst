.. Copyright (c) 2016-2023 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

Contributing
============

Contributions are welcomed via `pull requests on GitHub
<https://github.com/glotzerlab/gsd/pulls>`__. Contact the **GSD** developers before starting work to
ensure it meshes well with the planned development direction and standards set for the project.

Features
--------

Implement functionality in a general and flexible fashion
_________________________________________________________

New features should be applicable to a variety of use-cases. The **GSD** developers can assist you
in designing flexible interfaces.

Maintain performance of existing code paths
___________________________________________

Expensive code paths should only execute when requested.

Version control
---------------

Base your work off the correct branch
_____________________________________

- Base backwards compatible bug fixes on ``trunk-patch``.
- Base additional functionality on ``trunk-minor``.
- Base API incompatible changes on ``trunk-major``.

Propose a minimal set of related changes
________________________________________

All changes in a pull request should be closely related. Multiple change sets that are loosely
coupled should be proposed in separate pull requests.

Agree to the Contributor Agreement
__________________________________

All contributors must agree to the Contributor Agreement before their pull request can be merged.

Set your git identity
_____________________

Git identifies every commit you make with your name and e-mail. `Set your identity`_ to correctly
identify your work and set it identically on all systems and accounts where you make commits.

.. _Set your identity: http://www.git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup

Source code
-----------

Use a consistent style
______________________

The **Code style** section of the documentation sets the style guidelines for **GSD** code.

Document code with comments
___________________________

Use doxygen header comments for classes, functions, etc. Also comment complex sections of code so
that other developers can understand them.

Compile without warnings
________________________

Your changes should compile without warnings.

Tests
-----

Write unit tests
________________

Add unit tests for all new functionality.

Validity tests
______________

The developer should run research-scale simulations using the new functionality and ensure that it
behaves as intended.

User documentation
------------------

Write user documentation
________________________

Document public-facing API with Python docstrings in Google style.

Example notebooks
_________________

Demonstrate new functionality in the documentation examples pages.

Document version status
_______________________

Each user-facing Python class, method, etc. with a docstring should have [``versionadded``,
``versionchanged``, and ``deprecated`` Sphinx directives]

Add developer to the credits
____________________________

Update the credits documentation to name each developer that has contributed to the code.

Propose a change log entry
__________________________

Propose a short concise entry describing the change in the pull request description.
