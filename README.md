# End to end machine learning using multiple AWS accounts across multiple environments.
#### Enable self service capability for data scientist and integrate with automated MLOps.

## Overview
[ABSTRACT]

## Terminology

Few terms to get familiar with before we get started with lab provisioning:

**Tools Account** - An AWS account managed by a centralized IT team, who are responsible for deploying the ML models to production through MLOps code pipeline.
**Data Scientist Account** - An AWS account used by Data Scientists where they could deploy Sagemaker notebooks, run their models, and submit once approved.
**Stage Account** - An AWS account where the code pipeline automatically deploys to and validates the ML models.
**Production Account** - An AWS account where the production applications run. MLOps code pipeline from this lab can be extended to 

**Note:** For this lab, we are are only using Tools, DataScience and Stage accounts. The MLOps pipeline can however be extended to auto-deploy the models to Production environment.

The figure below shows the architecture you will build using this lab.  

![ee-login](images/MLOps_CrossAccount_Architecture.jpg) 

## Steps Involved

**Step-1:** Prepare the Lab environment 
* Configure Service Catalog Product/Portfolio in the Tools Account and share it with a Spoke account (DataScience Account for this lab).
* Configure a Service Catalog Product/Portfolio and other networking resources in the DataScience account and allow access to Data Scientists user/role.
* Configure the stage accounts [Steps]
* Configure MLOps Pipeline in the Tools Account [Steps]

**Step-2:** Data scientists request AWS resources 
* Log in to the DataScience AWS account
* Go to AWS Service Catalog and launch the Sagemaker Notebook instance
* Use the Outputs from AWS Service Catalog and continue with remaining work.

**Step-3:** Data scientists build/train the ML models and submit the final Model.
* Steps to start a notebook
* Steps to build/train the ML model
* Steps to submit the Model to S3 bucket in Tools account

### Step-1 : Prepare the Lab environment

In this section, we will deploy the AWS Service Catalog portfolio in Tools account and share it with the Data scientists account, allow Data scientists to launch SC resources, and setups the ML Codepiepline. For this lab, we will use CloudFormation to create all the required resources.  

Make a note the AWS Account IDs for the Tools, Datascience and Stage accounts provided to you.  You will use these in the steps below.


 
#### Deploy AWS Service Catalog resources

#### Clone or download this git repo
1. Clone or download the zip file of this repo.
2. If you downloaded the zip, unzip the file.

#### Configure  Tools Account
1.1. Log in to your assigned **Tools Account** using the  credentials provided by your lab administrator.

1.2  Setup ServiceCatalog

1.2.1 Copy and paste the below link in your web browser of your Tools Account
https://us-east-2.console.aws.amazon.com/cloudformation#/stacks/new?stackName=LabSCToolsAccountSetup&templateURL=https://marketplace-sa-resources.s3.amazonaws.com/scmlops/prepare_tools_account.yaml

* a. In **Create stack** page, choose **Next**
* b. In **Specify stack details** page, Type in your *DataScience Account Id* under **SpokeAccountID** 
* c. In **Configure stack options** page, leave the defaults and choose **Next**
* d. Scroll down **Review LabSCToolsAccountSetup** page to review the selections and choose **Create stack**
* e. Wait for the stack to deploy resource completely.
* f. Choose **Outputs** section and note down the values of **MasterPortfolioId** and **SagemakerProductID**. You will use this information in next step.
![Outputs Screenshot](images/ToolsAccount_Outputs.png)

1.2.2 Go to Service Catalog Console - https://us-east-2.console.aws.amazon.com/servicecatalog/ and choose **Portfolios** and **Data Scientists - Sample Portfolio**

1.2.3 Choose Actions --> **Share(1)** to list the accounts the portfolio is shared with. Enter the *SpokeAccountID* that you provided as input parameter.

1.3  Setup MLOps Pipeline

1.3.1 Create a CloudFormation stack to prepare deploy lambda functions to be used by MLOps pipeline

* a. In **Create stack** page, choose "Upload a template file", Choose file : tools-account/pipeline/PrepPipeline.yml; Click **Next**
* b. In **Specify stack details** page, type in "MLOpsPipelinePrep" for Stack Name.
* c. In **Configure stack options** page, leave the defaults and choose **Next**
* d. Scroll down **Review** page to review the selections and choose **Create stack**

1.3.2 Upload lambda zip files from the downloaded git repo code to the S3 bucket created in 1.3.1
* a. Upload tools-account/lambda-code/MLOps-BIA-DeployModel.py.zip
* b. Upload tools-account/lambda-code/MLOps-BIA-GetStatus.py.zip
* c. Upload tools-account/lambda-code/MLOps-BIA-EvaluateModel.py.zip

1.3.3 Create a CloudFormation stack to setup the MLOps Code Pipeline
* a. In **Create stack** page, choose "Upload a template file", Choose file : tools-account/pipeline/BuildPipeline.yml; Click **Next**
* b. In **Specify stack details** page, type in "MLOpsPipeline" for Stack Name.
* c. In **Configure stack options** page, type in 'DataScienceAccountID', 'StageAccountID', an UniqueID  and click **Next**
* d. Scroll down **Review** page to review the selections, select checkbox to give permissions to create IAM resources and click  **Create stack**
 

##### Configure DataScience  Account
1.4 Log in to your assigned **Data Scientists Account** using the *Lab Administrator* credentials provided.

**PLEASE READ:** Service Catalog is a regional service. Please make sure you are in the same region where you shared the portfolio from in above section.

1.5 Setup ServiceCatalog
 
1.5.1 Copy and paste the below link in your web browser
https://us-east-2.console.aws.amazon.com/cloudformation#/stacks/new?stackName=LabDSAccountSCSetup&templateURL=https://marketplace-sa-resources.s3.amazonaws.com/scmlops/prepare_datascientist_account.yaml

* a. In **Create stack** page, choose **Next**
* b. Enter the **MasterPortfolioId** and **SagemakerProductID** you noted in Step 1.2.1(f) and choose **Next**.
* c. In **Configure stack options** page, leave the defaults and choose **Next**
* d. Scroll down **Review LabDSAccountSCSetup** page and select **I acknowledge that AWS CloudFormation might create IAM resources** option and choose **Create stack**
* f. Check in the **Outputs** tab, and note down the **SwitchRoleLink** role. You will use the URL link value to switch role as DataScientist in Step-2 below.
![Outputs Screenshot](images/DS-PrepStackOutput.png)

1.6 Create DataScience resources 

1.6.1 Create a CloudFormation stack to create a S3 bucket to hold all training data and model artifacts
* a. In **Create stack** page, choose "Upload a template file", Choose file : datascience-account/CreateDSResources.yml; Click **Next**
* b. In **Specify stack details** page, type in "DSResources" for Stack Name.
* c. In **Configure stack options** page, leave the defaults and choose **Next**
* d. Scroll down **Review** page to review the selections and click  **Create stack**
 
##### Configure Stage Account

1.7 Create Stage account resources 

1.7.1 Create a CloudFormation stack 
* a. In **Create stack** page, choose "Upload a template file", Choose file : stage-account/CreateResources.yml; Click **Next**
* b. In **Specify stack details** page, type in "StageResources" for Stack Name.
* c. In **Configure stack options** page,  type in 'ToolsAccountID' and choose **Next**
* d. Scroll down **Review** page to review the selections and click  **Create stack**


### Step-2 : Data scientists request for AWS resources

In this section, you will login in as a **Data Scientist** and launch a Secure Sagemaker Notebook from the self-service portal powered by AWS Service Catalog.

#### Launch a Sagemaker notebook in Data Scientists account
2.1. Log in to the **Data Scientists** account using the same credentials as you used in step 1.4

2.2. Switch to **Data Scientist** role, using the URL you copied in Step 1.5.1(f)
![Outputs Screenshot](images/DS-SwitchRole.png)

2.3. Under **Find services**, search for and choose **Service Catalog**  

2.4. Now you will see a "Amazon Secure Sagemaker" product under **Products list**. 
![SC Login Screen for Data Scientists](images/DS-ScProduct.png)
**PS:** If you don't see a product in your page, ensure you were able to switch the role properly and also in correct region. You can get this information from the ***top-right corner*** of the page.

* a. Choose the product and click on **LAUNCH PRODUCT** button

* b. Under **Product version** page, enter a name for your service catalog product and choose **NEXT**

* c. Select **SagemakerInstance** notebook instance size (small for the purposes of this lab) and select a team name **TeamName**

* d. In TagOptions page, select a **Value** from drop-down for tag **cost-center** and choose **NEXT**

* e. Leave defaults in **Notifications** page and choose **NEXT**

* f. Under **Review** page, review all the options selected and choose **LAUNCH**

* g. On sucessful completion of the SC product launch, the Data scientist can get the notebook access information on **Outputs** page of the provisioned product (as shown below).
![SC Outputs](images/DS-ProvisionedProduct.png)

* f. Click on **SageMakerNoteBookURL** to open the Notebook interface on the console. Alternatively, Click on **SageMakerNoteBookTerminalURL** to open the Terminal.

* g. Make note of the BucketName value in the outputs.  You will use this in Step 3.

#### Access Sagemaker notebook

### Step-3 : Data scientists build/train the ML models and submit the final Model.

In this step, you will build an XGBoost model in the datascience account and once ready will transfer the model along with test data to IT Tools account.
Open the "xgboost_abalone.ipynb", read the narration and execute the cells.   


#### Walkthrough  of the Codepipeline




## Conclusion

## Clean Up (Optional)

* Stage Account
    1. Empty the S3 bucket with name starting with "mlops-bia-data-" 
    2. Delete the CloudFormation Stack with name "MLOpsResources"
* DataScience Account
    1. Empty the S3 bucket with name starting with "datascience-project" 
    2. Delete the CloudFormation Stack with name "DSEnvironment" (Is this correct??)
*  Tools Account
    1. Empty the S3 bucket with name starting with "mlops-bia-data" 
    2. Empty the S3 bucket with name stating with "mlops-bia-codepipeline-artifacts"
    3. Empty the S3 bucket with name stating with "mlops-bia-lambda-code-"
    4. Delete the CloudFormation Stack with name "MLOpsPipeline"
    5.1 Wait till the MLOpsPipeline is deleted.
    5.2 Delete the CloudFormation Stack with name "MLOpsPipelinePrep" 

---
### !!!!!! WorkLog : Will be removed later

2.4 Launch CloudFormation Stack

aws cloudformation deploy --stack-name pre-reqs  --template-file ToolsAcct/pre-reqs.yaml --profile mlops-tools-user 

3. Prepare the Data Science account.Datascience / Dev Account
(Note : Resources below will be created by the ServiceCatalog in the workshop.  For
now using a cloudformation template)

3.1 Launch the cloudformation template to launch these resources
S3 bucket; Name - datascience; folders - data, models/development, models/release

SageMaker notebook
