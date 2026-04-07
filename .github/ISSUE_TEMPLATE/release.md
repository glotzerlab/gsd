---
name: Release checklist
about: '[for maintainer use]'
title: 'Release gsd 5.0.0'
labels: ''
assignees: 'joaander'

---

To make a new GSD release:

- [ ] Make a new `release-{X.Y.Z}` branch (where `{X.Y.Z}` is the new version).

On that branch, take the following steps (committing after each step when needed):

- [ ] Run `prek autoupdate`
- [ ] Check for new or duplicate contributors since the last release:
  `comm -13 (git log $(git describe --tags --abbrev=0) --format="%aN <%aE>" | sort | uniq | psub) (git log --format="%aN <%aE>" | sort | uniq | psub)`.
  Add entries to `.mailmap` to remove duplicates.
- [ ] Review `CHANGELOG.rst` and revise if needed.
- [ ] Run `bump-my-version bump {type}`. Replace `{type}` with:
  - `patch` when this release *only* includes bug fixes.
  - `minor` when this release includes new features and possibly bug fixes.
  - `major` when this release includes API breaking changes.
- [ ] Push the branch and open a pull request.
- [ ] Check that readthedocs builds the docs correctly in the pull request checks.
- [ ] Merge the pull request after all tests pass.
- [ ] Make a new tag on the trunk branch:
  ```
  git switch trunk
  git pull
  git tag -a v{X.Y.Z}
  git push origin --tags
  ```

> [!IMPORTANT]
> Make sure to **include** `v` in the tag name!

Navigate to https://github.com/glotzerlab/gsd/actions and approve the request
to post the release. The `release` GitHub Action will post GitHub and PyPI
releases. After a few hours, the conda-forge autotick bot will submit a PR for
the new release.

- [ ] Check that the GitHub release posted correctly: https://github.com/glotzerlab/hoomd-blue/releases
- [ ] Check that the PyPi release posted correctly: https://pypi.org/project/gsd/
- [ ] Merge the conda-forge recipe, updating it first if necessary (e.g. when adding dependencies).


- [ ] Via pull request, add a blank release notes entry for the next release:
  ```
  Next release
  ^^^^^^^^^^^^^^^^^^^^

  *Added*

  *Changed*

  *Deprecated*

  *Removed*

  *Fixed*
  ```

> [!NOTE]
> Paste `Next release` exactly as shown. `bump-my-version` will replace that
> string with the version number and date.

