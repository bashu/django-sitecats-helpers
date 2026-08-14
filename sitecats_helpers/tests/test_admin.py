from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.test import RequestFactory
from django.test import TestCase

from sitecats.utils import get_category_model
from sitecats.utils import get_tie_model

from sitecats_helpers.admin import CategoryStackedInline
from sitecats_helpers.admin import CategoryTabularInline

from .admin import ArticleAdmin
from .admin import CommentAdmin
from .models import Article
from .models import Comment


class CategoryCounterTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )
        category_model = get_category_model()
        self.cat1 = category_model.add(title="Politics", creator=self.user)
        self.cat2 = category_model.add(title="Sports", creator=self.user)

        self.tied_once = Article.objects.create(title="tied once")
        self.tied_once.categories.create(category=self.cat1, creator=self.user)

        self.tied_twice = Article.objects.create(title="tied twice")
        self.tied_twice.categories.create(category=self.cat1, creator=self.user)
        self.tied_twice.categories.create(category=self.cat2, creator=self.user)

        self.untied = Article.objects.create(title="untied")

        self.model_admin = ArticleAdmin(Article, admin.site)

    def get_request(self):
        request = self.factory.get("/")
        request.user = self.user
        return request

    def test_annotates_category_counter(self):
        counters = {
            obj.pk: obj.category_counter
            for obj in self.model_admin.get_queryset(self.get_request())
        }
        assert counters[self.tied_once.pk] == 1
        assert counters[self.tied_twice.pk] == 2  # noqa: PLR2004
        assert counters[self.untied.pk] == 0

    def test_category_counter_method_reads_annotation(self):
        obj = self.model_admin.get_queryset(self.get_request()).get(
            pk=self.tied_twice.pk,
        )
        assert self.model_admin.category_counter(obj) == 2  # noqa: PLR2004

    def test_category_counter_is_sortable(self):
        assert ArticleAdmin.category_counter.admin_order_field == "category_counter"

        ordered = list(
            self.model_admin.get_queryset(self.get_request()).order_by(
                "category_counter",
            ),
        )
        assert ordered == [self.untied, self.tied_once, self.tied_twice]


class CategoryInlineTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )

    def get_request(self):
        request = self.factory.get("/")
        request.user = self.user
        return request

    def test_stacked_inline_is_configured_for_ties(self):
        assert issubclass(CategoryStackedInline, GenericStackedInline)
        assert CategoryStackedInline.model is get_tie_model()
        assert CategoryStackedInline.ordering == ["category__title"]

    def test_tabular_inline_is_configured_for_ties(self):
        assert issubclass(CategoryTabularInline, GenericTabularInline)
        assert CategoryTabularInline.model is get_tie_model()
        assert CategoryTabularInline.ordering == ["category__title"]

    def test_stacked_inline_formset_binds_to_instance(self):
        article = Article.objects.create(title="article")
        model_admin = ArticleAdmin(Article, admin.site)
        (inline,) = model_admin.get_inline_instances(self.get_request(), article)
        formset_class = inline.get_formset(self.get_request(), article)
        assert formset_class(instance=article).instance == article

    def test_tabular_inline_formset_binds_to_instance(self):
        comment = Comment.objects.create(title="comment")
        model_admin = CommentAdmin(Comment, admin.site)
        (inline,) = model_admin.get_inline_instances(self.get_request(), comment)
        formset_class = inline.get_formset(self.get_request(), comment)
        assert formset_class(instance=comment).instance == comment
