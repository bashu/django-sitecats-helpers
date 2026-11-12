from django.contrib import admin

from sitecats_helpers.admin import CategoryCounter
from sitecats_helpers.admin import CategoryListFilter
from sitecats_helpers.admin import CategoryStackedInline
from sitecats_helpers.admin import CategoryTabularInline

from .models import Article
from .models import Comment


@admin.register(Article)
class ArticleAdmin(CategoryCounter, admin.ModelAdmin):
    list_display = ("title", "category_counter")
    list_filter = (CategoryListFilter,)
    inlines = (CategoryStackedInline,)


# Registered with a tabular inline to exercise CategoryTabularInline separately.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = (CategoryTabularInline,)
