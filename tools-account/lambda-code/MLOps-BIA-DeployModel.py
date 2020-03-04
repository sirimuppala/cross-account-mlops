import boto3
import os
import tempfile
import json
from boto3.session import Session

sagemaker = boto3.client('sagemaker')
code_pipeline = boto3.client('codepipeline')


def lambda_handler(event, context):
    try:
        jobName = "datascience-project1"

        # Event is  {'CodePipeline.job': {'id': 'b40ddb4a-8559-4551-bd8d-781f73fcfc2c', 'accountId': '480774895708', 'data': {'actionConfiguration': {'configuration': {'FunctionName': 'MLOps-BIA-DeployModel-smm', 'UserParameters': '{ "InitialInstanceCount": 1, "InitialVariantWeight": 1, "InstanceType": "ml.t2.medium", "EndpointConfigName": "Dev" }'}}, 'inputArtifacts': [{'name': 'SourceArtifact', 'revision': 'HkIrDxS6RdLArKDCEt4HEktdvfdGNLKE', 'location': {'type': 'S3', 's3Location': {'bucketName': 'mlops-bia-codepipeline-artifacts-smm-7c3f4020', 'objectKey': 'ToolsPipeline-CodePi/SourceArti/w6CXMvR.tar.gz'}}}], 'outputArtifacts': [{'name': 'HostingInfo', 'revision': None, 'location': {'type': 'S3', 's3Location': {'bucketName': 'mlops-bia-codepipeline-artifacts-smm-7c3f4020', 'objectKey': 'ToolsPipeline-CodePi/HostingInf/6IOT3Cs'}}}], 'artifactCredentials': {'accessKeyId': 'ASIAW74DKXBOBJCHVX35', 'secretAccessKey': 'tTv1MTrnUSWPyaetxnD7BELKsfJp0Rgnx2Ee2Zbt', 'sessionToken': 'IQoJb3JpZ2luX2VjEDEaCXVzLXdlc3QtMiJIMEYCIQD0cMENm7UNags1MZFnXt3ghWjVXQFiCcI491tMhbf1nQIhAOZ0P8Sb0/zJNX5da69RO/YpPzStL1Q6A2ALopKmzNj6KooFCPr//////////wEQABoMNDgwNzc0ODk1NzA4IgzSr378JLPMr9eJipcq3gTpsjv6wSbjelSRqz0dR00ovWlxy7WMhuJ7B2vl++mB1t6zIiz9JjEHil2jK8hE32xYGWe0E/Gfln8QdjJZ1xHsffRgDnRuoxs0BrTTu0/mmWxA4YLnI3Eam7dmQzUY1m5WxGY7tbBWmGBA16/k2Ezic+/HMyVVSOnqRaRaqPTpBaTbU9ir3ceCboqq/B8dI24W/bu+eqPaNZoC/MaRKrVNriAeJcVaSZl3qqt4tZDm7Uo4lSzEWUPPIu6dPh7xggAalMxZ1JfbP2VeVC9XR65Zj2S3zmH85LtMzl+Cf0YT1tuJhqkiKGTsRHDnTybnZCcCar0zw0Tkor/tLpueJrfVq8urzQ0P3Hhi+kQrwEoXRxc57SPjQNzajBHQJIpuelGQGNEdjf54npktuJjhnODz3v1+lO2xBzZ98Tr5JivPg16NHml7P8Xlnw1EjsORXJjhQd4DTaKgz4ijSHkg0fLARsOwGgzgx/laJiNkDq3p/ZIDJNs7+xf1inp8JZMIOq7HAk5e8f+Loj5iTt4oDADrkiwkoLhVCaV/FVZjfjr6GmlNIvMcTICo8RJXYRtRHPTAQlyoH6EWL/GtPSYAb5qGx/OyFd4DXcGELm/v8vMphjUrtdTBVZok/MocZx6e6oi3Lf4JgdJ84Dqx5trPpOxilvAK3kqo9eJHjh6aqcAJ/VGkhab5+652kR1B67EK2dttCxNFUMUC5WnSQs0fxpV0UJv97KG+cDsibH5tmlJgYvfAMeyXwc0qVftFu4XTe5gJq6oIHokh400Wp7yhGo1Rq9qDCp67eWCr7QQso2Uw14fs8gU6hALtUg32sIx4NFeoJDx5ZrrqNDFbtOnDA+DCyhT+kVYV3/YM9Hu08S/pB8UxaYtc0p9sLbpzhe8/bg1JzefW4FYvHnWCSfP025+fIl9vfreQvc4aPzGSUN9A8n67wwobzNWVOSQ/hjdAUkGZU827w4w6HCD1+YgTTTiKJAZ5TBhY+C883edul+JhcUfSELRDHIlZZINS+4WMfUJRlad8gSGY2ndKc6vjjLxjp1L1ffHppm/Umt4Nol7DcXTR3OtmRlV3q/F6s0d63mHaQJs1uk/R0ANkAPSvddn7c1OH3JbTMoTQQsCehESDOR/wOTJqVMSp827yDY72XgePIxBUtY34H4NZxg==', 'expirationTime': 1583023963000}}}}

        # This is the model.tar.gz
        objectKey = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']

        print("[INFO]Object:", objectKey)

        bucketname = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
        print("[INFO]Bucket:", bucketname)

        print("[INFO]Creating new endpoint configuration")
        configText = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        config_param = json.loads(configText)

        event['stage'] = 'Deployment'
        event['status'] = 'Creating'

        endpoint_environment = config_param["EndpointConfigName"]
        print("[INFO]Endpoint environment:", endpoint_environment)
        initial_variant_weight = config_param['InitialVariantWeight']
        print('[INFO]INITIAL_VARIANT_WEIGHT:', initial_variant_weight)

        # trainingImage = "246618743249.dkr.ecr.us-west-2.amazonaws.com/xgboost:1"
        trainingImage = "433757028032.dkr.ecr.us-west-2.amazonaws.com/xgboost:1"

        # endpoint_environment can be changed based on specific environment setup
        # valid values are 'Dev','Test','Prod'
        # value input below should be representative to the first target environment in your pipeline (typically Dev or Test)

        # modelArtifact = 'https://s3.mlops-bia-codepipeline-artifacts-smm-7c3f4020.amazonaws.com/ToolsPipeline-CodePi/SourceArti/0A24plI.tar.gz'

        # modelArtifact = 'https://{}.s3-{}.amazonaws.com/{}/{}'.format(bucket, region, prefix,MOVIE_RECOMMENDATION_MODEL)

        # modelArtifact = 'https://mlops-bia-codepipeline-artifacts-smm-7c3f4020.amazonaws.s3-us-west-2.amazonaws.com/ToolsPipeline-CodePi/SourceArti/0A24plI.tar.gz'

        ##TODO : Should not be hardcoded.
        modelArtifact = 'https://mlops-bia-data-smm-7c3f4020.s3-us-west-2.amazonaws.com/models/model.tar.gz'

        if endpoint_environment == 'Dev':
            print("[INFO]Environment Input is Dev so Creating model resource from training artifact")
            create_model(jobName, trainingImage, modelArtifact)
        else:
            print("[INFO]Environment Input is not equal to Dev meaning model already exists - no need to recreate")

        endpoint_config_name = jobName + '-' + endpoint_environment
        print("[INFO]EndpointConfigName:", endpoint_config_name)

        event['message'] = 'Creating Endpoint Hosting"{} started."'.format(endpoint_config_name)

        create_endpoint_config(jobName, endpoint_config_name, config_param, initial_variant_weight)

        # TO DO
        # if initial_variant_weight == 1:
        # CleanUp old endpoint to avoid additional charges
        #    clean_up_oldendpoints(endpoint_environment)
        # else:
        #    print("[INFO] Initial variant is not 1")

        create_endpoint(endpoint_config_name)

        event['models'] = 'ModelName:"'.format(jobName)
        event['status'] = 'InService'
        event['endpoint'] = endpoint_config_name
        event['endpoint_config'] = endpoint_config_name
        event['job_name'] = jobName

        write_job_info_s3(event)
        put_job_success(event)

    except Exception as e:
        print(e)
        print('Unable to create deployment job.')
        event['message'] = str(e)
        put_job_failure(event)

    print("Returning the event ", event)

    return event


def lambda_handler_old(event, context):
    try:
        # Read in information from previous get_status job
        previousStepEvent = read_job_info(event)

        # print("[INFO]previousStepEvent:", previousStepEvent)

        # print("Event is ", event)

        # Event is  {'CodePipeline.job': {'id': 'b40ddb4a-8559-4551-bd8d-781f73fcfc2c', 'accountId': '480774895708', 'data': {'actionConfiguration': {'configuration': {'FunctionName': 'MLOps-BIA-DeployModel-smm', 'UserParameters': '{ "InitialInstanceCount": 1, "InitialVariantWeight": 1, "InstanceType": "ml.t2.medium", "EndpointConfigName": "Dev" }'}}, 'inputArtifacts': [{'name': 'SourceArtifact', 'revision': 'HkIrDxS6RdLArKDCEt4HEktdvfdGNLKE', 'location': {'type': 'S3', 's3Location': {'bucketName': 'mlops-bia-codepipeline-artifacts-smm-7c3f4020', 'objectKey': 'ToolsPipeline-CodePi/SourceArti/w6CXMvR.tar.gz'}}}], 'outputArtifacts': [{'name': 'HostingInfo', 'revision': None, 'location': {'type': 'S3', 's3Location': {'bucketName': 'mlops-bia-codepipeline-artifacts-smm-7c3f4020', 'objectKey': 'ToolsPipeline-CodePi/HostingInf/6IOT3Cs'}}}], 'artifactCredentials': {'accessKeyId': 'ASIAW74DKXBOBJCHVX35', 'secretAccessKey': 'tTv1MTrnUSWPyaetxnD7BELKsfJp0Rgnx2Ee2Zbt', 'sessionToken': 'IQoJb3JpZ2luX2VjEDEaCXVzLXdlc3QtMiJIMEYCIQD0cMENm7UNags1MZFnXt3ghWjVXQFiCcI491tMhbf1nQIhAOZ0P8Sb0/zJNX5da69RO/YpPzStL1Q6A2ALopKmzNj6KooFCPr//////////wEQABoMNDgwNzc0ODk1NzA4IgzSr378JLPMr9eJipcq3gTpsjv6wSbjelSRqz0dR00ovWlxy7WMhuJ7B2vl++mB1t6zIiz9JjEHil2jK8hE32xYGWe0E/Gfln8QdjJZ1xHsffRgDnRuoxs0BrTTu0/mmWxA4YLnI3Eam7dmQzUY1m5WxGY7tbBWmGBA16/k2Ezic+/HMyVVSOnqRaRaqPTpBaTbU9ir3ceCboqq/B8dI24W/bu+eqPaNZoC/MaRKrVNriAeJcVaSZl3qqt4tZDm7Uo4lSzEWUPPIu6dPh7xggAalMxZ1JfbP2VeVC9XR65Zj2S3zmH85LtMzl+Cf0YT1tuJhqkiKGTsRHDnTybnZCcCar0zw0Tkor/tLpueJrfVq8urzQ0P3Hhi+kQrwEoXRxc57SPjQNzajBHQJIpuelGQGNEdjf54npktuJjhnODz3v1+lO2xBzZ98Tr5JivPg16NHml7P8Xlnw1EjsORXJjhQd4DTaKgz4ijSHkg0fLARsOwGgzgx/laJiNkDq3p/ZIDJNs7+xf1inp8JZMIOq7HAk5e8f+Loj5iTt4oDADrkiwkoLhVCaV/FVZjfjr6GmlNIvMcTICo8RJXYRtRHPTAQlyoH6EWL/GtPSYAb5qGx/OyFd4DXcGELm/v8vMphjUrtdTBVZok/MocZx6e6oi3Lf4JgdJ84Dqx5trPpOxilvAK3kqo9eJHjh6aqcAJ/VGkhab5+652kR1B67EK2dttCxNFUMUC5WnSQs0fxpV0UJv97KG+cDsibH5tmlJgYvfAMeyXwc0qVftFu4XTe5gJq6oIHokh400Wp7yhGo1Rq9qDCp67eWCr7QQso2Uw14fs8gU6hALtUg32sIx4NFeoJDx5ZrrqNDFbtOnDA+DCyhT+kVYV3/YM9Hu08S/pB8UxaYtc0p9sLbpzhe8/bg1JzefW4FYvHnWCSfP025+fIl9vfreQvc4aPzGSUN9A8n67wwobzNWVOSQ/hjdAUkGZU827w4w6HCD1+YgTTTiKJAZ5TBhY+C883edul+JhcUfSELRDHIlZZINS+4WMfUJRlad8gSGY2ndKc6vjjLxjp1L1ffHppm/Umt4Nol7DcXTR3OtmRlV3q/F6s0d63mHaQJs1uk/R0ANkAPSvddn7c1OH3JbTMoTQQsCehESDOR/wOTJqVMSp827yDY72XgePIxBUtY34H4NZxg==', 'expirationTime': 1583023963000}}}}

        jobName = previousStepEvent['TrainingJobName']
        jobArn = previousStepEvent['TrainingJobArn']
        print("[INFO]TrainingJobName:", jobName)
        print("[INFO]TrainingJobArn:", jobArn)
        modelArtifact = previousStepEvent['ModelArtifacts']['S3ModelArtifacts']
        print("[INFO]Model Artifacts:", modelArtifact)
        trainingImage = previousStepEvent['AlgorithmSpecification']['TrainingImage']
        print("[INFO]TrainingImage:", trainingImage)

        print("[INFO]Creating new endpoint configuration")
        configText = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        config_param = json.loads(configText)

        event['stage'] = 'Deployment'
        event['status'] = 'Creating'

        endpoint_environment = config_param["EndpointConfigName"]
        print("[INFO]Endpoint environment:", endpoint_environment)
        initial_variant_weight = config_param['InitialVariantWeight']
        print('[INFO]INITIAL_VARIANT_WEIGHT:', initial_variant_weight)

        # endpoint_environment can be changed based on specific environment setup
        # valid values are 'Dev','Test','Prod'
        # value input below should be representative to the first target environment in your pipeline (typically Dev or Test)
        if endpoint_environment == 'Dev':
            print("[INFO]Environment Input is Dev so Creating model resource from training artifact")
            create_model(jobName, trainingImage, modelArtifact)
        else:
            print("[INFO]Environment Input is not equal to Dev meaning model already exists - no need to recreate")

        endpoint_config_name = jobName + '-' + endpoint_environment
        print("[INFO]EndpointConfigName:", endpoint_config_name)

        event['message'] = 'Creating Endpoint Hosting"{} started."'.format(endpoint_config_name)

        create_endpoint_config(jobName, endpoint_config_name, config_param, initial_variant_weight)

        # TO DO
        # if initial_variant_weight == 1:
        # CleanUp old endpoint to avoid additional charges
        #    clean_up_oldendpoints(endpoint_environment)
        # else:
        #    print("[INFO] Initial variant is not 1")

        create_endpoint(endpoint_config_name)

        event['models'] = 'ModelName:"'.format(jobName)
        event['status'] = 'InService'
        event['endpoint'] = endpoint_config_name
        event['endpoint_config'] = endpoint_config_name
        event['job_name'] = jobName

        write_job_info_s3(event)
        put_job_success(event)

    except Exception as e:
        print(e)
        print('Unable to create deployment job.')
        event['message'] = str(e)
        put_job_failure(event)

    return event


def create_model(jobName, trainingImage, modelArtifact):
    """ Create SageMaker model.
    Args:
        jobName (string): Name to label model with
        trainingImage (string): Registry path of the Docker image that contains the model algorithm
        modelArtifact (string): URL of the model artifacts created during training to download to container
    Returns:
        (None)
    """
    # Role to pass to SageMaker training job that has access to training data in S3, etc
    SageMakerRole = os.environ['SageMakerExecutionRole']

    try:
        response = sagemaker.create_model(
            ModelName=jobName,
            PrimaryContainer={
                'Image': trainingImage,
                'ModelDataUrl': modelArtifact
            },
            ExecutionRoleArn=SageMakerRole
        )
    except Exception as e:
        print(e)
        print("ERROR:", "create_model", response)
        raise (e)


def create_endpoint_config(jobName, endpoint_config_name, config_param, initial_variant_weight):
    """ Create SageMaker endpoint configuration.
    Args:
        jobName (string): Name to label endpoint configuration with. For easy identification of model deployed behind endpoint the endpoint name will match the trainingjob
    Returns:
        (None)

        { "InitialInstanceCount": "1", "InitialVariantWeight": "1", "InstanceType": "ml.t2.medium", "EndpointConfigName": "Dev" }
    """
    try:

        deploy_instance_type = config_param['InstanceType']
        initial_instance_count = config_param['InitialInstanceCount']
        print('[INFO]DEPLOY_INSTANCE_TYPE:', deploy_instance_type)
        print('[INFO]INITIAL_INSTANCE_COUNT:', initial_instance_count)

        response = sagemaker.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    'VariantName': 'AllTraffic',
                    'ModelName': jobName,
                    'InitialInstanceCount': initial_instance_count,
                    'InitialVariantWeight': initial_variant_weight,
                    'InstanceType': deploy_instance_type,
                }
            ]
        )
        print("[SUCCESS]create_endpoint_config:", response)
        return response
    except Exception as e:
        print(e)
        print("[ERROR]create_endpoint_config:", response)
        raise (e)


def create_endpoint(endpoint_config_name):
    print("[INFO]Creating Endpoint")
    """ Create SageMaker endpoint with input endpoint configuration.
    Args:
        jobName (string): Name of endpoint to create.
        EndpointConfigName (string): Name of endpoint configuration to create endpoint with.
    Returns:
        (None)
    """
    try:
        response = sagemaker.create_endpoint(
            EndpointName=endpoint_config_name,
            EndpointConfigName=endpoint_config_name
        )

        print("[SUCCESS]create_endpoint:", response)
        return response

    except Exception as e:
        print(e)
        print("[ERROR]create_endpoint:", response)
        raise (e)


def update_endpoint(endpoint_name, config_name):
    """ Update SageMaker endpoint to input endpoint configuration.
    Args:
        endpoint_name (string): Name of endpoint to update.
        config_name (string): Name of endpoint configuration to update endpoint with.
    Returns:
        (None)
    """
    try:
        sagemaker.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=config_name
        )
    except Exception as e:
        print(e)
        print("[ERROR]update_endpoint:", e)
        raise (e)


def read_job_info(event):
    tmp_file = tempfile.NamedTemporaryFile()

    # objectKey = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']
    objectKey = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']

    print("[INFO]Object:", objectKey)

    bucketname = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
    print("[INFO]Bucket:", bucketname)

    artifactCredentials = event['CodePipeline.job']['data']['artifactCredentials']

    session = Session(aws_access_key_id=artifactCredentials['accessKeyId'],
                      aws_secret_access_key=artifactCredentials['secretAccessKey'],
                      aws_session_token=artifactCredentials['sessionToken'])

    s3 = session.resource('s3')

    obj = s3.Object(bucketname, objectKey)

    item = json.loads(obj.get()['Body'].read().decode('utf-8'))

    print("Item:", item)

    return item


def write_job_info_s3(event):
    print(event)

    objectKey = event['CodePipeline.job']['data']['outputArtifacts'][0]['location']['s3Location']['objectKey']

    bucketname = event['CodePipeline.job']['data']['outputArtifacts'][0]['location']['s3Location']['bucketName']

    artifactCredentials = event['CodePipeline.job']['data']['artifactCredentials']

    artifactName = event['CodePipeline.job']['data']['outputArtifacts'][0]['name']

    # S3 Managed Key for Encryption
    S3SSEKey = os.environ['SSEKMSKeyIdIn']

    json_data = json.dumps(event)
    print(json_data)

    session = Session(aws_access_key_id=artifactCredentials['accessKeyId'],
                      aws_secret_access_key=artifactCredentials['secretAccessKey'],
                      aws_session_token=artifactCredentials['sessionToken'])

    s3 = session.resource("s3")
    # object = s3.Object(bucketname, objectKey + '/event.json')
    object = s3.Object(bucketname, objectKey)
    print(object)
    object.put(Body=json_data, ServerSideEncryption='aws:kms', SSEKMSKeyId=S3SSEKey)
    print('event written to s3')


def put_job_success(event):
    print("[SUCCESS]Endpoint Deployed")
    print(event['message'])
    code_pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])


def put_job_failure(event):
    print('[ERROR]Putting job failure')
    print(event['message'])
    code_pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])