import boto3
import os

# Create SQS client
sqs = boto3.client('sqs', region_name='eu-central-1', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
queue_url = 'https://sqs.eu-central-1.amazonaws.com/719069272797/wiankor-silnik'

try:
  while True:
    # Long poll for message on provided SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=20
    )
    print(response)
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print(message['Body'])
finally:
  print("Czyszczenie")
