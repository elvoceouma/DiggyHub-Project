from azure.storage.blob import BlobServiceClient
import datetime
from datetime import timedelta
from app import output_path


file_path = output_path
# Define your Azure Blob Storage connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=diggyhubreceipts;AccountKey=pkJlnVNulbXLRbdOG1c4hVwwa0fFs4rUQophJCVimqHBco/5eDqrlmhafWj3+roAPb6rbp50L33D+AStyC2PDg==;EndpointSuffix=core.windows.net"

try:
    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)

    def upload_file_to_azure(file_path, container_name, blob_name):
        try:
            # Get a blob client for the specified container and blob
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=blob_name)

            # Upload the file to Azure Blob Storage
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
        except Exception as e:
            print("Error uploading file to Azure Blob Storage:")
            print(str(e))

    def generate_azure_download_url(container_name, blob_name, expiration=3600):
        try:
            # Get a blob client for the specified container and blob
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=blob_name)

            # Generate a shared access signature (SAS) URL with read permission
            url = blob_client.generate_shared_access_signature(
                permission="r",
                expiry=datetime.datetime.utcnow() + timedelta(seconds=expiration)
            )

            # Combine the blob URL and SAS token to create the download URL
            download_url = f"{blob_client.url}?{url}"
            print(download_url)
        except Exception as e:
            print("Error generating Azure Blob Storage download URL:")
            print(str(e))

except Exception as e:
    print("Error creating Azure BlobServiceClient:")
    print(str(e))
