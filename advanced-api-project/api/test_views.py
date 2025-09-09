# api/test_views.py
"""
API view tests for the Book endpoints.

Covers:
- CRUD: list, detail, create, update, delete
- Permissions: unauthenticated vs authenticated behavior
- Validation: publication_year not in the future
- Filtering: title, author, publication_year, min_year/max_year
- Search: across title and author__name
- Ordering: asc/desc on publication_year

Run:  python manage.py test api
"""

from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Authors
        cls.achebe = Author.objects.create(name="Chinua Achebe")
        cls.soyinka = Author.objects.create(name="Wole Soyinka")

        # Books
        cls.tfa = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=cls.achebe
        )
        cls.nlae = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=cls.achebe
        )
        cls.ake = Book.objects.create(
            title="Aké: The Years of Childhood", publication_year=1981, author=cls.soyinka
        )

        # Auth user
        cls.username = "tester"
        cls.password = "testpass123"
        from django.contrib.auth import get_user_model

        User = get_user_model()
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)

    def setUp(self):
        self.client = APIClient()

    # ---------- READ (public) ----------

    def test_list_books_public_ok(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("results", resp.data)
        self.assertGreaterEqual(resp.data["count"], 3)

    def test_detail_book_public_ok(self):
        url = reverse("book-detail", kwargs={"pk": self.tfa.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], self.tfa.id)
        self.assertEqual(resp.data["title"], "Things Fall Apart")
        self.assertEqual(resp.data["publication_year"], 1958)

    # ---------- CREATE (auth required) ----------

    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        payload = {"title": "The Interpreter", "publication_year": 1965, "author": self.soyinka.id}
        resp = self.client.post(url, payload, format="json")
        # DRF returns 403 (Forbidden) for unauthenticated POST with IsAuthenticated
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated_201(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("book-create")
        payload = {"title": "The Interpreter", "publication_year": 1965, "author": self.soyinka.id}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], "The Interpreter")
        self.assertEqual(resp.data["publication_year"], 1965)
        self.assertEqual(resp.data["author"], self.soyinka.id)

    def test_create_book_future_year_400(self):
        self.client.login(username=self.username, password=self.password)
        future = date.today().year + 1
        url = reverse("book-create")
        payload = {"title": "Future Book", "publication_year": future, "author": self.achebe.id}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", resp.data)

    # ---------- UPDATE (auth required) ----------

    def test_update_book_requires_auth(self):
        url = reverse("book-update", kwargs={"pk": self.tfa.id})
        resp = self.client.patch(url, {"publication_year": 1959}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated_200(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("book-update", kwargs={"pk": self.tfa.id})
        resp = self.client.patch(url, {"publication_year": 1959}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["publication_year"], 1959)

    # ---------- DELETE (auth required) ----------

    def test_delete_book_requires_auth(self):
        url = reverse("book-delete", kwargs={"pk": self.nlae.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated_204(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("book-delete", kwargs={"pk": self.nlae.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Verify it is gone
        detail = self.client.get(reverse("book-detail", kwargs={"pk": self.nlae.id}))
        self.assertEqual(detail.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- FILTERS ----------

    def test_filter_publication_year_exact(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"publication_year": 1960})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["count"], 1)
        self.assertEqual(resp.data["results"][0]["title"], "No Longer at Ease")

    def test_filter_by_author_id(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"author": self.achebe.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data["results"]]
        self.assertIn("Things Fall Apart", titles)
        self.assertIn("No Longer at Ease", titles)

    def test_filter_title_icontains(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"title": "fall"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(b["title"] == "Things Fall Apart" for b in resp.data["results"]))

    def test_filter_year_range(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"min_year": 1950, "max_year": 1970})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data["results"]]
        self.assertIn("Things Fall Apart", titles)
        self.assertIn("No Longer at Ease", titles)

    # ---------- SEARCH ----------

    def test_search_author_name(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"search": "achebe"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data["results"]]
        self.assertIn("Things Fall Apart", titles)
        self.assertIn("No Longer at Ease", titles)

    # ---------- ORDERING ----------

    def test_ordering_desc_publication_year(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data["results"]]
        self.assertEqual(sorted(years, reverse=True), years)
