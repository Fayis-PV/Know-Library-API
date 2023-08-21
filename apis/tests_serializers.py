from django.test import TestCase
from .models import Website, Category
from .serializers import WebsiteSerializer, CategorySerializer

class SerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.website_data = {
            'name': 'Test Website',
            'url': 'https://example.com',
            'description': 'Test Description',
            'image':'',
            'banners':'',
            'category': [self.category.id],
            'active': True
        }
        self.website_serializer = WebsiteSerializer(data=self.website_data)

    def test_website_serializer_valid(self):
        self.assertTrue(self.website_serializer.is_valid())

    def test_website_serializer_invalid(self):
        invalid_data = self.website_data.copy()
        invalid_data['name'] = ''  # Blank name
        invalid_serializer = WebsiteSerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())

    def test_website_serializer_create(self):
        self.assertTrue(self.website_serializer.is_valid())
        instance = self.website_serializer.save()
        print(self.website_serializer.validated_data)

        self.assertEqual(instance.name, 'Test Website')
        self.assertEqual(instance.url, 'https://example.com')
        self.assertEqual(instance.description, 'Test Description')
        self.assertTrue(list(instance.category.values_list('id',flat=True)))
        self.assertEqual(instance.category.first(), self.category)
        self.assertTrue(instance.active)

    def test_category_serializer_valid(self):
        category_data = {'name': 'New Category'}
        category_serializer = CategorySerializer(data=category_data)
        self.assertTrue(category_serializer.is_valid())

    def test_category_serializer_invalid(self):
        invalid_data = {'name': ''}  # Blank name
        invalid_serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())

    # Add more tests for other serializers as needed

