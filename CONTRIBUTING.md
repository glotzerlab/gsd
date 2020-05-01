Contributions are welcomed via
[pull requests on GitHub](https://github.com/glotzerlab/gsd/pulls).
Contact the **GSD** developers before starting work to ensure it meshes well
with the planned development direction and standards set for the project.

# Features

## Implement functionality in a general and flexible fashion

New features should be applicable to a variety of use-cases. The **GSD**
developers can assist you in designing flexible interfaces.

## Maintain performance of existing code paths

Expensive code paths should only execute when requested.

# Version control

## Base your work off the correct branch

Bug fixes should be based on `maint`. New features should be based on `master`.

## Propose a minimal set of related changes

All changes in a pull request should be closely related. Multiple change sets
that are loosely coupled should be proposed in separate pull requests.

## Agree to the Contributor Agreement

All contributors must agree to the Contributor Agreement
([ContributorAgreement.md](ContributorAgreement.md)) before their pull request
can be merged.

# Source code

## Use a consistent style

[style.rst](doc/style.rst) defines the style guidelines for **GSD** code.

## Document code with comments

Use doxygen header comments for classes, functions, etc. Also comment complex
sections of code so that other developers can understand them.

## Compile without warnings

Your changes should compile without warnings.

# Tests

## Write unit tests

Add unit tests for all new functionality.

## Validity tests

The developer should run research-scale simulations using the new functionality
and ensure that it behaves as intended.

# User documentation

## Write user documentation

Document public-facing API with Python docstrings in Google style.

## Example notebooks

Demonstrate new functionality in the documentation examples pages.

## Document version status

Each user-facing Python class, method, etc. with a docstring should have
[versionadded, versionchanged, and deprecated Sphinx
directives]

## Add developer to the credits

Update the credits documentation to reference what each developer contributed to
the code.

## Propose a change log entry

Propose a short concise entry describing the change in the pull request
description.
