from Widgets.widget import Widget
from Requests.request import Request
import logging

class S3Handler:

    
    def __init__(self, widget, request):
        self.widget = widget
        self.request = request
        self.client = ""
        
    # write object to a S3 bucket 
    def write(self,  client,  target_bucket):
        
        
        object_key = f"widgets/{self.widget.owner}/{self.widget.widgetId}"
        # print(self.widget.owner)
        # print(self.widget.widgetId)
        # print(object_key)
        logging.basicConfig(filename="s3.log", level=logging.INFO)
        self.client = client
        self.client.put_object(Body=self.widget.toJSON(), Bucket= target_bucket, Key=object_key)
        logging.warning(f'added object {object_key} to S3 bucket')