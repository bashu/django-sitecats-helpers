import django

if django.VERSION < (1, 9):
    from .admin import (
        TieCounter,
        CategoryListFilter,
        CategoryStackedInline,
        CategoryTabularInline,
    )

default_app_config = 'sitecats_helpers.apps.SitecatsHelpersConfig'

__version__ = '0.0.1'