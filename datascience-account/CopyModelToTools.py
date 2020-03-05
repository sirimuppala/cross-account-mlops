import boto3

s3 = boto3.client('s3')

##Variables to set
target_bucket = 'mlops-bia-data-smm-40527430'
target_object = 'models/model.tar.gz'
target_validation_data_tools = 'data/validation_data_tools.csv'
# target_validation_data_prod = 'data/validation_data_prod.csv' ##IS THIS NEEDED?

source_bucket = 'datascience-project-smm-b2fc41b0'
tools_account_access_arn = 'arn:aws:iam::480774895708:role/AllowAccessToDevAccountRole-smm-40527430'

key = 'model.tar.gz'
validation_data_file_tools = 'validation_tools.csv'
validation_data_file_prod = 'validation_prod.csv'

print("S3 bucket is ", source_bucket, " model is: ", key, " validation data for tools: ", validation_data_file_tools,
      " validation data for prod: ", validation_data_file_prod)

# Download the trained model file
trained_model_file = 'local-model.tar.gz'
s3.download_file(source_bucket, key, trained_model_file)
print("Model downloaded ", trained_model_file)

# Download the validation files
local_validation_data_file_tools = 'data/smoketest.csv'
# local_validation_data_file_prod='local_validation_prod.csv'

s3.download_file(source_bucket, key, trained_model_file)
# s3.download_file(source_bucket, key, local_validation_data_file_tools)
# s3.download_file(source_bucket, key, local_validation_data_file_prod)
print("Model downloaded ", trained_model_file)
print("Validation data for tools account downloaded ", local_validation_data_file_tools)
# print("validation data for production downloaded ", local_validation_data_file_prod)

sts_connection = boto3.client('sts')
acct_b = sts_connection.assume_role(
    RoleArn=tools_account_access_arn,
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

with open(trained_model_file, "rb") as f:
    tools_s3_client.upload_fileobj(f, target_bucket, target_object)

with open(local_validation_data_file_tools, "rb") as f:
    tools_s3_client.upload_fileobj(f, target_bucket, target_validation_data_tools)

