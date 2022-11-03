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
    
    def __init__(self, type, requestId, widgetId, owner, label, 
    description, otherAttributes):
        self.type = type
        self.requestId = requestId
        self.widgetId = widgetId
        self.owner = owner
        self.label = label
        self.description = description
        self.otherAttributes = otherAttributes
    
    # serialize widget object to JSON string
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
        

    
    def getAttribute(self, s):
        if not isinstance(s, str):
            raise TypeError("The input attribute should be a string")
        

