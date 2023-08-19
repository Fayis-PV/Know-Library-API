from django.test import TestCase
from .models import Category,Website
import json
from django.db import IntegrityError


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')

    def test_category_name(self):
        self.assertEqual(str(self.category), 'TestCategory')  # Test __str__ method

    def test_category_creation(self):
        category = Category.objects.get(name='TestCategory')
        self.assertEqual(category.name, 'TestCategory')


class WebsiteModelTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.website = Website.objects.create(name='Test Website', url='https://example.com', description='Test Description')

    def test_add_categories(self):
        # Add categories to the website
        self.website.add_categories([self.category1.id, self.category2.id])
        
        # Check if categories are added correctly
        self.assertEqual(self.website.category.count(), 2)

    def test_to_json(self):
        # Create sample data for the website
        self.website.image = 'https://example.com/image.jpg'
        self.website.banners = ['https://example.com/banner1.jpg', 'https://example.com/banner2.jpg']
        self.website.save()

        # Get the JSON representation of the website
        website_json = self.website.to_json()

        # Parse the JSON and check for specific values
        parsed_json = json.loads(website_json)
        self.assertEqual(parsed_json['name'], 'Test Website')
        self.assertEqual(parsed_json['image'], 'https://example.com/image.jpg')
        self.assertEqual(parsed_json['banners'][0], 'https://example.com/banner1.jpg')

# Note: Make sure to adjust the imports and model names based on your actual project structure.