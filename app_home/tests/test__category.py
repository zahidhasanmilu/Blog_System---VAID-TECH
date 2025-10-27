from django.test import TestCase
from django.utils.text import slugify
from app_home.models import Category

class CategoryModelTest(TestCase):

    def setUp(self):
        # Test এর জন্য একটি category তৈরি
        self.category = Category.objects.create(title="Django Testing")

    def test_category_creation(self):
        """Category object ঠিক তৈরি হচ্ছে কিনা"""
        self.assertEqual(self.category.title, "Django Testing")
        self.assertIsNotNone(self.category.slug)  # slug auto generate হয়েছে কিনা

    def test_slug_generation(self):
        """slug ঠিকভাবে তৈরি হচ্ছে কিনা"""
        expected_slug = slugify(self.category.title)
        self.assertEqual(self.category.slug, expected_slug)

    # def test_str_method(self):
    #     """__str__ method ঠিক কাজ করছে কিনা"""
    #     self.assertEqual(str(self.category), "Django Testing")

    def test_unique_title_constraint(self):
        """একই title আবার create করলে IntegrityError হবে কিনা"""
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(title="Django Testing")
