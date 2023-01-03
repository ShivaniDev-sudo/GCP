import base64
from google.cloud import storage

def resize_image(data, context):
  # Get the bucket name and file key from the event data
  bucket_name = data['bucket']
  file_key = data['name']

  # Download the file from GCS
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(file_key)
  image_data = blob.download_as_string()

  # Resize the image
  # (Code to resize the image goes here)

  # Upload the resized image to GCS
  resized_blob = bucket.blob('resized/' + file_key)
  resized_blob.upload_from_string(resized_image_data)

