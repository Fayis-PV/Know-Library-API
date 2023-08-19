from django.db import models
import requests
import json
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    description = models.TextField()
    image = models.URLField(blank=True,null=True)
    banners = models.TextField(blank=True,null=True ) 
    category = models.ManyToManyField(Category)
    added_on = models.DateField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

    def add_categories(self, categories):
        """
        Adds categories to the website.

        Parameters:
        - categories: List of categories to be added.
        """
        for category in categories:
            category = Category.objects.get(id = category)
            self.category.add(category)

        
    def to_json(self):
        image_str = str(self.image) if self.image else None
        banners_str = json.loads(self.banners) if self.banners else []
        categories_list = [str(category) for category in self.category.all()] if self.category.exists() else []

        data_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'image': image_str,
            'banners': banners_str,
            'categories': categories_list,
            'active': self.active
        }

        json_data = json.dumps(data_dict)
        return json_data