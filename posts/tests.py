from django.test import TestCase
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import datetime
from .models import *
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .forms import PostForm


class PostTests(TestCase):
    image = open("test_img.jpeg", "rb")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="testuser", email="testuser@gmail.com", password="password"
        )

        cls.post = Post.objects.create(
            title="A good title",
            content="A good body content",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
            slug=slugify("A good title"),
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "A good title")
        self.assertEqual(self.post.content, "A good body content")
        self.assertEqual(self.post.thumbnail.read(), open("test_img.jpeg", "rb").read())
        self.assertEqual(self.post.author, self.user)

    def test_post_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")

    def test_post_details_view(self):
        response = self.client.get(reverse("details", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A good body content")
        self.assertTemplateUsed(response, "details.html")


class PostFormTest(TestCase):

    image = open("test_img.jpeg", "rb")
    image_dict = {
        "thumbnail": SimpleUploadedFile(
            image.name, image.read(), content_type="image/jpeg"
        ),
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="testuser", email="testuser@gmail.com", password="password"
        )

        cls.post = Post.objects.create(
            title="A good title",
            content="A good body content",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
            slug=slugify("A good title"),
            author=cls.user,
        )

    def test_post_form_valid(self):

        data = {
            "title": "New title",
            "content": "New Body",
        }

        form = PostForm(data, self.image_dict)
        self.assertTrue(form.is_valid())

    # def test_post_write_view(self):
    #     response = self.client.post(
    #         reverse("write"),
    #         {

    #             "title": "New Title",
    #             "content": "New Content",
    #             "thumbnail": SimpleUploadedFile(
    #                 self.image.name, self.image.read(), content_type="image/jpeg"
    #             ),
    #         },
    #     )
    #     self.assertEqual(response.status_code, 302)
