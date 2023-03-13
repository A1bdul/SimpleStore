import os

import cloudinary
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Images

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('cloud_name'),
    api_key=os.getenv('api_key'),
    api_secret=os.getenv('api_secret'),
    api_proxy="http://proxy.server:9999"
)

import cloudinary.uploader as uploader
import cloudinary.api


def upload_image(data):
    # Upload the image and get its URL
    # ==============================

    # Upload the image.
    # Set the asset's public ID and allow overwriting the asset with new versions
    photo = uploader.upload(data, overwrite=True)

    # Build the URL for the image and save it in the variable 'srcURL'
    src_url = cloudinary.CloudinaryImage(photo['public_id'])

    return Images.objects.create(image=src_url)


def delete_image(data):
    uploader.destroy(data)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
