---
name: Release checklist
about: '[for maintainer use]'
title: 'Release gsd 3.X.Y'
labels: ''
assignees: 'joaander'

---

Release checklist:

- [ ] Run *bumpversion*.
- [ ] Review the change log.
- [ ] Check for new or duplicate contributors since the last release:
  `comm -13 <(git log LAST_TAG --format="%aN <%aE>" | sort | uniq) <(git log --format="%aN <%aE>" | sort | uniq)`.
  Add entries to `.mailmap` to remove duplicates.
- [ ] Check readthedocs build, especially change log formatting.
  - [Build status](https://readthedocs.org/projects/gsd/builds/)
  - [Output](https://gsd.readthedocs.io/en/latest/)
- [ ] Tag and push.
- [ ] Update conda-forge recipe.
- [ ] Update glotzerlab-software.
