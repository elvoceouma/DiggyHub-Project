from google.cloud import storage


def upload_file_to_gcs(file_path, bucket_name, object_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(file_path)


def generate_gcs_download_url(bucket_name, object_name, expiration=3600):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    url = blob.generate_signed_url(expiration=expiration)
    return url


# Specify the file path, bucket name, and object name
file_path = '/path/to/file.txt'
bucket_name = 'your-bucket-name'
object_name = 'file.txt'

# Upload the file to Google Cloud Storage
upload_file_to_gcs(file_path, bucket_name, object_name)
print('File uploaded to Google Cloud Storage')

# Generate a signed URL for downloading the file
download_url = generate_gcs_download_url(bucket_name, object_name)
print('Download URL:', download_url)
