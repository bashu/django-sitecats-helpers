from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from sitecats.utils import get_tie_model


class CategoryCounter:
    def get_queryset(self, request):
        return self.model.objects.get_queryset().annotate(
            category_counter=Count("categories__category", distinct=True),
        )

    @admin.display(
        description=_("# of categories"),
        ordering="category_counter",
    )
    def category_counter(self, obj):
        return obj.category_counter


class CategoryListFilter(admin.SimpleListFilter):
    title = _("category")
    parameter_name = "category"

    def lookups(self, request, model_admin):
        ct = ContentType.objects.get_for_model(model_admin.model)
        return tuple(
            (cat.pk, cat.title)
            for cat in get_tie_model().get_linked_objects(
                filter_kwargs={"content_type": ct},
                by_category=True,
            )
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(categories__category__id=self.value()).distinct()
        return queryset


class CategoryInlineBase:
    model = get_tie_model()
    verbose_name = _("category")
    verbose_name_plural = _("categories")
    ordering = ["category__title"]


class CategoryStackedInline(CategoryInlineBase, GenericStackedInline):
    pass


class CategoryTabularInline(CategoryInlineBase, GenericTabularInline):
    pass
