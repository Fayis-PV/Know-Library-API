import requests
from urllib.request import urlopen
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

class RemoteStorage:
    IMGUR_CLIENT_ID = "a8a3eb4b42eafb8"

    @staticmethod
    def save_img(image):
        """
        Uploads the image to Imgur using its API and returns the URL of the uploaded image.

        Parameters:
        - image: The image data (file-like object or URL).

        Returns:
        - The URL of the uploaded image if successful, otherwise None.
        """

        url = "https://api.imgur.com/3/upload"
        headers = {
            "Authorization": f"Client-ID {RemoteStorage.IMGUR_CLIENT_ID}",
        }
        if isinstance(image, (UploadedFile)):
            image_data = image.read()
        elif isinstance(image, str):
            try:
                response = urlopen(image)
                if response:
                    image_data = response.read()
                else:
                    raise ValidationError('Invalid URL. Please provide a valid URL.')
            except Exception as e:
                raise ValidationError('Invalid URL. Please provide a valid URL.') from e
        else:
            raise ValidationError('Invalid image data.')

        payload = {
            "image": image_data,
        }

        try:
            response = requests.post(url, headers=headers, files=payload)
            data = response.json()
            if response.status_code == 200 and data.get("success", False):
                return data["data"]["link"]
            else:
                print(f"Error uploading image: {data['error']}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error uploading image: {e}")
            return None

    @staticmethod
    def save_image(request):
        image = request.data.get('image')
        if image in ('',None):
            return None
        image_link = RemoteStorage.save_img(image)
        return image_link
    
    @staticmethod
    def save_banners(request):
        banners = request.data.getlist('banners')
        banners_list = []
        for banner in banners:
            if banner in ('',None):
                return None
            banner_link = RemoteStorage.save_img(banner)
            if banner_link:
                banners_list.append(banner_link)
        return banners_list

