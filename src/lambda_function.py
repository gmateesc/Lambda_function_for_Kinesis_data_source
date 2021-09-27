
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
