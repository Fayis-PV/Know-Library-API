from django.urls import path
from .views import *


urlpatterns = [
    path('', home,name='home'),
    path("websites", WebsitesListView.as_view(), name="websites_list"),
    # path('websites/create',WebsitesCreateView.as_view(), name = 'websites_create'),
    path("websites/<int:pk>", WebsitesDetailView.as_view(), name="websites_detail"),
    path("categories", CategoriesListView.as_view(), name="categories"),
    path("categories/<int:pk>", CategoriesDetailView.as_view(), name="categories"),

    # path("auth/admin", AdminAuthView.as_view(), name="admin_login"),
    path("admin", AdminPageView.as_view(), name="admin_page")
    
]
