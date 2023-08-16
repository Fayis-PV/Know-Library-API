from django.test import TestCase,SimpleTestCase
from .views import *
import random
from django.urls import resolve,reverse

# Create your tests here.

class TestUrls(TestCase):
    def test_websites_list_url(self):
        url = reverse('websites_list')
        self.assertEqual(resolve(url).func.view_class, WebsitesListView)


    def test_websites_detail_url(self):
        pk = 247
        url = reverse('websites_detail',args=[pk])
        self.assertEqual(resolve(url).func.view_class, WebsitesDetailView)

    
    def test_categories_list_url(self):
        url = reverse('categories_list')
        self.assertEqual(resolve(url).func.view_class, CategoriesListView)


    def test_categories_detail_url(self):
        pk = 2
        url = reverse('categories_detail',args=[pk])
        self.assertEqual(resolve(url).func.view_class, CategoriesDetailView)


    def test_admin_page_url(self):
        url = reverse('admin_page')
        self.assertEqual(resolve(url).func.view_class, AdminPageView)