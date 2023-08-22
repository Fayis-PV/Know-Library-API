from django.urls import path
from .views import *

app_name = 'apis'
urlpatterns = [
    path('', home,name='home'),
    path("websites", WebsitesListView.as_view(), name="websites_list"),
    path("websites/<int:pk>", WebsitesDetailView.as_view(), name="websites_detail"),
    path("categories", CategoriesListView.as_view(), name="categories_list"),
    path("categories/<int:pk>", CategoriesDetailView.as_view(), name="categories_detail"),

    path('signup', CustomSignupView.as_view(), name='signup'),
    path('login',CustomLoginView.as_view(),name= 'login'),
    path('logout',CustomLogoutView.as_view(),name= 'logout'),
    path("admin", AdminPageView.as_view(), name="admin_page"),
]
