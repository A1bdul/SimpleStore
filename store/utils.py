import os

import cloudinary
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken

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
    uploader.upload(data, public_id="quickstart_butterfly", unique_filename=False, overwrite=True)

    # Build the URL for the image and save it in the variable 'srcURL'
    src_url = cloudinary.CloudinaryImage("quickstart_butterfly").build_url()

    # Log the image URL to the console.
    # Copy this URL in a browser tab to generate the image on the fly.
    print("****2. Upload an image****\nDelivery URL: ", src_url, "\n")
    return cloudinary.CloudinaryImage('quickstart_butter_fly')


def delete_image(data):
    uploader.destroy(data)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
