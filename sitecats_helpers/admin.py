# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Count
from django.contrib.contenttypes.admin import (
    GenericStackedInline, GenericTabularInline)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from sitecats.utils import get_category_model, get_tie_model


class TieCounter():

    def get_queryset(self, request):
        return self.model.objects.get_queryset().annotate(
            tie_counter=Count('categories', distinct=True))

    def tie_counter(self, obj):
        return obj.tie_counter
    tie_counter.admin_order_field = 'tie_counter'
    tie_counter.short_description = _('# of ties')


class CategoryListFilter(admin.SimpleListFilter):
    title = _('category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        ct = ContentType.objects.get_for_model(model_admin.model)
        return tuple([(cat.alias, cat.title) for cat in get_tie_model().get_linked_objects(
            filter_kwargs={'content_type': ct}, by_category=True)])

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(categories__category__alias=self.value())


class CategoryInlineBase():
    model = get_tie_model()
    verbose_name = _('category')
    verbose_name_plural = _('categories')
    ordering = ['category__title']
    exclude = ['creator']


class CategoryStackedInline(CategoryInlineBase, GenericStackedInline):
    pass


class CategoryTabularInline(CategoryInlineBase, GenericTabularInline):
    pass