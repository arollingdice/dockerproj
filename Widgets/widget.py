import logging
import boto3
from botocore.exceptions import ClientError
import os
import json


class Widget:
    type = ""
    requestId = ""
    widgetId = ""
    owner = ""
    label = ""
    description = ""
    otherAttributes = []
    
    def __init__(self, object_json):
        if 'type' in object_json:
            self.type = object_json['type']
            
        if 'requestId' in object_json:
            self.requestId = object_json['requestId']
            
        if 'widgetId' in object_json:
            self.widgetId = object_json['widgetId']
            
        if 'owner' in object_json:
            self.owner = object_json['owner']
            
        if 'label' in object_json:
            
            self.label = object_json['label']
            
        if 'description' in object_json:
            self.description = object_json['description']
            
        if 'otherAttributes' in object_json:
            self.otherAttributes = object_json['otherAttributes']

    # serialize widget object to JSON string
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
        

    
    def getAttribute(self, s):
        if not isinstance(s, str):
            raise TypeError("The input attribute should be a string")
        

