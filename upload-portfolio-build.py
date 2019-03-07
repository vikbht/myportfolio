import json
import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes

def lambda_handler(event, context):

    
    s3=boto3.resource('s3', config=Config(signature_version='s3v4'))
    
    porfolio_bucket = s3.Bucket('pfvb')
    porfolio_bucket_build = s3.Bucket('pfvb-build')
    
    portfolio_zip = io.BytesIO()
    
    porfolio_bucket_build.download_fileobj('portfoliobuild.zip', portfolio_zip)
    
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            porfolio_bucket.upload_fileobj(obj,nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            porfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            
    return 'Lambda invoked'
