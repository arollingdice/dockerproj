import boto3
import json
import sys
from Widgets.widget import Widget
from Dynamo.dynamo_handler import Dynamo_Handler
from S3.s3_handler import S3Handler
from Requests.request import Request
import time
import logging






# storage_method = input('Where do you want to store these widgets:\n A: S3\n B: DynamoDB\n')
# parse the object to JSON

# to store the widget object in S3 or DynamoDB.

storage_method = sys.argv[1]
request_source = sys.argv[2]

if request_source == "bucket":
    requests = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
    i = 0
    requests.queue = requests.request_queue(0)
    while(len(requests.queue)):
         
        # fetch a request from request queue.
        # and parse it into a JSON object
        cur_request_json = requests.json_key(i)
        op = cur_request_json['type']
        print(op)
        # handle create request.
        if op == 'create':
            # create a new widget object using the current request's json.
            new_widget = requests.create_request(object_json=cur_request_json)
            
            # print(new_widget) 
            target_bucket = "usu-cs5260-yucong-web"
            # Write the new widget object to S3 or DynamoDB.
            flag = 0 # flag for writing state.
            if storage_method == "s3":
                s3_handler = S3Handler(widget=new_widget, request=requests)
                s3_handler.write(target_bucket=target_bucket)
                flag = 1
            
            elif storage_method == "dynamo":
                dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                dynamo_handler.write(db_resource='dynamodb')
                flag = 1
                
                
            if flag == 1:# write success
                i = i + 1
                requests.queue = requests.queue[1:]
              
        elif op == 'delete':
            new_widget = requests.delete_request(object_json=cur_request_json)
            

            if storage_method == "s3":
                s3_handler = S3Handler(widget=new_widget, request=requests)
                s3_handler.delete(target_bucket=target_bucket)
                
            
            elif storage_method == "dynamo":
                dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                dynamo_handler.delete()
        
        else:
            
            new_widget = requests.update_request(object_json=cur_request_json)
            
            if storage_method == "s3":
                s3_handler = S3Handler(widget=new_widget, request=requests)
                s3_handler.update(target_bucket=target_bucket)
                
            
            elif storage_method == "dynamo":
                dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                dynamo_handler.update()
        # if request runs out, pause for a while, then
        # try to get new requests.
        if not requests.queue:
            print("Now I wait!!!!")
            i = 0 # reset counter
            time.sleep(3)
            requests = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
        # To do: process DELETE and CHANGE OPREATION
    
else:
    # Create SQS client
    sqs = boto3.client('sqs')
    requests = Request(boto3.Session(), client='sqs', bucket_name='usu-cs5260-yucong-requests')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/851124454141/cs5260-requests'
    i = 0
    while(i < 200):
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        if 'Messages' not in response:
            time.sleep(3)
        
        else:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            object_json = json.loads(message['Body'])
            op = object_json['type']
            if op == 'create':
        # create a new widget object using the current request's json.
                new_widget = requests.create_request(object_json=object_json)
                
                # print(new_widget) 
                target_bucket = "usu-cs5260-yucong-web"
                # Write the new widget object to S3 or DynamoDB.
                flag = 0 # flag for writing state.
                if storage_method == "s3":
                    s3_handler = S3Handler(widget=new_widget, request=requests)
                    s3_handler.write(target_bucket=target_bucket)
                    
                
                elif storage_method == "dynamo":
                    dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                    dynamo_handler.write(db_resource='dynamodb')
               
                
            elif op == 'delete':
                new_widget = requests.delete_request(object_json=object_json)
                

                if storage_method == "s3":
                    s3_handler = S3Handler(widget=new_widget, request=requests)
                    s3_handler.delete(target_bucket=target_bucket)
                    
                
                elif storage_method == "dynamo":
                    dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                    dynamo_handler.delete()
            
            else:
                
                new_widget = requests.update_request(object_json=object_json)
                
                if storage_method == "s3":
                    s3_handler = S3Handler(widget=new_widget, request=requests)
                    s3_handler.update(target_bucket=target_bucket)
                    
                
                elif storage_method == "dynamo":
                    dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
                    dynamo_handler.update()
                
                    
            i = i + 1