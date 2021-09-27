# Lambda_function_for_Kinesis_data_source

Implement a Lambda function that consumes events from Kinesis and exports them to S3.


## Prerequisites

The AWS client is installed on the machine, and the AWS configuration and credentials are set up under
```bash
   ~/.aws
```




## Lambda function code 


I have implemented the lambda function in Python. I developed the code
on the local host, and I created the lambda function with AWS CLI
(aws lambda create-function), thereby getting the oppoortunity to
develop and test the lambda function using AWS Cloud9
integrated development environment as shown below:


![lambda_function.py](images/lambda_function_code.png)


Let's described the Python code in detail:

```python
  $ cat lambda_function.py

  import json
  import base64
  import datetime
  import boto3

  print('Loading function lambda_handler')
  s3 = boto3.client('s3')

  def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))
    keys = []

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        payload_str = str(payload,encoding='utf-8')
        print("Decoded payload: " + payload_str)
        
        now = datetime.datetime.now()
        ts = str(int(now.timestamp() * 1000)) + '_ms'
        s3.put_object(Body=payload, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts)
        keys.append(ts)
    
    return {
        'statusCode': 200,
        'body': ','.join(keys)
    }

```

The `lambda_handler` function receives receives and processes events from a Kinesis data,
which is configured as shown in section

  7.4 Add Kinesis stream 'kinesis-stream-for-lambda' as event source to Lambda func 'ProcessKinesisEventsAndPersistToS3'


The for loop iterates over all event records in `event['Records']`, extracts the payload,
writes it to the CloudWatch logs and exports it to the S3 bucket 'lambda-for-kinesis-ds-gabriel'
(section 4. Create the S3 bucket 'lambda-for-kinesis-ds-gabriel' and attach bucket policy,
described the creation of the S3 bucket 'lambda-for-kinesis-ds-gabriel').


We use the time stamp (current time in milliseconds) as the key of the object inserted in S3,
and the payload of the event as the body of the object.


Thus, we persist the Kinesis events to S3.




## AWS CLI Version

The version of he AWS client we use is
```bash
   gabriel $ aws --version
   aws-cli/2.0.62 Python/3.9.0 Darwin/19.6.0 source/x86_64
```





##  Create IAM role 'lambda-get-kinesis-events-export-to-s3'


### Create policy document

The  policy doc is

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




### Run 'aws iam create-role --role-name lambda-get-kinesis-events-export-to-s3'


Create role 'lambda-get-kinesis-events-export-to-s3'

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ aws iam create-role \
         --role-name lambda-get-kinesis-events-export-to-s3 \
         --assume-role-policy-document file://lambda-trust-policy.json

  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-get-kinesis-events-export-to-s3",
        "RoleId": "AROASASKFEOOGGMYWPZGG",
        "Arn": "arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3",
        "CreateDate": "2021-09-27T17:32:44+00:00",
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




#### Check role lambda-get-kinesis-events-export-to-s3

  gabriel $ aws iam get-role --role-name lambda-get-kinesis-events-export-to-s3
  {
    "Role": {
        "Path": "/",
        "RoleName": "lambda-get-kinesis-events-export-to-s3",
        "RoleId": "AROASASKFEOOGGMYWPZGG",
        "Arn": "arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3",
        "CreateDate": "2021-09-27T17:32:44+00:00",
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






### Assign policies to the role lambda-get-kinesis-events-export-to-s3


Will assign the polices needed to access Kinesis, CloudWatch and S3.


#### Initial policies attached to role 'lambda-get-kinesis-events-export-to-s3'

```bash
    gabriel $ aws iam list-attached-role-policies --role-name lambda-get-kinesis-events-export-to-s3
    {
      "AttachedPolicies": []
    }

```



#### Attach the following policies to the role 'lambda-get-kinesis-events-export-to-s3'


- AWSLambdaBasicExecutionRole
```
   gabriel $ aws iam attach-role-policy    \
                 --role-name  lambda-get-kinesis-events-export-to-s3    \
                 --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```


- AWSLambdaKinesisExecutionRole
```
   gabriel $ aws iam attach-role-policy    \
                 --role-name  lambda-get-kinesis-events-export-to-s3    \
                 --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole
```                          


- CloudWatchLogsFullAccess
```
    gabriel $ aws iam attach-role-policy    \
                  --role-name  lambda-get-kinesis-events-export-to-s3    \
                  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
```


- CloudWatchEventsFullAccess
```
   gabriel $ aws iam attach-role-policy    \
                 --role-name  lambda-get-kinesis-events-export-to-s3    \
                 --policy-arn arn:aws:iam::aws:policy/CloudWatchEventsFullAccess
```


- AmazonS3FullAccess
```
   gabriel $ aws iam attach-role-policy    \
                 --role-name  lambda-get-kinesis-events-export-to-s3    \
                 --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

```



#### Check policies attached to the role 'lambda-get-kinesis-events-export-to-s3'
```
   gabriel $ aws iam list-attached-role-policies --role-name lambda-get-kinesis-events-export-to-s3
   {
     "AttachedPolicies": [
        {
            "PolicyName": "AmazonS3FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3FullAccess"
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




```

3. Create IAM role 'lambda-get-kinesis-events-export-to-s3'
     
     3.1 Create policy doc
	   
     3.2 Run 'aws iam create-role --role-name lambda-get-kinesis-events-export-to-s3'
	   
     3.3 Assign policies to the role lambda-get-kinesis-events-export-to-s3






4. Create the S3 bucket 'lambda-for-kinesis-ds-gabriel' and attach bucket policy

    4.1 Create S3 bucket 'lambda-for-kinesis-ds-gabriel'
          4.1.1 Run the "aws s3 create-bucket" CLI
          4.1.2 Check the S3 bucket ARN


    4.2 Create S3 bucket policy and attach it to bucket 'lambda-for-kinesis-ds-gabriel'
          4.2.0 Command 'aws s3api put-bucket-policy'
          4.2.1 Create S3 bucket policy "s3-bucket-policy.json"
          4.2.2 Attach the policy to the bucket lambda-for-kinesis-ds-gabriel





5. Create Kinesis stream

    5.0 How to create Kinesis stream and make it the event source for the lambda function [DOC]

    5.1 Create the Kinesis event stream 'kinesis-stream-for-lambda'




6. Export CloudWatch logs to S3



7. Create the lambda function that writes Kinesis events to S3


     7.3 Deploy the lambda function
     
           7.3.1 Create deployment package

           7.3.2 Create lambda-function ProcessKinesisEventsAndPersistToS3

           7.3.3 Invoke function with test event
	  
                   7.3.3.1 Test function from the Lambda function console
                             7.3.3.1.1 Create test event 'kinesis-event'
                             7.3.3.1.2 Invoke lambda fnction with test event 'kinesis-event'

                   7.3.3.2 Test function from the AWS CLI
                             7.3.3.2.1 Create simple Kinesis event kinesis_simple_event.json
                             7.3.3.2.2 Invoke lambda function with event kinesis_simple_event.json		  




     7.4 Add Kinesis stream 'kinesis-stream-for-lambda' as event source to Lambda func 'ProcessKinesisEventsAndPersistToS3'

           7.4.1 The Kinesis stream "kinesis-stream-for-lambda"

           7.4.2 Add Kinesis stream as event source to function 'ProcessKinesisRecords'

           7.4.3 Check event source mappings for lambda function 'ProcessKinesisEventsAndPersistToS3'



     7.5 Test the lambda function

           7.5.0 Test function from the Lambda function console
                    7.5.0.1 Create test event 'kinesis-event'
                    7.5.0.2 Invoke lambda fnction with test event 'kinesis-event'
                    7.5.0.3 Get the S3 object created by lambda invocation from console

           7.5.1 Test function from the AWS CLI
                    7.5.1.1 Create simple Kinesis event kinesis_simple_event.json
                    7.5.1.2 Invoke lambda function with event kinesis_simple_event.json
                    7.5.1.3 Get the S3 object created by lambda invocation


---









4. Create the S3 bucket 'lambda-for-kinesis-ds-gabriel' and attach bucket policy
---------------------------------------------------------------------------------



4.1 Create S3 bucket 'lambda-for-kinesis-ds-gabriel'    
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




4.1.1 Run the "aws s3 create-bucket" CLI
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




4.1.2 Check the S3 bucket ARN
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




5. Create Kinesis stream and associate it with the Lambda function
------------------------------------------------------------------


See

  Section "Create a Kinesis stream" under
  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html




5.0 How to create Kinesis stream and make it the event source for the lambda function [DOC]
--------------------------------------------------------------------------------------------


Steps:


1. Use the create-stream command to create a stream:

     aws kinesis create-stream --stream-name KINESIS_EVENT_STREAM_NAME --shard-count 1



2. Then get the stream ARN using the describe-stream command:

     aws kinesis describe-stream --stream-name KINESIS_EVENT_STREAM_NAME



3. Define the Kinesis stream as event source for the lambda function

   aws lambda create-event-source-mapping \
      --function-name LAMBDA_FUNCTION \
      --event-source  ARN_OF_KINESIS_EVENT_SOURCE
      --batch-size 100 \
      --starting-position LATEST

---




5.1 Create the Kinesis event stream 'kinesis-stream-for-lambda'
---------------------------------------------------------------


1. Use the create-stream command to create the stream 'kinesis-stream-for-lambda':

    gabriel $ aws kinesis create-stream --stream-name kinesis-stream-for-lambda --shard-count 1



2. Then get the stream ARN using the describe-stream command:

    gabriel $ aws kinesis describe-stream --stream-name kinesis-stream-for-lambda| jq -M '.StreamDescription.StreamARN'
    "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda"


We will use the stream ARN in section 7.4 

  7.4 Add Kinesis stream 'kinesis-stream-for-lambda' as event source to Lambda func 'ProcessKinesisEventsAndPersistToS3'

to associate the Kinesis data stream with the Lambda function.

---





6. Export CloudWatch logs to S3
-------------------------------




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





#######

7. Deploy

7.3 Deploy the lambda function
-------------------------------


7.3.1 Create deployment package
--------------------------------

See

  section 4.1.2 Create a deployment package



Create zip script

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ more zip_py.sh
  version=1.0.0
  zip function_py_${version}.zip lambda_function.py



Run zip script

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code
  
  gabriel $ ./zip_py.sh
    adding: lambda_function.py (deflated 46%)
  


Check zip file

  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ ls -l function_py_1.0.0.zip 
  -rw-r--r--  1 gabriel  staff  605 Sep 27 19:17 function_py_1.0.0.zip


---




7.3.2 Create lambda-function ProcessKinesisEventsAndPersistToS3
-----------------------------------------------------------------

See

  sectiom 4.2.3 Create function resource with the CLI

  section 4.2 Create lambda function resource
  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html




Steps:


0. Check config with the CLI

    gabriel $ aws configure
    AWS Access Key ID [****************SYRA]: 
    AWS Secret Access Key [****************ikEd]: 
    Default region name [us-east-2]: us-east-1
    Default output format [json]: 




1. Get the ARN of the role

    gabriel $ aws iam list-roles | jq -M '.Roles[] | select(.RoleName=="lambda-get-kinesis-events-export-to-s3") | .Arn'
    "arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3"

    gabriel $ aws iam get-role --role-name lambda-get-kinesis-events-export-to-s3 | jq -M '.Role.Arn'
    "arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3"



2. Run "aws lamba create-function", specifying the function name of the new function, the zip-file,
   handler, runtime and role

    gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

    gabriel $ aws lambda create-function    \
            --function-name ProcessKinesisEventsAndPersistToS3 \
            --zip-file fileb://function_py_1.0.0.zip   \
            --handler lambda_function.lambda_handler   \
           --runtime python3.9                        \
            --role 'arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3'
    {
       "FunctionName": "ProcessKinesisEventsAndPersistToS3",
       "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisEventsAndPersistToS3",
       "Runtime": "python3.9",
       "Role": "arn:aws:iam::138668221340:role/lambda-get-kinesis-events-export-to-s3",
       "Handler": "lambda_function.lambda_handler",
       "CodeSize": 605,
       "Description": "",
       "Timeout": 3,
       "MemorySize": 128,
       "LastModified": "2021-09-27T18:32:15.391+0000",
       "CodeSha256": "EuGXM3bCwOOJoruOBIVL+GlSQbHcLX+/LwlJCnj7hHU=",
       "Version": "$LATEST",
       "TracingConfig": {
         "Mode": "PassThrough"
       },
       "RevisionId": "a15ce240-1bed-489d-a767-bcf11f1e361c",
       "State": "Active",
       "LastUpdateStatus": "Successful"
    }

---






7.4 Add Kinesis stream 'kinesis-stream-for-lambda' as event source to Lambda func 'ProcessKinesisEventsAndPersistToS3'
-----------------------------------------------------------------------------------------------------------------------



7.4.1 The Kinesis stream "kinesis-stream-for-lambda"
-----------------------------------------------------

See

  section 5.1 Create Kinesis stream with 'aws kinesis create-stream' command



Get name and ARN of Kinesis stream 

  gabriel $ aws kinesis list-streams
  {
    "StreamNames": [
        "kinesis-stream-for-lambda"
    ]
  }


  gabriel $ aws kinesis describe-stream --stream-name kinesis-stream-for-lambda | jq -M '.StreamDescription.StreamARN'
  "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda"


---




7.4.2 Add Kinesis stream as event source to function 'ProcessKinesisRecords'
-----------------------------------------------------------------------------


See

  section 5.2 Add Kinesis stream as event source to Lambda function w/ 'aws lambda create-event-source-mapping'




o List the lambda functions and identify function "ProcessKinesisEventsAndPersistToS3"
 
   gabriel $ aws lambda list-functions \
               | jq -M '.Functions[] | {"FunctionName": .FunctionName, "FunctionArn": .FunctionArn}'
   {
     "FunctionName": "KinesisPassOne",
     "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:KinesisPassOne"
   }
   {
     "FunctionName": "ProcessKinesisEventsAndPersistToS3",
     "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisEventsAndPersistToS3"
   }
   {
     "FunctionName": "ProcessKinesisRecords",
     "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisRecords"
   }




o Get event source mappings for function ProcessKinesisEventsAndPersistToS3

   gabriel $ aws lambda list-event-source-mappings  \
                          --function-name ProcessKinesisEventsAndPersistToS3  \
                         --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda
   {
      "EventSourceMappings": []
   }




o Add the Kinesis stream as an event source to the lambda function

    gabriel $ aws lambda create-event-source-mapping  \
                    --function-name ProcessKinesisEventsAndPersistToS3    \
                    --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda \
                    --batch-size 100 \
                    --starting-position LATEST
    {
      "UUID": "29c5d773-492b-43e3-be4e-3617d9a68bda",
      "BatchSize": 100,
      "MaximumBatchingWindowInSeconds": 0,
      "ParallelizationFactor": 1,
      "EventSourceArn": "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda",
      "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisEventsAndPersistToS3",
      "LastModified": "2021-09-27T22:37:28.422000+02:00",
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


---



7.4.3 Check event source mappings for lambda function 'ProcessKinesisEventsAndPersistToS3'
-------------------------------------------------------------------------------------------


See

  5.2.2 Check the event source mappings for lambda function 'ProcessKinesisRecords'



Get event source mappings for function ProcessKinesisEventsAndPersistToS3

  gabriel $ aws lambda list-event-source-mappings  \
                       --function-name ProcessKinesisEventsAndPersistToS3  \
                       --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda
  {
    "EventSourceMappings": [
        {
            "UUID": "29c5d773-492b-43e3-be4e-3617d9a68bda",
            "BatchSize": 100,
            "MaximumBatchingWindowInSeconds": 0,
            "ParallelizationFactor": 1,
            "EventSourceArn": "arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda",
            "FunctionArn": "arn:aws:lambda:us-east-1:138668221340:function:ProcessKinesisEventsAndPersistToS3",
            "LastModified": "2021-09-27T22:38:00+02:00",
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
                         --function-name ProcessKinesisEventsAndPersistToS3  \
                         --event-source arn:aws:kinesis:us-east-1:138668221340:stream/kinesis-stream-for-lambda \
	          | jq -M '.EventSourceMappings[] | {"State": .State}'
  {
     "State": "Enabled"
  }


---





7.5 Test the lambda function
------------------------------


7.5.0 Test function from the Lambda function console
-------------------------------------------------------


7.5.0.1 Create test event 'kinesis-event'
-----------------------------------------

Go to the Lambda function, select Test tab, then "Configure test event":

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisEventsAndPersistToS3?tab=code

and enter:

  Event template: Kinesis data dtream (kinesos-ge-records)

  Event namr kinesis-simple-event

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

Then click "create"
 
---



7.5.0.2 Invoke lambda fnction with test event 'kinesis-event'
----------------------------------------------------------------


From the lambda function console

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisEventsAndPersistToS3?tab=code

Click on "Test" tab.



I get the response


o Test Event Name
    kinesis-event


o Response

  {
    "statusCode": 200,
    "body": "1632768117322_ms"
  }



o Function Logs

  START RequestId: c1ea44a4-f073-4ce6-ae18-0f9ab35a6515 Version: $LATEST
  Received event: {
    "Records": [{
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
    }]
  }

  Decoded payload: Hello, this is a test 123.
  END RequestId: c1ea44a4-f073-4ce6-ae18-0f9ab35a6515 
  REPORT RequestId: c1ea44a4-f073-4ce6-ae18-0f9ab35a6515  \
         Duration: 238.03 ms \
	 Billed Duration: 239 ms \
	 Memory Size: 128 MB \
	 Max Memory Used: 69 MB	\
	 Init Duration: 423.06 ms


o Request ID

   c1ea44a4-f073-4ce6-ae18-0f9ab35a6515

---



7.5.0.3 Get the S3 object created by lambda invocation from console
--------------------------------------------------------------------

Go to

  https://console.aws.amazon.com/s3/object/lambda-for-kinesis-ds-gabriel?region=us-east-1&prefix=1632747250166_ms

which has

o S3 URI

   s3://lambda-for-kinesis-ds-gabriel/1632747250166_ms
   s3://lambda-for-kinesis-ds-gabriel/1632748493813_ms
   s3://lambda-for-kinesis-ds-gabriel/1632749354552_ms
   s3://lambda-for-kinesis-ds-gabriel/1632749571924_ms


o Object URL

   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632747250166_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632748493813_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632749354552_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632749571924_ms
   

o ARN

   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632747250166_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632748493813_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632749354552_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632749571924_ms

---







7.5.1 Test function from the AWS CLI
-------------------------------------


See

  4.3 Test the lambda function
       4.3.1 Create the input file with sample Kinesis event

  4.4 Get the logs of the Lambda function
       4.4.1 How to get log data with AWS CLI
              4.4.1.1 Get logResult encoded: "aws lambda invoke --function-name FUNC_NAME --log-type Tail"
       4.4.2 Retrieve the logs of the ProcessKinesisRecords function
              4.4.2.2 Get the LogResult and decode it

---



7.5.1.1 Create simple Kinesis event kinesis_simple_event.json
--------------------------------------------------------------


Save it as kinesis_simple_event.json then run


  gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

  gabriel $ more kinesis_simple_event.json 
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




7.5.1.2 Invoke lambda function with event kinesis_simple_event.json
---------------------------------------------------------------------

See

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessKinesisEventsAndPersistToS3?tab=code



Invoke lambda function ProcessKinesisEventsAndPersistToS3 in several ways


1. Invoke with payload file://kinesis_simple_event.json and get the returned valus

    gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

    gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisEventsAndPersistToS3 \
                      --payload file://kinesis_simple_event.json \
                      output.txt
    {
       "StatusCode": 200,
       "ExecutedVersion": "$LATEST"
    }


  Check output

    gabriel $ more output.txt  | jq -M '.'
    {
      "statusCode": 200,
      "body": "1632770555059_ms"
    }

---


2. Invoke with payload file://kinesis_simple_event.json and get the base64 log result
 
    gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

    gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisEventsAndPersistToS3 \
                      --payload file://kinesis_simple_event.json \
                      --log-type Tail		                 \
	              output.txt
  {
      "StatusCode": 200,
      "LogResult": "U1RBUlQgUmVxdWVzdElkOiA1Yzk4NzEyNy1hYmUwLTQ5M2UtOGIzMC05YzU5MTU5ZWFlMWMgVmVyc2lvbjogJExBVEVTVApSZWNlaXZlZCBldmVudDogewoiUmVjb3JkcyI6IFsKewoia2luZXNpcyI6IHsKInBhcnRpdGlvbktleSI6ICJwYXJ0aXRpb25LZXktMDMiLAoia2luZXNpc1NjaGVtYVZlcnNpb24iOiAiMS4wIiwKImRhdGEiOiAiU0dWc2JHOHNJSFJvYVhNZ2FYTWdZU0IwWlhOMElERXlNeTQ9IiwKInNlcXVlbmNlTnVtYmVyIjogIjQ5NTQ1MTE1MjQzNDkwOTg1MDE4MjgwMDY3NzE0OTczMTQ0NTgyMTgwMDYyNTkzMjQ0MjAwOTYxIiwKImFwcHJveGltYXRlQXJyaXZhbFRpbWVzdGFtcCI6IDE0Mjg1Mzc2MDAKfSwKImV2ZW50U291cmNlIjogImF3czpraW5lc2lzIiwKImV2ZW50SUQiOiAic2hhcmRJZC0wMDAwMDAwMDAwMDA6NDk1NDUxMTUyNDM0OTA5ODUwMTgyODAwNjc3MTQ5NzMxNDQ1ODIxODAwNjI1OTMyNDQyMDA5NjEiLAoiaW52b2tlSWRlbnRpdHlBcm4iOiAiYXJuOmF3czppYW06OkVYQU1QTEUiLAoiZXZlbnRWZXJzaW9uIjogIjEuMCIsCiJldmVudE5hbWUiOiAiYXdzOmtpbmVzaXM6cmVjb3JkIiwKImV2ZW50U291cmNlQVJOIjogImFybjphd3M6a2luZXNpczpFWEFNUExFIiwKImF3c1JlZ2lvbiI6ICJ1cy1lYXN0LTEiCn0KXQp9CkRlY29kZWQgcGF5bG9hZDogSGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4KRU5EIFJlcXVlc3RJZDogNWM5ODcxMjctYWJlMC00OTNlLThiMzAtOWM1OTE1OWVhZTFjClJFUE9SVCBSZXF1ZXN0SWQ6IDVjOTg3MTI3LWFiZTAtNDkzZS04YjMwLTljNTkxNTllYWUxYwlEdXJhdGlvbjogMjg1LjYyIG1zCUJpbGxlZCBEdXJhdGlvbjogMjg2IG1zCU1lbW9yeSBTaXplOiAxMjggTUIJTWF4IE1lbW9yeSBVc2VkOiA2OCBNQglJbml0IER1cmF0aW9uOiAzNTkuNjMgbXMJCg==",
      "ExecutedVersion": "$LATEST"
  }





3. Invoke with payload file://kinesis_simple_event.json and get the log result by decoding the base64 data
 
    gabriel $ cd ~/Desktop/GoogleDrive/Cloud/Deployment/02_Terraform/07_Serverless_lambda/03_AWS_lambda_kinesis/02_Code

    gabriel $ aws lambda invoke \
                      --cli-binary-format raw-in-base64-out \
                      --function-name ProcessKinesisEventsAndPersistToS3 \
                      --payload file://kinesis_simple_event.json \
                      --log-type Tail		                 \
                      --query 'LogResult'                        \
		      --output text                              \
	              output.txt | base64 -d


  START RequestId: 64172f63-a548-419d-a3ee-9d568aa672cd Version: $LATEST
  Received event: {
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
    }]
  }
  
  Decoded payload: Hello, this is a test 123.
  END RequestId: 64172f63-a548-419d-a3ee-9d568aa672cd
  REPORT RequestId: 64172f63-a548-419d-a3ee-9d568aa672cd\
         Duration: 171.91 ms\
	 Billed Duration: 172 ms\
	 Memory Size: 128 MB\
	 Max Memory Used: 69 MB


  START RequestId: a88934bd-45b8-447e-9619-547d64b59ee7 Version: $LATEST
    2021-09-25T13:05:14.842Z	a88934bd-45b8-447e-9619-547d64b59ee7	INFO	Decoded payload: Hello, this is a test 123.
  END RequestId: a88934bd-45b8-447e-9619-547d64b59ee7
  REPORT RequestId: a88934bd-45b8-447e-9619-547d64b59ee7 \
         Duration: 84.25 ms     \
	 Billed Duration: 85 ms \
	 Memory Size: 128 MB    \
	 Max Memory Used: 64 MB


---



7.5.1.3 Get the S3 object created by lambda invocation
------------------------------------------------------


Steps:


1. List objects ib the bucket lambda-for-kinesis-ds-gabriel


   gabriel $ aws s3api list-objects --bucket lambda-for-kinesis-ds-gabriel
   {
     "Contents": [
        {
            "Key": "1632747250166_ms",
            "LastModified": "2021-09-27T12:54:11+00:00",
            "ETag": "\"b294169d1e9be8f8171d808b4ce19480\"",
            "Size": 29,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "gabrielmateescu",
                "ID": "9c8c13c3e2fa376172b075f825c42f5ff4cb84d1b225a42822d7fc2f790024b6"
            }
        },
        ...
        {
            "Key": "1632771546597_ms",
            "LastModified": "2021-09-27T19:39:07+00:00",
            "ETag": "\"75c5afa1146857f64e92e6bb6e561ded\"",
            "Size": 26,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "gabrielmateescu",
                "ID": "9c8c13c3e2fa376172b075f825c42f5ff4cb84d1b225a42822d7fc2f790024b6"
            }
        }
     ]
   }





2. List objects in the bucket


  gabriel $ aws s3api list-objects --bucket lambda-for-kinesis-ds-gabriel \
                      | jq -M '.Contents[]|{"Key":.Key,"LastModified":.LastModified}'
  {
    "Key": "1632747250166_ms",
    "LastModified": "2021-09-27T12:54:11+00:00"
  }
  ...
  {
    "Key": "1632762295020_ms",
    "LastModified": "2021-09-27T17:04:56+00:00"
  }
  {
    "Key": "1632768117322_ms",
    "LastModified": "2021-09-27T18:41:58+00:00"
  }
  {
    "Key": "1632770555059_ms",
    "LastModified": "2021-09-27T19:22:36+00:00"
  }
  {
    "Key": "1632771369005_ms",
    "LastModified": "2021-09-27T19:36:10+00:00"
  }
  {
    "Key": "1632771546597_ms",
    "LastModified": "2021-09-27T19:39:07+00:00"
  }




3. Get the object of intrest

   gabriel $ aws s3api get-object --bucket lambda-for-kinesis-ds-gabriel --key "1632771546597_ms" s3_out
   {
      "AcceptRanges": "bytes",
      "LastModified": "2021-09-27T19:39:07+00:00",
      "ContentLength": 26,
      "ETag": "\"75c5afa1146857f64e92e6bb6e561ded\"",
      "ContentType": "binary/octet-stream",
      "Metadata": {}
   }



   gabriel $ more s3_out 
   Hello, this is a test 123.


---







13. Lambda function that writes Kinesis events to S3 [Console and CLI]
----------------------------------------------------------------------


13.1 Generate time stamp as S3 key
----------------------------------

import datetime
now = datetime.datetime.now()
ts = str(int(now.timestamp() * 1000)) + '_ms'

>>> import datetime
>>> now = datetime.datetime.now()

>>> now
datetime.datetime(2021, 9, 27, 14, 44, 50, 410993)

>>> now.timestamp()
1632746690.410993

>>> int(now.timestamp())
1632746690

>>> int(now.timestamp()*1000)
1632746690410

>>> str(int(now.timestamp()*1000)) + '_ms'
'1632746690410_ms'


---





13.2 Create python Lambda function
----------------------------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html
  https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3

  https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html
  https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.17




$ more lambda_function.py

import json
import base64
import boto3
import datetime

print('Loading function lambda_handler')
s3 = boto3.client('s3')
#s3 = boto3.resource('s3')

def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))
    
    keys = []

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        ##print("Decoded payload: " + str(payload))
        ##print("Decoded payload: " + str(payload, 'utf-8'))
        payload_str = str(payload,encoding='utf-8')
        print("Decoded payload: " + payload_str)
	
        now = datetime.datetime.now()
        ts = str(int(now.timestamp() * 1000)) + '_ms'
	keys.append(ts)
        #s3.put_object(Body=payload_str, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts, Content-Type='text/plain')	
        s3.put_object(Body=payload, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts)

    return {
        'statusCode': 200,
        'body': ','.join(keys)
    }

----







13.3 Invoke function with test event
------------------------------------


13.3.1 Create test event 'kinesis-event'
----------------------------------------

kinesis-event

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



13.3.2 Invoke lambda fnction with test event 'kinesis-event'
-------------------------------------------------------------


From the lambda function consol

  https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/KinesisPassOne?newFunction=true&tab=code

Click on "Test" tab.



I get the response


o Test Event Name
    kinesis-event


o Response
  {
    "statusCode": 200,
    "body": "1632750328164_ms"
  }



o Function Logs

  START RequestId: 1fd80a64-04d9-4f1b-a560-2901792e9ff4 Version: $LATEST
  Received event: {
    "Records": [{
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
    }]
  }

  Decoded payload: Hello, this is a test 123.
  END RequestId: 1fd80a64-04d9-4f1b-a560-2901792e9ff4
  REPORT RequestId: 1fd80a64-04d9-4f1b-a560-2901792e9ff4 \
         Duration: 238.03 ms \
	 Billed Duration: 239 ms \
	 Memory Size: 128 MB \
	 Max Memory Used: 69 MB	\
	 Init Duration: 423.06 ms


o Request ID

   1fd80a64-04d9-4f1b-a560-2901792e9ff4

---




13.4 Get the S3 object created by lambda invocation
---------------------------------------------------


13.4.1 Console
--------------

Go to

  https://console.aws.amazon.com/s3/object/lambda-for-kinesis-ds-gabriel?region=us-east-1&prefix=1632747250166_ms

which has

o S3 URI

   s3://lambda-for-kinesis-ds-gabriel/1632747250166_ms
   s3://lambda-for-kinesis-ds-gabriel/1632748493813_ms
   s3://lambda-for-kinesis-ds-gabriel/1632749354552_ms
   s3://lambda-for-kinesis-ds-gabriel/1632749571924_ms


o Object URL

   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632747250166_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632748493813_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632749354552_ms
   https://lambda-for-kinesis-ds-gabriel.s3.amazonaws.com/1632749571924_ms
   

o ARN

   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632747250166_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632748493813_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632749354552_ms
   arn:aws:s3:::lambda-for-kinesis-ds-gabriel/1632749571924_ms

---



13.4.2 CLI
----------


Step 1
-------


Code

  s3.put_object(Body=payload, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts)



o list obj

  gabriel $ aws s3api list-objects --bucket lambda-for-kinesis-ds-gabriel
  {
    "Contents": [
        {
            "Key": "1632747250166_ms",
            "LastModified": "2021-09-27T12:54:11+00:00",
            "ETag": "\"b294169d1e9be8f8171d808b4ce19480\"",
            "Size": 29,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "gabrielmateescu",
                "ID": "9c8c13c3e2fa376172b075f825c42f5ff4cb84d1b225a42822d7fc2f790024b6"
            }
        }
    ]
  }



o Get the object

  gabriel $ aws s3api get-object --bucket lambda-for-kinesis-ds-gabriel --key "1632747250166_ms" out
  {
    "AcceptRanges": "bytes",
    "LastModified": "2021-09-27T12:54:11+00:00",
    "ContentLength": 29,
    "ETag": "\"b294169d1e9be8f8171d808b4ce19480\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
  }

  gabriel $ more out
  b'Hello, this is a test 123.'


---


Step 2
------

Code

  s3.put_object(Body=payload, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts)


Get obj

  gabriel $ aws s3api get-object --bucket lambda-for-kinesis-ds-gabriel --key "1632748493813_ms" out
  {
    "AcceptRanges": "bytes",
    "LastModified": "2021-09-27T13:14:55+00:00",
    "ContentLength": 29,
    "ETag": "\"b294169d1e9be8f8171d808b4ce19480\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
  }

  gabriel $ more out
  b'Hello, this is a test 123.'



---


Step 3
-------

Code

  s3.put_object(Body=payload, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts)


Get obj

  gabriel $ aws s3api get-object --bucket lambda-for-kinesis-ds-gabriel --key "1632749354552_ms" out
  {
    "AcceptRanges": "bytes",
    "LastModified": "2021-09-27T13:29:15+00:00",
    "ContentLength": 29,
    "ETag": "\"b294169d1e9be8f8171d808b4ce19480\"",
    "ContentType": "text/plain",
    "Metadata": {}
  }

  gabriel $ more out
  b'Hello, this is a test 123.'


---


Step 4
------

Code

  payload_str = str(payload,encoding='utf-8')
  s3.put_object(Body=payload_str, Bucket='lambda-for-kinesis-ds-gabriel', Key=ts, Content-Type='text/plain')



Get obj

  gabriel $ aws s3api get-object --bucket lambda-for-kinesis-ds-gabriel --key "1632749571924_ms" out
  {
    "AcceptRanges": "bytes",
    "LastModified": "2021-09-27T13:32:53+00:00",
    "ContentLength": 26,
    "ETag": "\"75c5afa1146857f64e92e6bb6e561ded\"",
    "ContentType": "text/plain",
    "Metadata": {}
  }

  gabriel $ more out
  Hello, this is a test 123.

---









19. Lambda with Kinesis, S3 and CloudWatch [DOC]
------------------------------------------------


19.1 Using AWS Lambda with Amazon Kinesis
-----------------------------------------

See

  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html

  Example Handler.py – Aggregation and processing
  https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html





The following Python function demonstrates how to aggregate and then process your final state:


def lambda_handler(event, context):

    print('Incoming event: ', event)
    print('Incoming state: ', event['state'])

    # Check if this is the end of the window to either aggregate or process.
    if event['isFinalInvokeForWindow']:
        # logic to handle final state of the window
        print('Destination invoke')
    else:
        print('Aggregate invoke')

    # Check for early terminations
    if event['isWindowTerminatedEarly']:
        print('Window terminated early')

    # Aggregation logic
    state = event['state']
    for record in event['Records']:
        state[record['kinesis']['partitionKey']] = state.get(record['kinesis']['partitionKey'], 0) + 1

    print('Returning state: ', state)
    return {'state': state}


---





19.2 Using AWS Lambda with CloudWatch
-------------------------------------



19.2.1 Read CloudWatch logs
---------------------------

  https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchlogs.html



---




19.3 Using AWS Lambda with Amazon S3
------------------------------------


19.3.1 Read and write S3 in Python
----------------------------------


19.3.1.1 Read S3 in Python
--------------------------

See

  Using an Amazon S3 trigger to invoke a Lambda function
  https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html



  import json
  import urllib.parse
  import boto3

  print('Loading function')

  s3 = boto3.client('s3')


  def lambda_handler(event, context):
  
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
    except Exception as e:
        print(e)
        print(f'Error getting obj {key} from bucket {bucket}. Do they exist and is bucket in same region as function.')
        raise e


---



19.3.1.2 Write to S3 in Python
------------------------------


  https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3


import boto3

some_binary_data = b'Here we have some data'
more_binary_data = b'Here we have some more data'

# Method 1: Object.put()
s3 = boto3.resource('s3')
object = s3.Object('my_bucket_name', 'my/key/including/filename.txt')
object.put(Body=some_binary_data)

# Method 2: Client.put_object()
client = boto3.client('s3')
client.put_object(Body=more_binary_data, Bucket='my_bucket_name', Key='my/key/including/anotherfilename.txt')


---






19.3.2 Write obj to S3 in Node.JS
---------------------------------


19.3.2.1 Create function putObjectToS3
--------------------------------------


See

  https://stackoverflow.com/questions/40188287/aws-lambda-function-write-to-s3



var AWS = require('aws-sdk');

function putObjectToS3(bucket, key, data) {

    var s3 = new AWS.S3();
    var params = {
            Bucket : bucket,
            Key : key,
            Body : data
    }
	
    s3.putObject(
	  params,
	  function(err, data) {
              if (err) console.log(err, err.stack); // an error occurred
              else     console.log(data);           // successful response
          }
    );

}


---


19.3.2.2 Use function s3.putObject
----------------------------------


See

  https://github.com/aws/aws-sdk-js/issues/3085


  const params = {
    Body: fs.readFileSync(filePath),
    Bucket: 'myBucketName',
    Key: filePath
  };

  s3.putObject(params, (err, data) => {
     if (err) {
        console.log('ERROR uploading file ' + filePath + ': ' + err);
     }
     else {
        console.log('Uploaded ' + filePath);
     }
  })


---





19.3.3 Export CloudWatch logs to S3
------------------------------------

See

  https://omardulaimi.medium.com/export-cloudwatch-logs-to-s3-with-lambda-dd45cf246766

  https://github.com/omardulaimi/export-cloudwatch-logs-to-s3-using-aws-lambda

  https://gist.github.com/omardulaimi/2e5f8468c063e584c072336df32c74e2#file-cloudwatch-logs-export-py




gabriel $ tree 13_Related/export-cloudwatch-logs-to-s3-using-aws-lambda
13_Related/export-cloudwatch-logs-to-s3-using-aws-lambda
├── BucketPolicy.json
├── CloudWatch-Logs-Export.py
└── README.md

0 directories, 3 files


import boto3
import os
import datetime


currentTime = datetime.datetime.now()
StartDate = currentTime - datetime.timedelta(days=nDays)
#EndDate = currentTime - datetime.timedelta(days=nDays - 1)
EndDate = StartDate

fromDate = int(StartDate.timestamp() * 1000)
toDate = int(EndDate.timestamp() * 1000)

# Create the subfolders' structure based on year, month, day
# Ex: BucketNAME/LogGroupName/Year/Month/Day
BUCKET_PREFIX = os.path.join(PREFIX, StartDate.strftime('%Y{0}%m{0}%d').format(os.path.sep))

def lambda_handler(event, context):
    client = boto3.client('logs')
    client.create_export_task (
         logGroupName=GROUP_NAME,
         fromTime=fromDate,
         to=toDate,
         destination=DESTINATION_BUCKET,
         destinationPrefix=BUCKET_PREFIX
        )


---





```

