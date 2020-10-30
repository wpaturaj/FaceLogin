import boto3
import hashlib
import matplotlib.image as mpimg
from io import BytesIO
from botocore.client import Config

def uploadFileS3(data,filePath,ACCESS_KEY_ID,ACCESS_SECRET_KEY,BUCKET_NAME):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(BUCKET_NAME).put_object(Key=filePath, Body=data)
        return True
    except Exception as e:
        print(e)
        return False

def getFileS3(filePath,ACCESS_KEY_ID,ACCESS_SECRET_KEY,BUCKET_NAME):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4'))
        bucket = s3.Bucket(BUCKET_NAME)
        image_object = bucket.Object(filePath)
        image = mpimg.imread(BytesIO(image_object.get()['Body'].read()), 'jp2')
        return image
    except Exception as e:
        print(e)
        return None

        # s3.download_file('your_bucket','k.png','/Users/username/Desktop/k.png')
def hashEmailAddress(email):
    return str(int(hashlib.sha1(email.encode('utf-8')).hexdigest(),16) % (10 ** 32))
