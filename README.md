# cross-account-mlops
MLOps with Amazon Sagemaker and Amazon CodePipeline with multiple AWS accounts

## High Level Steps

1. Prepare for the workshop

1.1 You will need three different AWS accounts for this workshop. Note down the AWS Account IDs.

2. Prepare the IT Tools account.

2.1 Login to IT Tools AWS account.

2.2 Launch CloudFormation Stack



2.3 Upload lambda zip files to the S3 bucket created in 2.2

* tools-account/lambda-code/MLOps-BIA-DeployModel.py.zip
* tools-account/lambda-code/MLOps-BIA-GetStatus.py.zip
* tools-account/lambda-code/MLOps-BIA-EvaluateModel.py.zip
* tools-account/lambda-code/MLOps-BIA-TrainModel.py.zip
 
2.4 Launch CloudFormation Stack

aws cloudformation deploy --stack-name pre-reqs  --template-file ToolsAcct/pre-reqs.yaml --profile mlops-tools-user 


3. Prepare the Data Science account.Datascience / Dev Account
(Note : Resources below will be created by the ServiceCatalog in the workshop.  For
now using a cloudformation template)

3.1 Launch the cloudformation template to launch these resources
S3 bucket; Name - datascience; folders - data, models/development, models/release

SageMaker notebook

3.2 
3.3 Upload the python code.
3.4 Copy over the model (and data?? from datascience account??)


