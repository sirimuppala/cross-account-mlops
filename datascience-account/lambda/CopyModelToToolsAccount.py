import urllib
import boto3
import ast
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    print("event is ", event)
    print("context is ", context)

    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print("S3 bucket is ", source_bucket, " and key is ", key)

    # Download the trained model file
    trained_model_file = '/tmp/model.tar.gz'
    s3.download_file(source_bucket, key, trained_model_file)
    print("Model downloaded ", trained_model_file)

    # Assume role to copy over the model to the tools account.
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::480774895708:role/AllowDevToToolsAccess",
        RoleSessionName="cross_acct_lambda"
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    tools_s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    print("tools_s3_client ", tools_s3_client)
    # target_bucket = 'tools-model-artifacts'
    target_bucket = 'mlops-bia-data-smm-7c3f4020'
    target_object = 'models/model.tar.gz'

    with open(trained_model_file, "rb") as f:
        tools_s3_client.upload_fileobj(f, target_bucket, target_object)