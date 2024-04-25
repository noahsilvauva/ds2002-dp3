#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/acv7qc"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

messages = []

def get_message():
    for i in range(10):
        try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )

        # Check if there is a message in the queue or not
            if "Messages" in response:
            # extract the two message attributes you want to use as variables
            # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                message = {"order": order, "word": word}
                messages.append(message)
                delete_message(handle)

        # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)
            
    # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])
    
    index = 0 
    word_order = 0

    while len(messages) > 0:
        if messages[index]['order'] == str(word_order):
            print(messages[index]['word'])
            del messages[index]
            index = 0
            word_order += 1
        else:
            index += 1
            continue

# Trigger the function
if __name__ == "__main__":
    get_message()

# Sources:
# https://www.codecademy.com/forum_questions/50ad6fa75a0341fd44001e34
# https://www.w3schools.com/python/python_while_loops.asp