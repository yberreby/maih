
import boto3
from IPython.display import Image, display
from PIL import Image as PImage, ImageDraw
import time
from IPython.display import IFrame
import time
import json
import random

def extract_text_from_pdf(bucket, document):
    """
    Extracts text from a PDF document stored in an S3 bucket.
    
    Parameters:
    - bucket: str, the name of the S3 bucket.
    - document: str, the name of the PDF document.
    
    Returns:
    - A list of text extracted from the PDF document.
    """
    mySession = boto3.session.Session()
    awsRegion = mySession.region_name

    s3 = boto3.client('s3')
    textract = boto3.client('textract')
    
    response = textract.start_document_text_detection(
                       DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': document} },
                       ClientRequestToken=str(random.randint(1,1e10)))

    print(response)

    found = False

    while not found:

        jobid = response['JobId']
        n_response = textract.get_document_text_detection(JobId=jobid)
        if n_response["JobStatus"] == "IN_PROGRESS":
            time.sleep(1)
            continue

        for item in n_response["Blocks"]:
            if item["BlockType"] == "LINE":
                found = True
                return (item["Text"])

def main():
    filename = "2002-n°65-Interdiction-aux-vehicules-de-plus-de-35-tonnes-avenue-de-Bordeaux.pdf"
    s3BucketName = "textract-console-eu-west-2-cdc481f3-67d6-4bce-ba92-4c6a125d5f8b"
    extract_text_from_pdf(s3BucketName, filename)