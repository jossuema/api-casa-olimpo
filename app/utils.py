from app.config import AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_CONTAINER, AZURE_SAS_READ, AZURE_SAS_WRITE
from azure.storage.blob import BlobServiceClient
from fastapi import File
import uuid

def generate_img_url(img_name: str):
    return f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{img_name}?{AZURE_SAS_READ}"

def generate_img_name(img_name:str):
    extension = img_name.split(".")[-1]
    return f"{uuid.uuid4()}.{extension}"

def upload_img_prenda(img_prenda: File, img_name: str):
    blob_service_client = blob_service_client = BlobServiceClient(f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/?{AZURE_SAS_WRITE}")
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=img_name)
    blob_client.upload_blob(img_prenda.file.read())

def delete_img_prenda(img_name: str):
    blob_service_client = blob_service_client = BlobServiceClient(f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/?{AZURE_SAS_WRITE}")
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=img_name)
    blob_client.delete_blob()

def update_img_prenda(img_prenda: File, img_name: str):
    delete_img_prenda(img_name)
    upload_img_prenda(img_prenda, img_name)