from Widgets.widget import Widget
from Requests.request import Request
import logging
import boto3

class S3Handler:

    
    def __init__(self, widget, request):
        self.widget = widget
        self.request = request
        self.client = boto3.client('s3')
        self.resource = boto3.resource('s3')
        
    # write object to a S3 bucket 
    def write(self, target_bucket):
        
        
        object_key = f"widgets/{self.widget.owner}/{self.widget.widgetId}"

        logging.basicConfig(filename="s3.log", level=logging.INFO)
        self.client.put_object(Body=self.widget.toJSON(), Bucket= target_bucket, Key=object_key)
        logging.warning(f'added object {object_key} to S3 bucket')
        
    def delete(self, target_bucket):
        
        object_key = f"widgets/{self.widget.owner}/{self.widget.widgetId}"

        logging.basicConfig(filename="s3.log", level=logging.INFO)
 
        self.resource.Object(f'{target_bucket}', object_key).delete()
        logging.warning(f'deleted object {object_key} from S3 bucket')    
        
    def update(self, target_bucket):
        
        object_key = f"widgets/{self.widget.owner}/{self.widget.widgetId}"
        self.resource.Object(f'{target_bucket}', object_key).delete()
        self.client.put_object(Body=self.widget.toJSON(), Bucket= target_bucket, Key=object_key)
        logging.warning(f'updated object {object_key} from S3 bucket') 