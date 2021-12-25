import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import uuid
from db import *
load_dotenv()

client = os.getenv("ACCESS_ID")
secret = os.getenv("ACCESS_KEY")
bkt = os.getenv("BUCKET")

def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    s3 = boto3.client('s3',
         aws_access_key_id=client,
         aws_secret_access_key=secret)

    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#idx = uuid.uuid4()
#upload_file('/home/pi/scripts/RaspberryPi/Multi_Camera_Adapter/Multi_Adapter_Board_4Channel/Multi_Camera_Adapter_V2.2_python/capture_1.jpg', bkt, str(idx)+'.jpg')
