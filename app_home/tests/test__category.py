import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from app_home.models import Category, Tag, Blog, BlogImage

import uuid

User = get_user_model()


# -----------------------
# Category Model Tests
# -----------------------
class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Django Testing")

    def test_category_creation(self):
        self.assertEqual(self.category.title, "Django Testing")
        self.assertIsNotNone(self.category.slug)

    def test_slug_generation(self):
        expected_slug = slugify(self.category.title)
        self.assertEqual(self.category.slug, expected_slug)

    def test_str_method(self):
        self.assertEqual(str(self.category), "Django Testing")

    def test_unique_title_constraint(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(title="Django Testing")


# -----------------------
# Tag Model Tests
# -----------------------
class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(title="Python")

    def test_tag_creation(self):
        self.assertEqual(self.tag.title, "Python")
        self.assertIsNotNone(self.tag.slug)

    def test_slug_generation(self):
        expected_slug = slugify(self.tag.title)
        self.assertEqual(self.tag.slug, expected_slug)

    def test_str_method(self):
        self.assertEqual(str(self.tag), "Python")

    def test_unique_title_constraint(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Tag.objects.create(title="Python")


# -----------------------
# Blog Model Tests
# -----------------------
class BlogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="zahid", email="zahidhasan.miluu@gmail.com", password="pass123")
        self.category = Category.objects.create(title="Programming")
        self.tag1 = Tag.objects.create(title="Django")
        self.tag2 = Tag.objects.create(title="Python")
        self.blog = Blog.objects.create(
            author=self.user,
            title="My First Blog",
            content="RichText content here.",
            category=self.category
        )
        self.blog.tags.add(self.tag1, self.tag2)

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, "My First Blog")
        self.assertEqual(self.blog.author.username, "zahid")
        self.assertEqual(self.blog.category.title, "Programming")
        self.assertIsNotNone(self.blog.created_date)
        self.assertIsNotNone(self.blog.updated_date)

    def test_blog_slug_generation(self):
        self.assertIsNotNone(self.blog.slug)
        self.assertIn("-", self.blog.slug)  # because generate_unique_slug adds uuid

    def test_blog_tags(self):
        self.assertEqual(self.blog.tags.count(), 2)
        tags_titles = [tag.title for tag in self.blog.tags.all()]
        self.assertIn("Django", tags_titles)
        self.assertIn("Python", tags_titles)

    def test_str_method(self):
        self.assertEqual(str(self.blog), "My First Blog")

    def test_get_absolute_url(self):
        url = self.blog.get_absolute_url()
        self.assertIn(self.blog.slug, url)


# -----------------------
# BlogImage Model Tests
# -----------------------
class BlogImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="zahid",email = 'zahidhasan.miluu@gmail.com', password="pass123")
        self.category = Category.objects.create(title="Programming")
        self.blog = Blog.objects.create(
            author=self.user,
            title="My Blog with Image",
            content="Some content",
            category=self.category
        )
        # Create a dummy image file
        self.image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'\x00\x01\x02',  # dummy bytes
            content_type='image/png'
        )
        self.blog_image = BlogImage.objects.create(blog=self.blog, image=self.image_file)

    def test_blogimage_creation(self):
        self.assertEqual(str(self.blog_image), self.blog.title)
        # get just the filename, ignore folder
        filename = os.path.basename(self.blog_image.image.name)
        self.assertTrue(filename.startswith('test_image_'))
        self.assertTrue(len(filename) > len('test_image.png'))

    def test_image_filename_sanitization(self):
        # Check that UUID appended to filename
        self.assertIn('_', self.blog_image.image.name)
