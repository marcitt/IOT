from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)


def upload_image(file_path, bucket_name, supa_path):
    with open(file_path, "rb") as file:
        response = supabase.storage.from_(bucket_name).upload(
            file=file,
            path=supa_path
        )
    return response
# ref: https://supabase.com/docs/reference/python/storage-from-upload
# consider implementing some error-handling code

upload_image(
    "test_image.jpg", bucket_name="iot_images", supa_path="focused/img_1.jpg"
)

# these images can then be accessed in the google colab notebook used for training model 
