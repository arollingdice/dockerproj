import boto3
import json
import sys
from Widgets.widget import Widget
from Dynamo.dynamo_handler import Dynamo_Handler
from S3.s3_handler import S3Handler
from Requests.request import Request
import time
import logging



requests = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')


# storage_method = input('Where do you want to store these widgets:\n A: S3\n B: DynamoDB\n')
# parse the object to JSON

# to store the widget object in S3 or DynamoDB.
storage_method = sys.argv[1]
requests_queue = requests.request_queue(0)
# print(requests_queue)
i = 0
while(len(requests.queue)):
    
    # fetch a request from request queue.
    # and parse it into a JSON object
    cur_request_json = requests.json_key(i)
    
    
    op = cur_request_json['type']
    # print(op)
    # handle create request.
    print(len(requests.queue))
    if op == 'create':
        # create a new widget object using the current request's json.
        new_widget = requests.create_request(object_json=cur_request_json)
        
        # print(new_widget) 
        target_bucket = "usu-cs5260-yucong-web"
        # Write the new widget object to S3 or DynamoDB.
        flag = 0 # flag for writing state.
        if storage_method == "s3":
            s3_handler = S3Handler(widget=new_widget, request=requests)
            s3_handler.write(client=boto3.client('s3'), target_bucket=target_bucket)
            flag = 1
        
        else:
            dynamo_handler = Dynamo_Handler(widget=new_widget, request=requests)
            dynamo_handler.write(db_resource='dynamodb')
            flag = 1
            
        if flag == 1:# write success
            i = i + 1
            requests.queue = requests.queue[1:]
          
        

    
    else:
        print("not a create request!")
        i = i + 1
        requests.queue = requests.queue[1:]
        
    # if request runs out, pause for a while, then
    # try to get new requests.
    if not requests.queue:
        print("Now I wait!!!!")
        i = 0 # reset counter
        time.sleep(3)
        requests = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
    # To do: process DELETE and CHANGE OPREATION