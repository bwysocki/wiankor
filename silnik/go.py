import boto3

# Create SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-central-1.amazonaws.com/719069272797/wiankor-silnik'

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
