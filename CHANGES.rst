Changes
-------

1.2.1 (2026-11-12)
~~~~~~~~~~~~~~~~~~

* Switched build backend from setuptools to hatchling.
* Moved package to ``src/`` layout; tests moved to top-level ``tests/``.
* Ported tests to pytest-django fixtures.
* Removed unused mypy, django-stubs, djLint and factory-boy dev dependencies.

1.2.0 (2026-10-10)
~~~~~~~~~~~~~~~~~~

* Added Python 3.15 support.
* Dropped Python 3.10 support; now requires Python 3.11-3.15.

1.1.0 (2026-08-14)
~~~~~~~~~~~~~~~~~~

* Dropped Python 3.6-3.9 support; now requires Python 3.10-3.14.
* Dropped Django 2.2-3.2 support; now requires Django 5.2-6.1.
* Require ``django-sitecats>=1.2.2`` explicitly (Django 4+ support was introduced there; dependency was previously unpinned).

1.0.1 (2021-11-30)
~~~~~~~~~~~~~~~~~~

* Add missing mo files.

1.0.0 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Added Django 3+ support.
* Dropped Python 2.7 support.
* Dropped Django 1.10 / 1.11 support.
