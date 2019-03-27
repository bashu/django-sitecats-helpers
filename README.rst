django-sitecats-helpers
=======================

Django admin helper classes for django-sitecats_ categories.

Authored by `Basil Shubin <http://github.com/bashu>`_, inspired by django-taggit-helpers_

.. image:: https://img.shields.io/pypi/v/django-sitecats-helpers.svg
    :target: https://pypi.python.org/pypi/django-sitecats-helpers/

.. image:: https://img.shields.io/pypi/dm/django-sitecats-helpers.svg
    :target: https://pypi.python.org/pypi/django-sitecats-helpers/

.. image:: https://img.shields.io/github/license/bashu/django-sitecats-helpers.svg
    :target: https://pypi.python.org/pypi/django-sitecats-helpers/

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-sitecats-helpers


Configuration
-------------

First make sure the project is configured for django-sitecats_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'sitecats_helpers',
    )


Usage
=====

CategoryCounter
---------------

Display (and sort by) number of categories associated with objects.

.. code-block:: python

    from sitecats_helpers import CategoryCounter
    # For Django 1.9+, use this instead:
    # from sitecats_helpers.admin import CategoryCounter

    class MyModelAdmin(CategoryCounter, admin.ModelAdmin):    # CategoryCounter before ModelAdmin
        list_display = (
            ...
            'category_counter',
        )

CategoryListFilter
------------------

Filter records by categories for the current model only.

.. code-block:: python

    from sitecats_helpers import CategoryListFilter
    # For Django 1.9+, use this instead:
    # from sitecats_helpers.admin import CategoryListFilter

    class MyModelAdmin(admin.ModelAdmin):
        list_filter = [CategoryListFilter]

CategoryStackedInline
---------------------

Add stacked inline for categories to admin.

.. code-block:: python

    from sitecats_helpers import CategoryStackedInline
    # For Django 1.9+, use this instead:
    # from sitecats_helpers.admin import CategoryStackedInline

    class MyModelAdmin(admin.ModelAdmin):
        inlines = [CategoryStackedInline]

CategoryTabularInline
---------------------

Add tabular inline for categorise to admin.

.. code-block:: python

    from sitecats_helpers import CategoryTabularInline
    # For Django 1.9+, use this instead:
    # from sitecats_helpers.admin import CategoryTabularInline

    class MyModelAdmin(admin.ModelAdmin):
        inlines = [CategoryTabularInline]

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-sitecats: https://github.com/idlesign/django-sitecats
.. _django-taggit-helpers: https://github.com/mfcovington/django-taggit-helpers
