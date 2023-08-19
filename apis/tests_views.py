from django.test import TestCase,Client
from .views import *
from django.urls import reverse,resolve
from .models import Website,Category
from rest_framework.test import APITestCase,APIClient
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_website_list_get_view(self):
        Website.objects.create(name='Website 1', url='https://example.com', description='Description 1')
        Website.objects.create(name='Website 2', url='https://example.org', description='Description 2')

        response = self.client.get(reverse('websites_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Website.objects.count(),2)

    
    def test_categories_list_get_view(self):
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        response = self.client.get(reverse('categories_list'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(Category.objects.count(),2)

    
class TestAuthView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testname', password='testpas')
        self.refresh = RefreshToken.for_user(self.user)


    def test_create_website_authenticated(self):
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        data = {
            "name": "Test Website",
            "url": 'http://example.com/',
            "description": 'Test description',
            "image": '',
            "banners": '',
            "category": [category1.id, category2.id],
        }

        url = reverse('websites_list')  # Replace with your URL name

        # Generate a valid access token
        access_token = str(self.refresh.access_token)

        # Set the Authorization header with the access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Website.objects.count(), 1)

        website = Website.objects.first()
        self.assertEqual(website.name, 'Test Website')
    

    def test_website_detail_update_view(self):
        access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        category1 = Category.objects.create(name='Category 1')
        website1 = Website.objects.create(name='Website 1', url='https://example.com', description='Description 1')
        data = {
            'name': 'Update for test',
            'description': 'Updated description',  # Include description
            'url': 'https://example.com',          # Include URL
            'image': '',                            # Include image (can be an empty string if not applicable)
            'banners': '',                          # Include banners (can be an empty string if not applicable)
            'category': [category1.id],            # Include category
        }

        response = self.client.put(reverse('websites_detail',args=[website1.id]),data,format = 'json',)
        self.assertEqual(response.status_code,200)

    def test_website_detail_delete_view(self):
        access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        category1 = Category.objects.create(name='Category 1')
        website1 = Website.objects.create(name='Website 1', url='https://example.com', description='Description 1')

        response = self.client.delete(reverse('websites_detail',args=[website1.id]),format = 'json',)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


    def test_website_create_unauthenticated(self):
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        data = {
            "name": "Test Website",
            "url": 'http://example.com/',
            "description": 'Test description',
            "image": '',
            "banners": '',
            "category": [category1.id, category2.id],
        }

        url = reverse('websites_list')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_website_put_unauthorized(self):
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        website1 = Website.objects.create(name='Website 1', url='https://example.com', description='Description 1')
        data = {
            'name': 'Update for test',
            'description': 'Updated description',  # Include description
            'url': 'https://example.com',          # Include URL
            'image': '',                            # Include image (can be an empty string if not applicable)
            'banners': '',                          # Include banners (can be an empty string if not applicable)
            'category': [category1.id],            # Include category
        }

        response = self.client.put(reverse('websites_detail',args=[website1.id]),data,format = 'json',)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_website_detail_delete_unauthorized(self):
        category1 = Category.objects.create(name='Category 1')
        website1 = Website.objects.create(name='Website 1', url='https://example.com', description='Description 1')

        response = self.client.delete(reverse('websites_detail',args=[website1.id]),format = 'json',)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

