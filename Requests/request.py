import boto3
import json
from Widgets.widget import Widget



class Request:
    
    def __init__(self, session, client, bucket_name):
        self.session = session
        self.client = self.session.client(client)
        self.bucket_name = bucket_name
        self.op_type = ""
        self.queue = []
        
    # return all existing requests in the bucket.
    def request_queue(self, count):
        if count == 0:
            queue = self.client.list_objects_v2(Bucket=self.bucket_name)
            self.queue = queue.get("Contents")
            return self.queue
        else:
            return self.queue
    
    # return 1 request per function call;
    def get_request(self, count):
        return self.request_queue(count)[0]
        
    def json_key(self, count):
        object_key = self.get_request(count)['Key']
        response_from_client = self.client.get_object(Bucket=self.bucket_name, Key=object_key)
        
        object_json = json.loads(response_from_client['Body'].read().decode('utf-8'))
        
        return object_json
        
    def create_request(self, object_json):
        self.op_type = object_json['type']
        
        if self.op_type != "create":
            raise TypeError("Incorrect request type. This function is for create request.")
            
        # parse JSON object to an Widget object.
        new_widget = Widget(object_json)
        
        return new_widget
        
    def delete_request(self, object_json):
        self.op_type = object_json['type']
        
        if self.op_type != "delete":
            raise TypeError("Incorrect request type. This function is for delete request.")
            
        # parse JSON object to an Widget object.
        new_widget = Widget(object_json)
        
        return new_widget
        
    def update_request(self, object_json):
        self.op_type = object_json['type']
        oj = object_json
        
        if self.op_type != "update":
            raise TypeError("Incorrect request type. This function is for update request.")
            
        # parse JSON object to an Widget object.
        new_widget = Widget(object_json)
        
        return new_widget