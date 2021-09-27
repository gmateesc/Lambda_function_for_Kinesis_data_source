# Lambda_function_for_Kinesis_data_source

Implement a Lambda function that consumes events from Kinesis and exports them to S3.


```
Part I: Create Lambda Function that is connected to a Kinesis Data Source
==========================================================================




1. Prerequisites



2. AWS Version



3. Create the execution role and add policies
    
    3.1 Overview

    3.2 Create the lambda-kinesis-role-from-console role from the IAM console




4. Create the lambda function, invoke it and get logs


    4.1 Create the function code and deployment package
    
         4.1.1 Function source code
	 
         4.1.2 Create a deployment package



    4.2 Create lambda function resource

         4.2.1 Check config with the CLI

         4.2.2 Check role "lambda-kinesis-role-created-from-console"

                4.2.2.1 Check with the UI

                4.2.2.2 Check with the CLI
                         4.2.2.2.1 aws iam list-roles
                         4.2.2.2.2 aws iam get-role --role-name ROLE_NAME

         4.2.3 Create function resource with the CLI

         4.2.4 Show the lambda function
                4.2.4.1 In the UI
                4.2.4.2 In the CLI




    4.3 Test the lambda function

         4.3.1 Raw binary vs base64 input files

         4.3.1 Create the input file

         4.3.3 Invoke lambda func with a sample event from US-EAST-1




    4.4 Get the logs of the Lambda function

         4.4.0 Overview

         4.4.1 How to get log data with AWS CLI
                4.4.1.0 The --log-type option
                4.4.1.1 Get logResult encoded: "aws lambda invoke --function-name FUNC_NAME --log-type Tail"
                4.4.1.2 Get logResult decoded: "aws lambda invoke --function-name FUNC_NAME --log-type Tail --query LogResult"

         4.4.2 Retrieve the logs of the ProcessKinesisRecords function
                4.4.2.1 Get the LogResult in base64
                4.4.2.2 Get the LogResult and decode it

         4.4.3 Script to download last five log events
	 


    4.5 Get logs with 'aws logs'

         4.5.0 Commands 'aws logs' to run

         4.5.1 Run "aws logs describe-log-streams --log-group-name LOG_GROUP_NAME"

         4.5.2 Run "aws logs get-log-events  --log-group-name LOG_GROUP_NAME --log-stream-name LOG_STREAM_NAME"




    4.6 Deleting logs

         4.6.1 Deleting a log group

         4.6.2 Configure a retention period after which logs are deleted automatically





5. Create Kinesis stream and associate it with the Lambda function

    5.0 How to create Kinesis stream and make it the event source for the lambda function [DOC]

    5.1 Create Kinesis stream with 'aws kinesis create-stream' command

    5.2 Add Kinesis stream as event source to Lambda function w/ 'aws lambda create-event-source-mapping'
         5.2.0 What we have
         5.2.1 Run 'aws lambda add-event-source' to add Kinesis stream as event source to
	       function 'ProcessKinesisRecords'
         5.2.2 Check the event source mappings for lambda function 'ProcessKinesisRecords'

    5.3 Send test event to Kinesis 
         5.3.0 Overview
         5.3.1 Create event with 'aws kinesis put-record' and test event source mapping sends it to Lambda function

    5.4 Test the Lambda function receives the event by inspecting the CloudWatch logs
          5.4.0 Overview
          5.4.1 Inspect CloudWatch log-group and log-stream-names in the console
          5.4.2 Inspect CloudWatch log-group and log-stream-names with the 'aws logs' CLI


---





Part II: Logging to s3
======================


6. Export CloudWatch logs to S3


    6.1 Create S3 bucket 'lambda-for-kinesis-ds-gabriel'
          6.1.1 Run the "aws s3 create-bucket" CLI
          6.1.2 Check the S3 bucket ARN


    6.2 Create S3 bucket policy and attach it to bucket 'lambda-for-kinesis-ds-gabriel'
          6.2.0 Command 'aws s3api put-bucket-policy'
          6.2.1 Create S3 bucket policy "s3-bucket-policy.json"
          6.2.2 Attach the policy to the bucket lambda-for-kinesis-ds-gabriel


    6.3 Attach policies to role lambda-kinesis-role-created-from-console
          6.3.0 Inital status of role lambda-kinesis-role-created-from-console
          6.3.1 Attach policies AmazonS3FullAccess, CloudWatchLogsFullAccess and CloudWatchEventsFullAccess
          6.3.2 Check policies attached to role lambda-kinesis-role-created-from-console

---







Part I: Create Lambda Function that is connected to a Kinesis Data Source
==========================================================================



1. Prerequisites
----------------


The AWS client is installed on the machine, and the AWS configuration and credentials are set up under

   ~/.aws


---



2. AWS Version
---------------

   gabriel $ aws --version
   aws-cli/2.0.62 Python/3.9.0 Darwin/19.6.0 source/x86_64

---




3. Create the execution role and add policies
---------------------------------------------



3.1 Overiew
------------


Here I create an AWS Lambdae execution role, then I attach to it the required permissions for AWS Kinesis and CloudWatch,


To create an execution role


1. Open the roles page in the IAM console.

     https://console.aws.amazon.com/iam/home#/roles


2. Choose Create role.

    Create a role with the following properties.

    Trusted entity – AWS Lambda.

    Permissions    – AWSLambdaKinesisExecutionRole.

                      The AWSLambdaKinesisExecutionRole policy has
                      the permissions that the function needs to read
                      items from Kinesis and write logs to CloudWatch Logs.

    Role name      – lambda-kinesis-role-created-from-console.

---




3.2 Create the lambda-kinesis-role-from-console role from the IAM console
--------------------------------------------------------------------------


To create an execution role


1. Open the roles page in the IAM console.

    https://console.aws.amazon.com/iam/home#/roles
    https://console.aws.amazon.com/iamv2/home#/roles



2. Choose Create role

    https://console.aws.amazon.com/iam/home#/roles$new?step=type



3. Under

     Select type of trusted entity

   select

     "AWS Service"
   


4. Scroll to "Choose a use case", select

     "Lambda"

   then click on "Next: Permissions" which takes you to

    https://console.aws.amazon.com/iam/home#/roles$new?step=permissions&commonUseCase=Lambda%2BLambda&selectedUseCase=Lambda

   where you attach permission policies to the role as shown next.



5. Attach these policies to the role

     AWSLambdaBasicExecutionRole

     AWSLambdaKinesisExecutionRole - The AWSLambdaKinesisExecutionRole policy has
                                     the permissions that the function needs to read
                                     items from Kinesis and write logs to CloudWatch Logs.
     AWSXRayDaemonWriteAccess

   then select "Next: Tags" and then "Next: Review", which takes to the
   Review page of the Create Role workflow



6. On the Review page of Create Role:

    https://console.aws.amazon.com/iam/home#/roles$new?\
    step=review&commonUseCase=Lambda%2BLambda&selectedUseCase=Lambda&\
    policies=arn:aws:iam::aws:policy%2Fservice-role%2FAWSLambdaKinesisExecutionRole&\
    policies=arn:aws:iam::aws:policy%2Fservice-role%2FAWSLambdaBasicExecutionRole&\
    policies=arn:aws:iam::aws:policy%2FAWSXRayDaemonWriteAccess


   enter:

     Role name:  lambda-kinesis-role-created-from-console

   then check the line
  
     AWS service: lambda.amazonaws.com

   and the policies

    AWSLambdaBasicExecutionRole
    AWSLambdaKinesisExecutionRole 
    AWSXRayDaemonWriteAccess
    
   and click om "Create Role"



7. This takes you to the IAM roles page

    https://console.aws.amazon.com/iamv2/home#/roles

   where you scroll to the newly created role

    lambda-kinesis-role-created-from-console

  and click on it to view it

    https://console.aws.amazon.com/iam/home#/roles/lambda-kinesis-role-created-from-console

---





4. Create the lambda function, invoke it and get logs
-----------------------------------------------------


See

   https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html




4.1 Create the function code and deployment package
---------------------------------------------------


See

  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html


4.1.1 Function source code
---------------------------

The following example code receives a Kinesis event input and processes the messages
that it contains. For illustration, the code writes some of the incoming event data
to CloudWatch Logs.


  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ cat index.js
  
  console.log('Loading function');

  exports.handler = function(event, context) {
    //console.log(JSON.stringify(event, null, 2));
    event.Records.forEach
    (
       function(record) {
          // Kinesis data is base64 encoded so decode here
          var payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii');
          console.log('Decoded payload:', payload);
       }
   );
  };


---



4.1.2 Create a deployment package
---------------------------------

Do this

  zip function_js.zip index.js


Details

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ more zip_js.sh 
  zip function_js.zip index.js

  gabriel $ ./zip_js.sh 
  adding: index.js (deflated 41%)
  

---




4.2 Create lambda function resource
-----------------------------------


See

  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html




4.2.1 Check config with the CLI
-------------------------------


  gabriel $ aws configure
  AWS Access Key ID [****************SYRA]: 
  AWS Secret Access Key [****************ikEd]: 
  Default region name [us-east-2]: us-east-1
  Default output format [json]: 



---




4.2.2 Check role "lambda-kinesis-role-created-from-console"
-----------------------------------------------------------



Check the role "lambda-kinesis-role-created-from-console" created in section

3.1.2.1 Create execution role 'lambda-role-created-from-console' in the IAM console


---



4.2.2.1 Check with the UI
-------------------------


  https://console.aws.amazon.com/iam/home#/roles/lambda-kinesis-role-created-from-console


---




4.2.2.2 Check with the CLI
--------------------------

See

  https://docs.aws.amazon.com/cli/latest/reference/iam/list-roles.html
  https://docs.aws.amazon.com/cli/latest/reference/iam/get-role.html




4.2.2.2.1 aws iam list-roles
----------------------------


  gabriel $ aws iam list-roles | head -11
  {
    "Roles": [
        {
            "Path": "/",
            "RoleName": "AmazonSSMRoleForAutomationAssumeQuickSetup",
            "RoleId": "AROASASKFEOOJF26V7ND6",
            "Arn": "arn:aws:iam::138668221340:role/AmazonSSMRoleForAutomationAssumeQuickSetup",
            "CreateDate": "2019-10-28T02:32:46+00:00",
            "AssumeRolePolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
    ...

  }

---


Full info

  gabriel $ aws iam list-roles | jq -M '.Roles[] | select(.RoleName=="lambda-kinesis-role-created-from-console")'
{
  "Path": "/",
  "RoleName": "lambda-kinesis-role-created-from-console",
  "RoleId": "AROASASKFEOODXUDWTUVP",
  "Arn": "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console",
  "CreateDate": "2021-09-22T21:07:48+00:00",
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  },
  "Description": "Allows Lambda functions to call AWS services on your behalf.",
  "MaxSessionDuration": 3600
}



Get ARN

  gabriel $ aws iam list-roles | jq -M '.Roles[] | select(.RoleName=="lambda-kinesis-role-created-from-console") | .Arn'
  "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console"


---



4.2.2.2.2 aws iam get-role --role-name ROLE_NAME
------------------------------------------------


Full info

  gabriel $ aws iam get-role --role-name lambda-kinesis-role-created-from-console
  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-kinesis-role-created-from-console",
        "RoleId": "AROASASKFEOODXUDWTUVP",
        "Arn": "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console",
        "CreateDate": "2021-09-22T21:07:48+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Description": "Allows Lambda functions to call AWS services on your behalf.",
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {}
    }
  }



Get ARN

  gabriel $ aws iam get-role --role-name lambda-kinesis-role-created-from-console | jq '.Role.Arn'
  "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console"


---





4.2.3 Create function resource with the CLI
-------------------------------------------



Steps:


0. Go to the dir containing function_js.zip

    gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

    gabriel $ ls -1
    function_js.zip
    index.js
    zip_js.sh



1. Get the ARN of the role

    gabriel $ aws iam list-roles | jq -M '.Roles[] | select(.RoleName=="lambda-kinesis-role-created-from-console") | .Arn'
    "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console"

    gabriel $ aws iam get-role --role-name lambda-kinesis-role-created-from-console | jq '.Role.Arn'
    "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console"




2. Run "aws lamba create-function", specifying the function name of the new function, the zip-file,
   handler, runtime and role

    gabriel $ aws lambda create-function    \
      --function-name ProcessKinesisRecords \
      --zip-file fileb://function_js.zip    \
      --handler index.handler \
      --runtime nodejs12.x    \
      --role "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console"
    {
      "FunctionName": "ProcessKinesisRecords",
      "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords",
      "Runtime": "nodejs12.x",
      "Role": "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console",
      "Handler": "index.handler",
      "CodeSize": 409,
      "Description": "",
      "Timeout": 3,
      "MemorySize": 128,
      "LastModified": "2021-09-24T13:42:33.664+0000",
      "CodeSha256": "G9zBS5ujuRmR7Q2rslBgwnd9gIOoy5MJcPbyBM0rRIA=",
      "Version": "$LATEST",
      "TracingConfig": {
         "Mode": "PassThrough"
      },
      "RevisionId": "e8b217f1-7338-4f08-866c-c9a0f32f4da6",
      "State": "Active",
      "LastUpdateStatus": "Successful"
    }



Next we inspect the lambda function we created.


---




4.2.4 Show the lambda function
------------------------------



4.2.4.1 In the UI
-----------------

See

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
  https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions



Steps:


1. Point browser to

    https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions


2. Click on

     ProcessKinesisRecords

  which takes you to

    https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=code

---



4.2.4.2 In the CLI
------------------

See

  gabriel $ aws lambda help


Steps:


1. Before creating the function in section 4.2.3

    gabriel $ aws lambda list-functions
    {
      "Functions": []
    }

    gabriel $ aws lambda list-functions --master-region=us-east-1 --function-version ALL
    {
      "Functions": []
    }



2. After creating the function in section 4.2.3

    gabriel $ aws lambda list-functions
    {
      "Functions": [
        {
            "FunctionName": "ProcessKinesisRecords",
            "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords",
            "Runtime": "nodejs12.x",
            "Role": "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console",
            "Handler": "index.handler",
            "CodeSize": 409,
            "Description": "",
            "Timeout": 3,
            "MemorySize": 128,
            "LastModified": "2021-09-24T13:42:33.664+0000",
            "CodeSha256": "G9zBS5ujuRmR7Q2rslBgwnd9gIOoy5MJcPbyBM0rRIA=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "e8b217f1-7338-4f08-866c-c9a0f32f4da6"
        }
      ]
    }

---






4.3 Test the lambda function
----------------------------

See

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/discover
  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=code

  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html

---


To test the Lambda function, invoke it manually using the invoke AWS Lambda CLI
command and a sample Kinesis event.


---


4.3.1 Raw binary vs base64 input files
--------------------------------------

See

  https://docs.aws.amazon.com/sdkref/latest/guide/setting-global-cli_binary_format.html
  

To test the Lambda Function, we will pass to the 'aws lambda' CLI the URL of a input file.

The AWS CLI can handle base64 and raw input files, and it determines how to handle them based on

  o the file prefix, which can be file:// or fileb://

  o the cli-binary-format option to the aws cli 

  o the AWS CLI version



The option cli-binary-format is relevant for file:// prefix spec of input files
that are raw binary when using AWS CLI version 2.

If you are using AWS CLI version 2, and the file:// notation, then the cli-binary-format option
to the aws cli is required to pass raw input data (because the 'base64' default is incorrect
in this case).

Check the AWS CLI version

     gabriel $ aws --version
     aws-cli/2.0.62 Python/3.9.0 Darwin/19.6.0 source/x86_64

---




4.3.2 Create the input file
---------------------------

Use the lambda UI to go to the function, click on Test tab, select "Configure test event",
then in the "Event template" box enter

  Kinesis-get-records

and you see this JSON

  {
    "Records": [
      {
        "kinesis": {
          "partitionKey": "partitionKey-03",
          "kinesisSchemaVersion": "1.0",
          "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
          "sequenceNumber": "49545115243490985018280067714973144582180062593244200961",
          "approximateArrivalTimestamp": 1428537600
        },
        "eventSource": "aws:kinesis",
        "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",
        "invokeIdentityArn": "arn:aws:iam::EXAMPLE",
        "eventVersion": "1.0",
        "eventName": "aws:kinesis:record",
        "eventSourceARN": "arn:aws:kinesis:EXAMPLE",
        "awsRegion": "us-east-1"
      }
    ]
  }


---



Save it as input_us-east-1.json then run


---


4.3.3 Invoke lambda func with a sample event from US-EAST-1
-----------------------------------------------------------


   gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

   gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisRecords \
                      --payload file://input_us-east-1.json \
                      output_us-east-2.txt
   {
      "StatusCode": 200,
      "ExecutedVersion": "$LATEST"
   }



   gabriel $ more output_us-east-1.txt
   null

---






4.4 Get the logs of the Lambda function
---------------------------------------


See

  https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html
  https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html

  https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html
  https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html#monitoring-cloudwatchlogs-cli




4.4.0 Overview
--------------


Two ways to get logging info:


o from the console

  * Lambda function console 

     https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=code
     https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=monitoring


  * CloudWatch

     https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html

     https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups
  
     https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups\
     /log-group/$252Faws$252Flambda$252FProcessKinesisRecords
  
     https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/\
     log-group/$252Faws$252Flambda$252FProcessKinesisRecords/log-events/\
     2021$252F09$252F25$252F$255B$2524LATEST$255D9ec4743fbdf94119a7d5dfe341d9f934

     https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/\
     log-group/$252Faws$252Flambda$252FProcessKinesisRecords/log-events/\
     2021$252F09$252F25$252F$255B$2524LATEST$255Dead95136114b4f1f87220811c464bebe$3Fstart$3DPT3H



o from CLI

    https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html




Example of using the Lambda function console
---------------------------------------------

See

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=code
    
  https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html
  https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html#monitoring-cloudwatchlogs-cli



o Go to

    https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisRecords?tab=code


o Select

    Test -> Kinesis-get-records then press TEST to run the function with the Kinesis-get-records input



o Click on Excution Result tab, where you see

   Test Event Name: Kinesis-get-records

   Response: null

   Function Logs
     START RequestId: 9eb22d6d-6f4c-4d21-af99-c683d39c4a0f Version: $LATEST
       2021-09-25T11:19:26.414Z	undefined	INFO	Loading function
       2021-09-25T11:19:26.419Z	9eb22d6d-6f4c-4d21-af99-c683d39c4a0f	INFO	Decoded payload: Hello, this is a test 123.
     END RequestId: 9eb22d6d-6f4c-4d21-af99-c683d39c4a0f
     REPORT RequestId: 9eb22d6d-6f4c-4d21-af99-c683d39c4a0f \
            Duration: 6.94 ms \
	    Billed Duration: 7 ms	Memory Size: 128 MB	Max Memory Used: 64 MB	Init Duration: 147.15 ms

   Request ID: 9eb22d6d-6f4c-4d21-af99-c683d39c4a0f


---





4.4.1 How to get log data with AWS CLI
--------------------------------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html

  https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html



You can use the AWS CLI to retrieve logs for an invocation using the

   --log-type

command option. The response contains a LogResult field that contains up to 4 KB
of base64-encoded logs from the invocation.


---




4.4.1.0 The --log-type option
-----------------------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html

  Google: aws lambda invoke logtype



LogType

   Set to Tail to include the execution log in the response.

   Applies to synchronously invoked functions only.

   Valid Values: None | Tail


---




4.4.1.1 Get logResult encoded: "aws lambda invoke --function-name FUNC_NAME --log-type Tail"
--------------------------------------------------------------------------------------------

The following example shows how to retrieve a log ID from the LogResult field for a function
named my-function.

  aws lambda invoke --function-name my-function out --log-type Tail

You should see the following output:

  {
    "StatusCode": 200,
    "LogResult": "U1RBUlQgUmVxdWVzdElkOiA4N2QwNDRiOC1mMTU0LTExZTgtOGNkYS0yOTc0YzVlNGZiMjEgVmVyc2lvb...",
    "ExecutedVersion": "$LATEST"
  }

---




4.4.1.2 Get logResult decoded: "aws lambda invoke --function-name FUNC_NAME --log-type Tail --query LogResult"
--------------------------------------------------------------------------------------------------------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html


In the same command pipe, use the --query option to 'aws lambda invoke' and pipe
the output of 'aws lambda invoke' to the abase64 utility to decode the logs:

  aws lambda invoke \
          --function-name my-function     \
	  --log-type Tail                 \
          --query 'LogResult'             \
          --output text ourput.txt | base64 -d


You should see the following output:

  START RequestId: 57f231fb-1730-4395-85cb-4f71bd2b87b8 Version: $LATEST
  "AWS_SESSION_TOKEN": "AgoJb3JpZ2luX2VjELj...", \
  "_X_AMZN_TRACE_ID": "Root=1-5d02e5ca-f5792818b6fe8368e5b51d50;Parent=191db58857df8395;Sampled=0"",ask/lib:/opt/lib",
  END RequestId: 57f231fb-1730-4395-85cb-4f71bd2b87b8
  REPORT RequestId: 57f231fb-1730-4395-85cb-4f71bd2b87b8  \
         Duration: 79.67 ms  \
	 Billed Duration: 80 ms   \
	 Memory Size: 128 MB   \
	 Max Memory Used: 73 MB

---






4.4.2 Retrieve the logs of the ProcessKinesisRecords function
-------------------------------------------------------------


See

  https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html
  
  https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html




Using the how-to from the previous section,invoke the lammbda function
ProcessKinesisRecords function, specifying the --log-type Tail option.

   gabriel $ aws lambda invoke \
                      --function-name ProcessKinesisRecords ... \
                      --log-type Tail		                \
                      ...

---




4.4.2.1 Get the LogResult in base64
-----------------------------------

   gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

   gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisRecords \
                      --payload file://input_us-east-1.json \
                      --log-type Tail		            \
	              output_us-east-1a.txt
  {
    "StatusCode": 200,
    "LogResult": "U1RBUlQgUmVxdWVzdElkOiAzZjMzZTEzZS1iZDE3LTRjOGQtOGM4Yy1kYmMzZGNjOTMzNjIgVmVyc2lvbjogJExBVEVTVAoyMDIxLTA5LTI1VDEzOjAwOjA0LjM4MFoJdW5kZWZpbmVkCUlORk8JTG9hZGluZyBmdW5jdGlvbgoyMDIxLTA5LTI1VDEzOjAwOjA0LjM4NVoJM2YzM2UxM2UtYmQxNy00YzhkLThjOGMtZGJjM2RjYzkzMzYyCUlORk8JRGVjb2RlZCBwYXlsb2FkOiBIZWxsbywgdGhpcyBpcyBhIHRlc3QgMTIzLgpFTkQgUmVxdWVzdElkOiAzZjMzZTEzZS1iZDE3LTRjOGQtOGM4Yy1kYmMzZGNjOTMzNjIKUkVQT1JUIFJlcXVlc3RJZDogM2YzM2UxM2UtYmQxNy00YzhkLThjOGMtZGJjM2RjYzkzMzYyCUR1cmF0aW9uOiAxNS42OSBtcwlCaWxsZWQgRHVyYXRpb246IDE2IG1zCU1lbW9yeSBTaXplOiAxMjggTUIJTWF4IE1lbW9yeSBVc2VkOiA2NCBNQglJbml0IER1cmF0aW9uOiAxOTMuNzIgbXMJCg==",
    "ExecutedVersion": "$LATEST"
  }


  gabriel $ more output_us-east-1a.txt 
  null


---



4.4.2.2 Get the LogResult and decode it
---------------------------------------

Run

   gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

   gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisRecords \
                      --payload file://input_us-east-1.json \
                      --log-type Tail		            \
                      --query 'LogResult'                   \
		      --output text                         \
	              output_us-east-1b.txt | base64 -d

  START RequestId: a88934bd-45b8-447e-9619-547d64b59ee7 Version: $LATEST
    2021-09-25T13:05:14.842Z	a88934bd-45b8-447e-9619-547d64b59ee7	INFO	Decoded payload: Hello, this is a test 123.
  END RequestId: a88934bd-45b8-447e-9619-547d64b59ee7
  REPORT RequestId: a88934bd-45b8-447e-9619-547d64b59ee7 \
         Duration: 84.25 ms     \
	 Billed Duration: 85 ms \
	 Memory Size: 128 MB    \
	 Max Memory Used: 64 MB



  gabriel $ more output_us-east-1b.txt
  null

---



TIP
---

Can also get the log by replacing

     --query 'LogResult' --output text 

with

     | jq -M '.LogResult'

i.e.,

   gabriel $ aws lambda invoke \
                        --cli-binary-format raw-in-base64-out \
                        --function-name ProcessKinesisRecords \
                        --payload file://input_us-east-1.json \
                        --log-type Tail		              \
	                output_us-east-1a.txt                 \
			| jq -M '.LogResult' | sed 's/\"//g' | base64 -d

---




4.4.3 Script to download last five log events
---------------------------------------------



Use a script similar to the one shown below to download the last five log events.

Create the following script get-logs.sh in your Lambda project directory 


  $ cat get-logs.sh 
  #!/bin/bash
  aws lambda invoke --function-name my-function --cli-binary-format raw-in-base64-out --payload '{"key": "value"}' out
  sed -i'' -e 's/"//g' out
  sleep 15
  aws logs get-log-events --log-group-name /aws/lambda/my-function --log-stream-name $(cat out) --limit 5


where

  The cli-binary-format option is required if you are using AWS CLI version 2.
  You can also configure this option in your AWS CLI config file.


  The script

   uses sed to remove quotes from the output file, and
   sleeps for 15 seconds to allow time for the logs to become available.


  The output includes the response from Lambda and the output
  from the get-log-events command.

---




4.5 Get logs with 'aws logs'
----------------------------



4.5.0 Commands 'aws logs' to run
--------------------------------

See

  Show the Log groups in CloudWatch
  https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

  aws log describe-log-streams
  https://docs.aws.amazon.com/cli/latest/reference/logs/describe-log-streams.html

  Log streams
  https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups
  /log-group/$252Faws$252Flambda$252FProcessKinesisRecords
  
---



Will take these steps:


o Figure out the log group name, see

     https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

  Tje log-group-name is

     /aws/lambda/LAMBDA_FUNCTION_NAME

  e.g.,

     /aws/lambda/ProcessKinesisRecords



o Get the log-stream names

    aws logs describe-log-streams --log-group-name LOG_GROUP_NAME



o Get the log events specifying the log-group-name and log-stream-name:

     aws logs get-log-events --log-group-name LOG_GROUP_NAME --log-stream-name LOG_STREAM_NAME --limit 5

  e.g.,
  
      aws logs get-log-events \
             --log-group-name /aws/lambda/ProcessKinesisRecords                       \
	     --log-stream-name "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c" \
             --limit 5

---





4.5.1 Run "aws logs describe-log-streams --log-group-name LOG_GROUP_NAME"
-------------------------------------------------------------------------


Command template

  aws logs describe-log-streams \
                --log-group-name /aws/lambda/FUNCTION_NAME \
	        --order-by {LastEventTime|LogStreamName}
		--descending

---



Do this:


o Function name is ProcessKinesisRecords, so

    log-group-name = /aws/lambda/ProcessKinesisRecords



o Run "aws logs describe-log-streams"

   gabriel $ aws logs describe-log-streams \
                --log-group-name /aws/lambda/ProcessKinesisRecords \
		--order-by LastEventTime \
		--descending
   {
     "logStreams": [
        {
            "logStreamName": "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c",
            "creationTime": 1632574807452,
            "firstEventTimestamp": 1632574804380,
            "lastEventTimestamp": 1632575408012,
            "lastIngestionTime": 1632575417032,
            "uploadSequenceToken": "49617975193235303962033332091512661722429324366603879010",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c",
            "storedBytes": 0
        },
        {
            "logStreamName": "2021/09/25/[$LATEST]d68065e763e04ed6be8d1b17fc821334",
            "creationTime": 1632569582579,
            "firstEventTimestamp": 1632569579229,
            "lastEventTimestamp": 1632569738112,
            "lastIngestionTime": 1632569747077,
            "uploadSequenceToken": "49617975193235303962033330913642937487879968890021741154",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]d68065e763e04ed6be8d1b17fc821334",
            "storedBytes": 0
        },
        {
            "logStreamName": "2021/09/25/[$LATEST]9ec4743fbdf94119a7d5dfe341d9f934",
            "creationTime": 1632568773900,
            "firstEventTimestamp": 1632568766414,
            "lastEventTimestamp": 1632569054646,
            "lastIngestionTime": 1632569063585,
            "uploadSequenceToken": "49618960112738634040139610627174780693661275290026902722",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]9ec4743fbdf94119a7d5dfe341d9f934",
            "storedBytes": 0
        },
        {
            "logStreamName": "2021/09/25/[$LATEST]ead95136114b4f1f87220811c464bebe",
            "creationTime": 1632567699015,
            "firstEventTimestamp": 1632567693558,
            "lastEventTimestamp": 1632567961547,
            "lastIngestionTime": 1632567970543,
            "uploadSequenceToken": "49618484817179225208959731156468857680792250984444200162",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]ead95136114b4f1f87220811c464bebe",
            "storedBytes": 0
        },
        {
            "logStreamName": "2021/09/25/[$LATEST]0fb510c943a249988144f90ce0db7131",
            "creationTime": 1632565798978,
            "firstEventTimestamp": 1632565792872,
            "lastEventTimestamp": 1632566095619,
            "lastIngestionTime": 1632566104582,
            "uploadSequenceToken": "49601945521753380972469494256052114453457023232794165330",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]0fb510c943a249988144f90ce0db7131",
            "storedBytes": 0
        },
        {
            "logStreamName": "2021/09/25/[$LATEST]a04f8631ae2a4685acf4ccd35c666a3e",
            "creationTime": 1632564497889,
            "firstEventTimestamp": 1632564493596,
            "lastEventTimestamp": 1632564493609,
            "lastIngestionTime": 1632564497905,
            "uploadSequenceToken": "49605428418999580120185292941074999111513883655790396274",
            "arn": "arn:aws:logs:us-east-1:138668221340:log-group:/aws/lambda/ProcessKinesisRecords:\
	            log-stream:2021/09/25/[$LATEST]a04f8631ae2a4685acf4ccd35c666a3e",
            "storedBytes": 0
        }
     ]
   }



o Run "aws logs describe-log-streams", extracting the field "logstreamName":

   gabriel $ aws logs describe-log-streams    \
                     --log-group-name /aws/lambda/ProcessKinesisRecords    \
		     --order-by LastEventTime  \
		     --descending | jq '.logStreams[] | {"logstreamName": .logStreamName}' 
  {
    "logstreamName": "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]d68065e763e04ed6be8d1b17fc821334"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]9ec4743fbdf94119a7d5dfe341d9f934"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]ead95136114b4f1f87220811c464bebe"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]0fb510c943a249988144f90ce0db7131"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]a04f8631ae2a4685acf4ccd35c666a3e"
  }




o Filter to see only the log-stream-name values


   gabriel $ aws logs describe-log-streams    \
                     --log-group-name /aws/lambda/ProcessKinesisRecords    \
		     --order-by LastEventTime  \
		     --descending | jq '.logStreams[] | .logStreamName'

  "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c"
  "2021/09/25/[$LATEST]d68065e763e04ed6be8d1b17fc821334"
  "2021/09/25/[$LATEST]9ec4743fbdf94119a7d5dfe341d9f934"
  "2021/09/25/[$LATEST]ead95136114b4f1f87220811c464bebe"
  "2021/09/25/[$LATEST]0fb510c943a249988144f90ce0db7131"
  "2021/09/25/[$LATEST]a04f8631ae2a4685acf4ccd35c666a3e"



o filter to see the most recent log-stream-name:


   gabriel $ aws logs describe-log-streams    \
                     --log-group-name /aws/lambda/ProcessKinesisRecords    \
		     --order-by LastEventTime  \
		     --descending              \
                     | jq '.logStreams[] | .logStreamName'  | head -1

  "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c"


---





4.5.2 Run "aws logs get-log-events  --log-group-name LOG_GROUP_NAME --log-stream-name LOG_STREAM_NAME"
------------------------------------------------------------------------------------------------------


Command template

  aws logs get-log-events \
           --log-group-name LOG_GROUP_NAME \
	   --log-stream-name LOG_STREAM_NAME --limit 5



Sreps:

1. We found so far

      log-group-name = /aws/lambda/ProcessKinesisRecords  

      log-stream-name = '2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c'



2. Run 'aws log get-log-events', specifying the log-group-name and log-stream-name:
  

   gabriel $ aws logs get-log-events \
                --log-group-name /aws/lambda/ProcessKinesisRecords                       \
                --log-stream-name '2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c' \
                --limit 5
   {
    "events": [
        {
            "timestamp": 1632575355443,
            "message": "REPORT \
	                RequestId: 75e7f443-ea12-4150-9925-3ba628b59bd0\t\
	                Duration: 110.54 ms\t\
			Billed Duration: 111 ms\t\
			Memory Size: 128 MB\t\
			Max Memory Used: 65 MB\t\n",
            "ingestionTime": 1632575364348
        },
        {
            "timestamp": 1632575408007,
            "message": "START RequestId: e39da0bb-8c95-4737-88da-831724225dba Version: $LATEST\n",
            "ingestionTime": 1632575417032
        },
        {
            "timestamp": 1632575408010,
            "message": "2021-09-25T13:10:08.010Z\te39da0bb-8c95-4737-88da-831724225dba\t\
			INFO\tDecoded payload: Hello, this is a test 123.\n",
            "ingestionTime": 1632575417032
        },
        {
            "timestamp": 1632575408012,
            "message": "END RequestId: e39da0bb-8c95-4737-88da-831724225dba\n",
            "ingestionTime": 1632575417032
        },
        {
            "timestamp": 1632575408012,
            "message": "REPORT RequestId: e39da0bb-8c95-4737-88da-831724225dba\t\
	                       Duration: 1.49 ms\t\
	                       Billed Duration: 2 ms\t\
			       Memory Size: 128 MB\t\
			       Max Memory Used: 65 MB\t\n",
            "ingestionTime": 1632575417032
        }
    ],
    "nextForwardToken": "f/36407648191462782020142947057358572592095420463172354051/s",
    "nextBackwardToken": "b/36407647019134907678586619066276816515855293559731781635/s"
   }


---





4.6 Deleting logs
-----------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/nodejs-logging.html

  https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention


Log groups aren't deleted automatically when you delete a function.

To avoid storing logs indefinitely,

  o delete the log group, or

  o configure a retention period after which logs are deleted automatically


---


4.6.1 Deleting a log group
--------------------------

  gabriel $ aws logs delete-log-group help


  NAME
       delete-log-group -


  DESCRIPTION

       Deletes  the  specified  log  group  and  permanently  deletes  all the
       archived log events associated with the log group.

       See also: AWS API Documentation

       See 'aws help' for descriptions of global parameters.


  SYNOPSIS
  
        delete-log-group
          --log-group-name <value>
          [--cli-input-json | --cli-input-yaml]
          [--generate-cli-skeleton <value>]
          [--cli-auto-prompt <value>]


  OPTIONS

       --log-group-name (string)
          The name of the log group.

       --cli-input-json | --cli-input-yaml (string)
          Reads arguments from the JSON string provided.
	  The JSON string follows the format provided by
            --generate-cli-skeleton.
	  If other arguments are provided on the command line, 
          those values will override the JSON-provided values. It is not
          possible to pass arbitrary binary values using a JSON-provided value as
          the string will be taken literally. This may not be specified along
          with --cli-input-yaml.


       --generate-cli-skeleton (string) Prints a  JSON  skeleton  to  standard
       output without sending an API request. If provided with no value or the
       value input, prints a sample input JSON that can be used as an argument
       for --cli-input-json. Similarly, if provided yaml-input it will print a
       sample input YAML that can be used with --cli-input-yaml.  If  provided
       with  the  value  output, it validates the command inputs and returns a
       sample output JSON for that command.

       --cli-auto-prompt (boolean) Automatically prompt for CLI input  parame-
       ters.

       See 'aws help' for descriptions of global parameters.


  EXAMPLES

       The following command deletes a log group named my-logs:

          aws logs delete-log-group --log-group-name my-logs

---




4.6.2 Configure a retention period after which logs are deleted automatically
-----------------------------------------------------------------------------

See

  https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention



---





5. Create Kinesis stream and associate it with the Lambda function
------------------------------------------------------------------


See

  Section "Create a Kinesis stream" under
  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html




5.0 How to create Kinesis stream and make it the event source for the lambda function [DOC]
--------------------------------------------------------------------------------------------


Steps:


1. Use the create-stream command to create a stream:

     aws kinesis create-stream --stream-name lambda-stream --shard-count 1



2. Then get the stream ARN using the describe-stream command:

     aws kinesis describe-stream --stream-name lambda-stream

   You should get the following output:

   {
     "StreamDescription": {
        "Shards": [
            {
                "ShardId": "shardId-000000000000",
                "HashKeyRange": {
                    "StartingHashKey": "0",
                    "EndingHashKey": "340282366920746074317682119384634633455"
                },
                "SequenceNumberRange": {
                    "StartingSequenceNumber": "49591073947768692513481539594623130411957558361251844610"
                }
            }
        ],
        "StreamARN": "arn:aws:kinesis:us-west-2:123456789012:stream/lambda-stream",
        "StreamName": "lambda-stream",
        "StreamStatus": "ACTIVE",
        "RetentionPeriodHours": 24,
        "EnhancedMonitoring": [
            {
                "ShardLevelMetrics": []
            }
        ],
        "EncryptionType": "NONE",
        "KeyId": null,
        "StreamCreationTimestamp": 1544828156.0
     }
    
   }
---


3. Define the Kinesis stream as event source for the lambda function

   aws lambda create-event-source-mapping \
      --function-name ProcessKinesisRecords \
      --event-source  arn:aws:kinesis:us-west-2:123456789012:stream/lambda-stream \
      --batch-size 100 \
      --starting-position LATEST

---




5.1 Create Kinesis stream with 'aws kinesis create-stream' command
------------------------------------------------------------------


1. Use the create-stream command to create the stream 'kinesis-stream-for-lambda':

    gabriel $ aws kinesis create-stream --stream-name kinesis-stream-for-lambda --shard-count 1



2. Then get the stream ARN using the describe-stream command:

    gabriel $ aws kinesis describe-stream --stream-name kinesis-stream-for-lambda| jq -M '.StreamDescription.StreamARN'
    "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda"


We use the stream ARN in the next step to associate the Kinesis data stream
with your Lambda function.


---



5.2 Add Kinesis stream as event source to Lambda function w/ 'aws lambda create-event-source-mapping'
-----------------------------------------------------------------------------------------------------


5.2.0 What we have
------------------

So far we have


o A Kinesis event stream created in the previous section, whose name and ARN are

   gabriel $ aws kinesis list-streams
   {
      "StreamNames": [
          "kinesis-stream-for-lambda"
      ]
   }

   gabriel $ aws kinesis describe-stream --stream-name kinesis-stream-for-lambda| jq -M '.StreamDescription.StreamARN'
   "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda"



o The lambda function name and ARN

   gabriel $ aws lambda list-functions \
     | jq -M '.Functions[] | {"FunctionName": .FunctionName, "FunctionArn": .FunctionArn}'
   {
     "FunctionName": "ProcessKinesisRecords",
     "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords"
   }

---




5.2.1 Run 'aws lambda add-event-source' to add Kinesis stream as event source to function 'ProcessKinesisRecords'
-----------------------------------------------------------------------------------------------------------------


Now we run 'aws lambda add-event-source' to add the Kinesis stream as an event source to the lambda
function 'ProcessKinesisRecords':


  gabriel $ aws lambda create-event-source-mapping  \
        --function-name ProcessKinesisRecords       \
        --event-source "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda" \
        --batch-size 100 \
        --starting-position LATEST
 {
    "UUID": "00a3d08e-fa6a-4e0c-8e86-4aafeac0ceef",
    "BatchSize": 100,
    "MaximumBatchingWindowInSeconds": 0,
    "ParallelizationFactor": 1,
    "EventSourceArn": "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda",
    "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords",
    "LastModified": "2021-09-27T17:26:32.244000+02:00",
    "LastProcessingResult": "No records processed",
    "State": "Creating",
    "StateTransitionReason": "User action",
    "DestinationConfig": {
        "OnFailure": {}
    },
    "MaximumRecordAgeInSeconds": -1,
    "BisectBatchOnFunctionError": false,
    "MaximumRetryAttempts": -1
  }


Note the mapping ID for later use.

  "UUID": "00a3d08e-fa6a-4e0c-8e86-4aafeac0ceef",

---



5.2.2 Check the event source mappings for lambda function 'ProcessKinesisRecords'
---------------------------------------------------------------------------------

Get a list of event source mappings by running the list-event-source-mappings command:

  gabriel $ aws lambda list-event-source-mappings  \
           --function-name ProcessKinesisRecords   \
           --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda
  {
    "EventSourceMappings": [
        {
            "UUID": "00a3d08e-fa6a-4e0c-8e86-4aafeac0ceef",
            "BatchSize": 100,
            "MaximumBatchingWindowInSeconds": 0,
            "ParallelizationFactor": 1,
            "EventSourceArn": "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda",
            "FunctionArn":    "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords",
            "LastModified":   "2021-09-27T17:27:00+02:00",
            "LastProcessingResult": "No records processed",
            "State": "Enabled",
            "StateTransitionReason": "User action",
            "DestinationConfig": {
                "OnFailure": {}
            },
            "MaximumRecordAgeInSeconds": -1,
            "BisectBatchOnFunctionError": false,
            "MaximumRetryAttempts": -1
        }
    ]
  }


and verify that "State" is "Enabled":

  gabriel $ aws lambda list-event-source-mappings    \
              --function-name ProcessKinesisRecords  \
	      --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda \
	      | jq -M '.EventSourceMappings[] | {"State": .State}'
  {
    "State": "Enabled"
  }


Event source mappings can be disabled to pause polling temporarily without losing any records.

---





5.3 Test the Kinesis event stream is received by the Lambda function
--------------------------------------------------------------------


5.3.0 Overview
--------------

In section

  4.3.4 Invoke lambda func with a sample event frm US-EAST-1

we invoked the lambda function explicitly passing as payload the content of a sample Kinesis record,
in the file input_us-east-1.json

   gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

   gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisRecords \
                      --payload file://input_us-east-1.json  \
                      output_us-east-2.txt
   {
      "StatusCode": 200,
      "ExecutedVersion": "$LATEST"
   }


In this section, we add an event record to Kinesis stream "kinesis-stream-for-lambda", and test
that, using the event source mapping defined in the previous section, the event is sent to the
Lambda function.

---



5.3.1 Create event w/ 'aws kinesis put-record' and test event source mapping sends it to Lambda function
---------------------------------------------------------------------------------------------------------


We add an event record to the Kinesis stream "kinesis-stream-for-lambda", which, using
the event source mapping defined in the previous section, is sent to the Lambda function


  gabriel $ aws kinesis put-record \
              --stream-name kinesis-stream-for-lambda \
              --partition-key 1                       \
              --cli-binary-format raw-in-base64-out   \
              --data "Synthetic event 1 sent to kinesis-stream-for-lambda"
  {
      "ShardId": "shardId-000000000000",
      "SequenceNumber": "49622443395029499785670175668639705570302921445832916994"
  }


where the --data value is a string that the CLI encodes to base64 prior to sending it to Kinesis,
thanks to the option --cli-binary-format raw-in-base64-out.

You can run the same command more than once to add multiple records to the stream.


---



5.4 Test the Lambda function receives the event by inspecting the CloudWatch logs
---------------------------------------------------------------------------------


5.4.0 Overview
--------------

The data gets to Lambda function as follows:

1. Lambda uses the execution role to read records from the stream.

2. Then it invokes your Lambda function, passing in batches of records.

3. The function decodes data from each record and logs it,
   sending the output to CloudWatch Logs. View the logs
   in the CloudWatch console

     https://console.aws.amazon.com/cloudwatch

---



5.4.1 Inspect CloudWatch log-group and log-stream-names in the console
----------------------------------------------------------------------

Log groups

  https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/

Select log group

  /aws/lambda/ProcessKinesisRecords

which takes you to

  https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/\
  log-group/$252Faws$252Flambda$252FProcessKinesisRecords


Click on the top log-stream

  https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/\
  log-group/$252Faws$252Flambda$252FProcessKinesisRecords/\
  log-events/2021$252F09$252F27$252F$255B$2524LATEST$255D66d8bd4d764744b29a7409c7b0381dec

---




5.4.2 Inspect CloudWatch log-group and log-stream-names with the 'aws logs' CLI
-------------------------------------------------------------------------------


See

  4.5.1 Run "aws logs describe-log-streams --log-group-name LOG_GROUP_NAME"
  4.5.2 Run "aws logs get-log-events  --log-group-name LOG_GROUP_NAME --log-stream-name LOG_STREAM_NAME"



o Get log stream names

  gabriel $ aws logs describe-log-streams    \
                       --log-group-name /aws/lambda/ProcessKinesisRecords    \
                       --order-by LastEventTime  \
                       --descending | jq '.logStreams[] | {"logstreamName": .logStreamName}' | head -12
  {
    "logstreamName": "2021/09/27/[$LATEST]66d8bd4d764744b29a7409c7b0381dec"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]b1ef48f590ed4cf4bf2bd8c34f3afe5c"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]d68065e763e04ed6be8d1b17fc821334"
  }
  {
    "logstreamName": "2021/09/25/[$LATEST]9ec4743fbdf94119a7d5dfe341d9f934"
  }



o Get the events on the log-stream-name 

  gabriel $ aws logs get-log-events  \
                 --log-group-name /aws/lambda/ProcessKinesisRecords  \
                 --log-stream-name '2021/09/27/[$LATEST]66d8bd4d764744b29a7409c7b0381dec' \
		 --limit 5
  {
    "events": [
        {
            "timestamp": 1632758376455,
            "message": "START RequestId: 3770519b-4622-4154-827a-ac5cd01cfbd4 Version: $LATEST\n",
            "ingestionTime": 1632758383343
        },
        {
            "timestamp": 1632758376455,
            "message": "2021-09-27T15:59:36.455Z\tundefined\tINFO\tLoading function\n",
            "ingestionTime": 1632758383343
        },
        {
            "timestamp": 1632758376469,
            "message": "2021-09-27T15:59:36.460Z\t\
	    3770519b-4622-4154-827a-ac5cd01cfbd4\tINFO\tDecoded payload: Synthetic event 1 sent to kinesis-stream-for-lambda\n",
            "ingestionTime": 1632758383343
        },
        {
            "timestamp": 1632758376472,
            "message": "END RequestId: 3770519b-4622-4154-827a-ac5cd01cfbd4\n",
            "ingestionTime": 1632758383343
        },
        {
            "timestamp": 1632758376472,
            "message": "REPORT RequestId: 3770519b-4622-4154-827a-ac5cd01cfbd4\t\
	    Duration: 11.86 ms\tBilled Duration: 12 ms\tMemory Size: 128 MB\tMax Memory Used: 64 MB\tInit Duration: 150.44 ms\t\n",
            "ingestionTime": 1632758383343
        }
    ],
    "nextForwardToken": "f/36411728524468609562522215402463673426474203616781074436/s",
    "nextBackwardToken": "b/36411728524089496894147194809057566215839181471179407360/s"
  }

---







Part II: Logging to s3
======================



6. Export CloudWatch logs to S3
-------------------------------




6.1 Create S3 bucket 'lambda-for-kinesis-ds-gabriel'    
----------------------------------------------------

See

  https://www.chaossearch.io/blog/how-to-create-an-s3-bucket-with-aws-cli
  
  aws s3 mb s3://lambda-function-kinesis-data-source-gabriel --region=eu-east-1

  ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/02_AWS_serverless_app/01_Docs/aws_s3.txt


Check

  gabriel $ curl -ik https://s3.us-east-1.amazonaws.com 
  HTTP/1.1 307 Temporary Redirect
  x-amz-id-2: gyejvJ8T9qiUYIjvwBbBdKT2Vldwtpl2ZLqKBuGpdvgoz6XaAcWGr8+ZOVKx6jDBGQmAQ6VN9wE=
  x-amz-request-id: HFP4F2R99GXE338D
  Date: Sun, 26 Sep 2021 14:51:51 GMT
  Location: https://aws.amazon.com/s3/
  Server: AmazonS3
  Content-Length: 0

---




6.1.1 Run the "aws s3 create-bucket" CLI
----------------------------------------


See

  https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html
  
  https://www.chaossearch.io/blog/how-to-create-an-s3-bucket-with-aws-cli
  
  aws s3api create-bucket --bucket=lambda-for-kinesis-ds-gabriel --region=us-east-1
 

Synopsis

    aws s3api create-bucket     \
            --bucket=lambda-for-kinesis-ds-gabriel \
	    --region=us-east-1  \
	    --create-bucket-configuration LocationConstraint=us-west-1


---

Run

  gabriel $ aws s3api create-bucket       \
                     --bucket=lambda-for-kinesis-ds-gabriel    \
		     --region=us-east-1     
  {
      "Location": "/lambda-for-kinesis-ds-gabriel"
  }


---

Check

  gabriel $ aws s3 ls   s3://lambda-for-kinesis-ds-gabriel --region=us-east-1


---


Show ACL

  gabriel $ aws s3api get-bucket-acl --bucket lambda-for-kinesis-ds-gabriel
  {
    "Owner": {
        "DisplayName": "gabrielmateescu",
        "ID": "9c8c13c3e2fa376172b075f825c42f5ff4cb84d1b225a42822d7fc2f790024b6"
    },
    "Grants": [
        {
            "Grantee": {
                "DisplayName": "gabrielmateescu",
                "ID": "9c8c13c3e2fa376172b075f825c42f5ff4cb84d1b225a42822d7fc2f790024b6",
                "Type": "CanonicalUser"
            },
            "Permission": "FULL_CONTROL"
        }
    ]
}


---




6.1.2 Check the S3 bucket ARN
------------------------------

Go to the S3 console

  https://console.aws.amazon.com/s3/home?region=us-east-1


Click on the bucket 'lambda-for-kinesis-ds-gabriel'

  https://console.aws.amazon.com/s3/buckets/lambda-for-kinesis-ds-gabriel?region=us-east-1&tab=objects


Clock on "Properties" tab

  https://console.aws.amazon.com/s3/buckets/lambda-for-kinesis-ds-gabriel?region=us-east-1&tab=properties


Copy the value of "Amazon Resource Name (ARN)"

  arn:aws:s3:::lambda-for-kinesis-ds-gabriel

---







10.3 Create IAM role 'lambda-write-to-s3-bucket' [DONE, NOT NEEDED]
-------------------------------------------------------------------

See

  https://www.chaossearch.io/blog/how-to-create-an-s3-bucket-with-aws-cli


---

Synopsis:

  $ aws iam create-role --role-name write-to-s3-bucket --assume-role-policy-document \
  '{ \
     "Version": "2012-10-17", \
     "Statement": \
          [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}] \
   }'

---



10.3.1 Create policy doc [DONE]
-------------------------------

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ more lambda-trust-policy.json
   {
    "Version": "2012-10-17",  
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }


---




10.3.2 Run 'aws iam create-role --role-name lambda-write-to-s3-bucket'
----------------------------------------------------------------------

Create role 'lambda-write-to-s3-bucket'

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ aws iam create-role \
         --role-name lambda-write-to-s3-bucket \
         --assume-role-policy-document file://lambda-trust-policy.json

  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-write-to-s3-bucket",
        "RoleId": "AROASASKFEOOFHYP2XGG3",
        "Arn": "arn:aws:iam::138668221340:role/lambda-write-to-s3-bucket",
        "CreateDate": "2021-09-26T15:25:21+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
  }


---






10.3.3 Check role 'lambda-write-to-s3-bucket' and get its ARN
--------------------------------------------------------------


o show all roles

   gabriel $ aws iam list-roles | egrep RoleName
            "RoleName": "AmazonSSMRoleForAutomationAssumeQuickSetup",
            "RoleName": "AmazonSSMRoleForInstancesQuickSetup",
            "RoleName": "AWSServiceRoleForAmazonEKS",
            "RoleName": "AWSServiceRoleForAutoScaling",
            "RoleName": "AWSServiceRoleForECS",
            "RoleName": "AWSServiceRoleForElasticLoadBalancing",
            "RoleName": "AWSServiceRoleForSupport",
            "RoleName": "AWSServiceRoleForTrustedAdvisor",
            "RoleName": "ecsInstanceRole",
            "RoleName": "ecs_instance_role",
            "RoleName": "lambda-kinesis-role-created-from-console",
            "RoleName": "lambda-role-created-from-console",
            "RoleName": "lambda-write-to-s3-bucket",
            "RoleName": "my-function-role-ii6bhoya",
            "RoleName": "ServerlessExample_iam_role",
            "RoleName": "ServerlessExample_iam_role_1",



o list role "lambda-write-to-s3-bucket"

   gabriel $ aws iam list-roles | jq -M '.Roles[] | select(.RoleName=="lambda-write-to-s3-bucket")'
  {
   "Path": "/",
   "RoleName": "lambda-write-to-s3-bucket",
   "RoleId": "AROASASKFEOOFHYP2XGG3",
   "Arn": "arn:aws:iam::138668221340:role/lambda-write-to-s3-bucket",
   "CreateDate": "2021-09-26T15:25:21+00:00",
   "AssumeRolePolicyDocument": {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "lambda.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   },
   "MaxSessionDuration": 3600
 }



o get role "lambda-write-to-s3-bucket"

  gabriel $ aws iam get-role --role-name "lambda-write-to-s3-bucket"
  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-write-to-s3-bucket",
        "RoleId": "AROASASKFEOOFHYP2XGG3",
        "Arn": "arn:aws:iam::138668221340:role/lambda-write-to-s3-bucket",
        "CreateDate": "2021-09-26T15:25:21+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {}
    }
   }


---


o Get the ARN of the role

   gabriel $ aws iam get-role --role-name "lambda-write-to-s3-bucket" | jq -M '.Role.Arn'
  "arn:aws:iam::138668221340:role/lambda-write-to-s3-bucket"


---




10.4 Create policy 'write-to-S3-bucket' and attach it to role 'lambda-write-to-s3-bucket' [DONE, NOT NEEDED]
-------------------------------------------------------------------------------------------------------------


We have

o bucket lambda-for-kinesis-ds-gabriel with ARN

     "arn:aws:s3:::lambda-for-kinesis-ds-gabriel",
     "arn:aws:s3:::lambda-for-kinesis-ds-gabriel/*"


o role 'lambda-write-to-s3-bucket', so far w/o any policy



Now we create the policy document then attach it to the role.


Synopsis

  $ aws iam put-role-policy \
        --role-name lambda-write-to-s3-bucket \
	--policy-name lambda-write-to-s3-bucket-policy \
	--policy-document '{"Version":"2012-10-17", "Statement":[{"Effect":"Allow", "Action":"s3:*", \
"Resource":["arn:aws:s3:::chaos-blog-test-bucket","arn:aws:s3:::chaos-blog-test-bucket/*"]}]}'

---



10.4.1 Create policy document lambda-write-to-s3-bucket-policy.json
-------------------------------------------------------------------


Create the policy docuement as JSON 

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ more lambda-write-to-s3-bucket-policy.json
  {
    "Version": "2012-10-17",  
    "Statement": [
      {
        "Effect": "Allow",
	"Action":"s3:*",
	"Resource": [
           "arn:aws:s3:::lambda-for-kinesis-ds-gabriel",
           "arn:aws:s3:::lambda-for-kinesis-ds-gabriel/*"
	]
      }
    ]
  }


---




10.4.2 Attach policy doc lambda-write-to-s3-bucket-policy.json to role lambda-write-to-s3-bucket [DONE]
--------------------------------------------------------------------------------------------------------


Attach policy doc to role "lambda-write-to-s3-bucket":

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ aws iam put-role-policy \
        --role-name lambda-write-to-s3-bucket \
	--policy-name lambda-write-to-s3-bucket-policy \
	--policy-document file://lambda-write-to-s3-bucket-policy.json


Check

  gabriel $ aws iam get-role-policy \
              --role-name lambda-write-to-s3-bucket \
	      --policy-name lambda-write-to-s3-bucket-policy
  {
    "RoleName": "lambda-write-to-s3-bucket",
    "PolicyName": "lambda-write-to-s3-bucket-policy",
    "PolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": [
                    "arn:aws:s3:::lambda-for-kinesis-ds-gabriel",
                    "arn:aws:s3:::lambda-for-kinesis-ds-gabriel/*"
                ]
            }
        ]
    }
  }


---





6.2 Create S3 bucket policy and attach it to bucket 'lambda-for-kinesis-ds-gabriel'
-----------------------------------------------------------------------------------

See

  https://omardulaimi.medium.com/export-cloudwatch-logs-to-s3-with-lambda-dd45cf246766




6.2.0 Command 'aws s3api put-bucket-policy'
-------------------------------------------


Get help

  gabriel $ aws s3api put-bucket-policy help

  NAME
       put-bucket-policy -


  DESCRIPTION

       Applies  an  Amazon S3 bucket policy to an Amazon S3 bucket. If you are
       using an identity other than the root user of the AWS account that owns
       the  bucket, the calling identity must have the PutBucketPolicy permis-
       sions on the specified bucket and belong to the bucket owner's  account
       in order to use this operation.

       If  you don't have PutBucketPolicy permissions, Amazon S3 returns a 403
       Access Denied error. If you have the correct  permissions,  but  you're
       not  using an identity that belongs to the bucket owner's account, Ama-
       zon S3 returns a 405 Method Not Allowed error.

       WARNING:
          As a security precaution, the root user of the AWS account that owns
          a  bucket  can always use this operation, even if the policy explic-
          itly denies the root user the ability to perform this action.

       For more information about bucket policies, see Using  Bucket  Policies
       and User Policies .

       The following operations are related to PutBucketPolicy :

       o CreateBucket

       o DeleteBucket

       See also: AWS API Documentation

       See 'aws help' for descriptions of global parameters.



SYNOPSIS

   put-bucket-policy
          --bucket <value>
          [--content-md5 <value>]
          [--confirm-remove-self-bucket-access | --no-confirm-remove-self-bucket-access]
          --policy <value>
          [--expected-bucket-owner <value>]
          [--cli-input-json | --cli-input-yaml]
          [--generate-cli-skeleton <value>]
          [--cli-auto-prompt <value>]


OPTIONS

       --bucket (string)
          The name of the bucket.

       --content-md5 (string)
          The MD5 hash of the request body.

       --confirm-remove-self-bucket-access | --no-confirm-remove-self-bucket-access (boolean)
          Set this parameter to true to confirm that you want to  remove  your
          permissions to change this bucket policy in the future.

       --policy (string)
          The bucket policy as a JSON document.

       --expected-bucket-owner (string)
          The  account id of the expected bucket owner. If the bucket is owned
          by a different account, the request  will  fail  with  an  HTTP  403
          (Access Denied) error.

       --cli-input-json  |  --cli-input-yaml (string)
       Reads arguments from the JSON string provided.
       The JSON string follows the format  provided by
       --generate-cli-skeleton. If other arguments are provided on the command
       line, those values will override the JSON-provided values.  It  is  not
       possible to pass arbitrary binary values using a JSON-provided value as
       the string will be taken literally. This may  not  be  specified  along
       with --cli-input-yaml.

       --generate-cli-skeleton  (string)  Prints  a  JSON skeleton to standard
       output without sending an API request. If provided with no value or the
       value input, prints a sample input JSON that can be used as an argument
       for --cli-input-json. Similarly, if provided yaml-input it will print a
       sample  input  YAML that can be used with --cli-input-yaml. If provided
       with the value output, it validates the command inputs  and  returns  a
       sample output JSON for that command.

       --cli-auto-prompt  (boolean) Automatically prompt for CLI input parame-
       ters.

       See 'aws help' for descriptions of global parameters.


EXAMPLES

  This example allows all users to retrieve any object in MyBucket except
  those  in  the MySecretFolder. It also grants put and delete permission
  to the root user of the AWS account 1234-5678-9012:


     $ cat policy.json
          {
             "Statement": [
                {
                   "Effect": "Allow",
                   "Principal": "*",
                   "Action": "s3:GetObject",
                   "Resource": "arn:aws:s3:::MyBucket/*"
                },
                {
                   "Effect": "Deny",
                   "Principal": "*",
                   "Action": "s3:GetObject",
                   "Resource": "arn:aws:s3:::MyBucket/MySecretFolder/*"
                },
                {
                   "Effect": "Allow",
                   "Principal": {
                      "AWS": "arn:aws:iam::123456789012:root"
                   },
                   "Action": [
                      "s3:DeleteObject",
                      "s3:PutObject"
                   ],
                   "Resource": "arn:aws:s3:::MyBucket/*"
                }
             ]
          }


     $ aws s3api put-bucket-policy --bucket MyBucket --policy file://policy.json


OUTPUT: None

---




6.2.1 Create S3 bucket policy "s3-bucket-policy.json"
------------------------------------------------------

See

  https://omardulaimi.medium.com/export-cloudwatch-logs-to-s3-with-lambda-dd45cf246766


We have the bucket

  lambda-for-kinesis-ds-gabriel

with ARNs

     "arn:aws:s3:::lambda-for-kinesis-ds-gabriel",
     "arn:aws:s3:::lambda-for-kinesis-ds-gabriel/*"
     


Define policy doc

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ cat s3-bucket-policy.json 
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.us-east-1.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::lambda-for-kinesis-ds-gabriel"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "logs.us-east-1.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::lambda-for-kinesis-ds-gabriel",	    
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
  }


---



6.2.2 Attach the policy to the bucket lambda-for-kinesis-ds-gabriel
--------------------------------------------------------------------

Attach the S3 bucket policy

  "s3-bucket-policy.json"

We have the bucket

  lambda-for-kinesis-ds-gabriel

---

Run

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ aws s3api put-bucket-policy --bucket  lambda-for-kinesis-ds-gabriel --policy file://s3-bucket-policy.json


Check

  gabriel $ aws s3api get-bucket-policy --bucket  lambda-for-kinesis-ds-gabriel 
  {
    "Policy": "{\"Version\":\"2012-10-17\",...}"
  }

and

  gabriel $ aws s3api get-bucket-policy --bucket  lambda-for-kinesis-ds-gabriel  \
                | jq -M '.Policy' | sed 's/"{/{/;s/}"/}/;s/\\//g' | jq -M '.'
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "logs.us-east-1.amazonaws.com"
        },
        "Action": "s3:GetBucketAcl",
        "Resource": "arn:aws:s3:::lambda-for-kinesis-ds-gabriel"
      },
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "logs.us-east-1.amazonaws.com"
        },
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::lambda-for-kinesis-ds-gabriel/*",
        "Condition": {
          "StringEquals": {
            "s3:x-amz-acl": "bucket-owner-full-control"
          }
        }
      }
    ]
  }


---



6.3 Attach policies to role lambda-kinesis-role-created-from-console
----------------------------------------------------------------------


6.3.0 Inital status of role lambda-kinesis-role-created-from-console
---------------------------------------------------------------------


Role

  gabriel $ aws iam get-role --role-name  lambda-kinesis-role-created-from-console
  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-kinesis-role-created-from-console",
        "RoleId": "AROASASKFEOODXUDWTUVP",
        "Arn": "arn:aws:iam::138668221340:role/lambda-kinesis-role-created-from-console",
        "CreateDate": "2021-09-22T21:07:48+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Description": "Allows Lambda functions to call AWS services on your behalf.",
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {
            "LastUsedDate": "2021-09-25T13:10:17+00:00",
            "Region": "us-east-1"
        }
    }
  }

---



Policies

  gabriel $ aws iam list-role-policies --role-name  lambda-kinesis-role-created-from-console
  {
    "PolicyNames": []
  }


  gabriel $ aws iam list-attached-role-policies --role-name  lambda-kinesis-role-created-from-console
  {
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonS3FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        },
        {
            "PolicyName": "AWSXRayDaemonWriteAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
        },
        {
            "PolicyName": "AWSLambdaKinesisExecutionRole",
            "PolicyArn": "arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole"
        },
        {
            "PolicyName": "AWSLambdaBasicExecutionRole",
            "PolicyArn": "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        }
    ]
  }


---



6.3.1 Attach policies AmazonS3FullAccess, CloudWatchLogsFullAccess and CloudWatchEventsFullAccess
--------------------------------------------------------------------------------------------------


o AmazonS3FullAccess

   gabriel $ aws iam attach-role-policy    \
             --role-name  lambda-kinesis-role-created-from-console    \
             --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"


o CloudWatchLogsFullAccess

    gabriel $ aws iam attach-role-policy    \
             --role-name  lambda-kinesis-role-created-from-console    \
             --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"


o CloudWatchEventsFullAccess

   gabriel $ aws iam attach-role-policy    \
             --role-name  lambda-kinesis-role-created-from-console    \
             --policy-arn "arn:aws:iam::aws:policy/CloudWatchEventsFullAccess"

---





6.3.2 Check policies attached to role lambda-kinesis-role-created-from-console
-------------------------------------------------------------------------------

  gabriel $ aws iam list-attached-role-policies --role-name  lambda-kinesis-role-created-from-console
  {
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonS3FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        },
        {
            "PolicyName": "AWSXRayDaemonWriteAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
        },
        {
            "PolicyName": "CloudWatchLogsFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
        },
        {
            "PolicyName": "AWSLambdaKinesisExecutionRole",
            "PolicyArn": "arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole"
        },
        {
            "PolicyName": "AWSLambdaBasicExecutionRole",
            "PolicyArn": "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        },
        {
            "PolicyName": "CloudWatchEventsFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/CloudWatchEventsFullAccess"
        }
    ]
  }

```

