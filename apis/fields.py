from rest_framework import serializers
from django.core.files import File

class ImageUrlField(serializers.FileField):
    def to_internal_value(self, data): 
        if data is None:
            return None 
        elif not isinstance(data,File):
            return data
        return super().to_internal_value(data)