import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.core.files import File
from urllib.request import urlopen

class RemoteStorage(Storage):
    def save_image( request):
        """
        Uploads the image to Imgur using its API and saves the URL of the uploaded image to the model.

        Parameters:
        - request: The HTTP request containing the image data.

        Returns:
        - True if the image upload is successful, otherwise False.
        """


        url = "https://api.imgur.com/3/upload"
        image = request.data.get('image')
        if image == '' or None:
            return None
        elif isinstance(image,File):
            if hasattr(image,'temporary_file_path'):
                path = image.temporary_file_path()
            else:
                path = None
            print(path)
            with open(path, "rb") as image_file:
                image_data = image_file.read()
        elif isinstance(image,str):
            try:
                response = urlopen(image)
                if response:
                    return image
                else:
                    raise ValueError('Invalid Url. Please give a valid url')
                return False
            except Exception as e:
                # raise ValueError('Invalid Url. Please give a valid Url') 
                return 'Given not a valid file not a Url. Please submit a valid one: \n',e
        else:
            return None

        headers = {
            "Authorization": "Client-ID a8a3eb4b42eafb8",
        }

        payload = {
            "image": image_data,
        }

        try:
            response = requests.post(url, headers=headers, files=payload)
            data = response.json()
            if response.status_code == 200 and data.get("success", False):
                image = data["data"]["link"]
                return image
            else:
                print(f"Error uploading image: {data['error']}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error uploading image: {e}")
            return False
        
    def save_banners(request):

        url = "https://api.imgur.com/3/upload"
        banners = request.data.getlist('banners')
        banners_list = []
        for banner in banners:
            if banner == '' or None:
                return None
            elif isinstance(banner,File):
                if hasattr(banner,'temporary_file_path'):
                    path = banner.temporary_file_path()
                else:
                    path = None
                print(path)
                with open(path, "rb") as banner_file:
                    banner_data = banner_file.read()
            elif isinstance(banner,str):
                try:
                    response = urlopen(banner)
                    if response:
                        return banner
                    else:
                        return ValueError('Invalid Url. Please give a valid Url') 
                except Exception as e:
                    return 'Given banners are not valid.',e
            else:
                return None

            headers = {
                "Authorization": "Client-ID a8a3eb4b42eafb8",
            }

            payload = {
                'image': banner_data,
            } 

            try:  
                response = requests.post(url, headers=headers, files=payload)
                data = response.json()
                print(data.get('status'),data.get('data'))
                if response.status_code == 200 and data.get('success',True):
                    banner_link = data.get('data').get('link')
                    banners_list.append(banner_link)
                    # return banner_link
                else:
                    print('Error in uploading Images. Try again')
                    return False
            except Exception as e:
                print('Error Occured: ',e)
                return False
        return banners_list
