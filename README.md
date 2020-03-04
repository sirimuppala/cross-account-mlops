# cross-account-mlops
MLOps with Amazon Sagemaker and Amazon CodePipeline with multiple AWS accounts

## High Level Steps

1. Create the accounts ()

2. Tools account 
2.1 Login as IT administrator

2.2 Execute the prep cloud formation template from tools-account directory

aws cloudformation deploy --stack-name pre-reqs  --template-file ToolsAcct/pre-reqs.yaml --profile mlops-tools-user 


2.2.1 Make note of S3 bucket
2.2.2 Zip up the lambda files and upload the lambda zip files to the S3 bucket

2.3 Execute the build pipeline template
Note to data S3 bucket and the cross account acess role


3. Datascience / Dev Account
(Note : For Hitachi - Create resources in 3.1 - using service catalog)
Launch the cloudformation template to launch these resources
3.1 S3 bucket; Name - datascience; folders - data, models/development, models/release
3.2 SageMaker notebook
3.3 Upload the python code.
3.4 Copy over the model (and data?? from datascience account??)


