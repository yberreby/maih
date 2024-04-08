from google.cloud import vision_v1
import re
from google.cloud import storage
import os

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def async_detect_document(gcs_source_uri, gcs_destination_uri, local_download_prefix):
    client = vision_v1.ImageAnnotatorClient()
    feature = vision_v1.Feature(type_=vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION)
    mime_type = 'application/pdf'

    gcs_source = vision_v1.GcsSource(uri=gcs_source_uri)
    input_config = vision_v1.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    gcs_destination = vision_v1.GcsDestination(uri=gcs_destination_uri)
    output_config = vision_v1.OutputConfig(gcs_destination=gcs_destination, batch_size=1)

    async_request = vision_v1.AsyncAnnotateFileRequest(
        features=[feature],
        input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(requests=[async_request])
    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # The output is written to GCS. We list and download files to the local output directory.
    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)

    storage_client = vision_v1.ImageAnnotatorClient().storage_client
    blobs = storage_client.list_blobs(output_bucket, prefix=prefix)
    for blob in blobs:
        local_path = os.path.join(local_download_prefix, os.path.basename(blob.name))
        download_blob(output_bucket, blob.name, local_path)

def main():
    # Configure these variables
    bucket_name = 'YOUR_BUCKET_NAME'
    pdf_file_name = '003-CIRCET-8-8bis-rue-St-Georges-pour-ORANGE.pdf'
    output_prefix = 'parsed'
    local_pdf_path = '../../data'
    local_download_prefix = '../../parsed'

    # Upload the local PDF to GCS
    gcs_source_uri = f'gs://{bucket_name}/{pdf_file_name}'
    upload_blob(bucket_name, local_pdf_path, pdf_file_name)

    # Configure GCS URI for output
    gcs_destination_uri = f'gs://{bucket_name}/{output_prefix}/'

    # Process the PDF with OCR
    async_detect_document(gcs_source_uri, gcs_destination_uri, local_download_prefix)

    # Cleanup: Consider deleting the PDF from GCS if it's no longer needed

if __name__ == '__main__':
    main()