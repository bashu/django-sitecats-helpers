from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase

from sitecats.utils import get_category_model

from sitecats_helpers.admin import CategoryListFilter

from .admin import ArticleAdmin
from .models import Article
from .models import Comment


class CategoryListFilterTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )
        category_model = get_category_model()
        self.tied = category_model.add(title="Tied", creator=self.user)

        self.article = Article.objects.create(title="article")
        self.article.categories.create(category=self.tied, creator=self.user)

        self.other_article = Article.objects.create(title="other")

        # Tied to a different model only - must not surface as an Article filter option.
        self.other_model_category = category_model.add(
            title="Comment only",
            creator=self.user,
        )
        comment = Comment.objects.create(title="comment")
        comment.categories.create(category=self.other_model_category, creator=self.user)

        self.model_admin = ArticleAdmin(Article, admin.site)

    def test_lookups_only_include_categories_tied_to_this_model(self):
        request = self.factory.get("/")
        f = CategoryListFilter(request, {}, Article, self.model_admin)
        assert f.lookups(request, self.model_admin) == (
            (self.tied.pk, self.tied.title),
        )

    def test_queryset_no_value_is_noop(self):
        request = self.factory.get("/")
        f = CategoryListFilter(request, {}, Article, self.model_admin)
        assert set(f.queryset(request, Article.objects.all())) == {
            self.article,
            self.other_article,
        }

    def test_queryset_filtered_by_category(self):
        params = {"category": str(self.tied.pk)}
        request = self.factory.get("/", params)
        f = CategoryListFilter(request, params, Article, self.model_admin)
        qs = f.queryset(request, Article.objects.all())
        assert list(qs) == [self.article]
        assert self.other_article not in qs
