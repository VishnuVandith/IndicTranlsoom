import os
import uuid
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, M2M100Tokenizer, M2M100ForConditionalGeneration
from fastapi import HTTPException
import boto3
from botocore.exceptions import ClientError



AUDIO_DIRECTORY = "audio_files"
os.makedirs(AUDIO_DIRECTORY, exist_ok=True)

def generate_unique_filename(extension: str = ".mp3"):
    return f"{uuid.uuid4()}{extension}"

def get_translation_model(src: str, tgt: str):
    MODEL_MAPPING = {
        "en-es": "Facebook/m2m100_418M",
        "es-en": "Facebook/m2m100_418M",
        "en-de": "Facebook/m2m100_418M",
        "de-en": "Facebook/m2m100_418M",
        "en-ar": "Facebook/m2m100_418M",
        "ar-en": "Facebook/m2m100_418M",
        "en-zh": "Facebook/m2m100_418M",
        "zh-en": "Facebook/m2m100_418M",
    }

    key = f"{src}-{tgt}"
    model_name = MODEL_MAPPING.get(key)

    if not model_name:
        raise HTTPException(status_code=404, detail=f"Translation model for {src} to {tgt} not found.")

    if "m2m100" in model_name:
        tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        model = M2M100ForConditionalGeneration.from_pretrained(model_name)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model

def get_content_type(filename):
        if filename.lower().endswith('.pdf'):
            return 'application/pdf'
        elif filename.lower().endswith('.mp3'):
            return 'audio/mpeg'
        elif filename.lower().endswith('.jpeg'):
            return 'image/jpeg'
        elif filename.lower().endswith('.png'):
            return 'image/PNG'
        elif filename.lower().endswith('.png'):
            return 'image/png'
        elif filename.lower().endswith('.jpg'):
            return 'image/JPG'
        else:
            return 'application/octet-stream'


def s3_utils(filepath: str,filename:str,folder:str):
    s3_client = boto3.client('s3',
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key'),
        region_name='us-east-1'
    )
    
    bucket_name = 'transloom-pdf'
    object_key = folder + filename
    print(object_key)
    
    
    # Upload file
    try:
        with open(filepath, 'rb') as file:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=file,
                ContentType= get_content_type(filename)
            )
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

    # Generate URL
    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name,
                                                       'Key': object_key},
                                               ExpiresIn=3600)  # URL expires in 1 hour
    except ClientError as e:
        print(f"An error occurred: {e}")
        return e

    return url