# Trigger Cloud Function or lambda is trigger via event ie. whenever there is metadata change on file metadata on cloud storage such as file is renmaed of 1.jpg to 1.png etc.

def metadata_change(event, context):
  # Get the bucket and file name from the event data
  bucket_name = event['bucket']
  file_name = event['name']

  # Create a Storage client
  storage_client = storage.Client()

  # Get the file from the bucket
  bucket = storage_client.get_bucket(bucket_name)
  file = bucket.get_blob(file_name)

  # Print the updated metadata of the file
  print(f'File {file_name} in bucket {bucket_name} was updated with the following metadata:')
  print(file.metadata)
