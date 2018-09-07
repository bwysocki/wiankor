import boto3
import os
import sys
import RPi.GPIO as GPIO
import time

# Create SQS client
sqs = boto3.client('sqs', region_name='eu-central-1', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
queue_url = 'https://sqs.eu-central-1.amazonaws.com/719069272797/wiankor-silnik'

GPIO.setmode(GPIO.BCM)

enable_pin = 18
in_1_pin = 23
in_2_pin = 24

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(in_1_pin, GPIO.OUT)
GPIO.setup(in_2_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(enable_pin, 500)
motor_pwm.start(0)

def forward(duty):
    GPIO.output(in_1_pin, True)
    GPIO.output(in_2_pin, False)
    motor_pwm.ChangeDutyCycle(duty)

def reverse(duty):
    GPIO.output(in_1_pin, False)
    GPIO.output(in_2_pin, True)
    motor_pwm.ChangeDutyCycle(duty)

def stop():
    GPIO.output(in_1_pin, False)
    GPIO.output(in_2_pin, False)
    motor_pwm.ChangeDutyCycle(0)

def cycle():
    forward(30)
    time.sleep(1)
    stop()

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

    if ('Messages' in response):
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        cycle()
        nrOfCycles = message['Body'].split("=")[1].strip()
        print(nrOfCycles)
    else:
        print("No message on the queue")
except:
    print "Unexpected error:", sys.exc_info()[0]
finally:
  print("Finishing...")
