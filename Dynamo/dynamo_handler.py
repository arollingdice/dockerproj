from Widgets.widget import Widget
from Requests.request import Request
import logging
import json
import boto3

class Dynamo_Handler:
    
    def __init__(self, widget, request):
        self.widget = widget
        self.request = request
        self.table = "my_widgets"

        
    def write(self, db_resource):
        logging.basicConfig(filename="dynamo.log", level=logging.INFO)
        db = boto3.resource('dynamodb')
        table = db.Table(self.table)
        serialize = self.widget.toJSON()
        widget_json = json.loads(serialize)
        
        # store 'otherAttributes' in a variable 
        expand = widget_json['otherAttributes']
        # delete the 'otherAttributes' key regardless 
        # whether it is in the dictionary
        widget_json.pop('otherAttributes', None)
        for i in expand:
            for k, v in i.items():
                widget_json['k'] = v
        
        table.put_item(Item=widget_json)
        logging.warning(f'added object {widget_json["widgetId"]} to dynamo table')
 