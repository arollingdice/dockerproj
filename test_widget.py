import unittest
from Widgets.widget import Widget
from Requests.request import Request
from unittest.mock import patch
import boto3

class TestGetAttribute(unittest.TestCase):
    @patch("Widgets.widget", autospec=True)
    def test_attribute(self, widget_mock):
        key = {'123':32, 'asd':45}
        test = Widget(key)

        # Test when input is a non-string variable
        self.assertRaises(TypeError, test.getAttribute("123"), "123")
        
    @patch("Requests.request", autospec = True)
    def test_update_request(self, requst_mock):
        object_json = {'type': 'update'}
        request_test = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
        self.assertRaises(TypeError, request_test.update_request(object_json))
        
    @patch("Requests.request", autospec = True)
    def test_create_request(self, requst_mock):
        object_json = {'type': 'create'}
        request_test = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
        self.assertRaises(TypeError, request_test.create_request(object_json))
    
    @patch("Requests.request", autospec = True)
    def test_delete_request(self, requst_mock):
        object_json = {'type': 'delete'}
        request_test = Request(boto3.Session(), client='s3', bucket_name='usu-cs5260-yucong-requests')
        self.assertRaises(TypeError, request_test.delete_request(object_json))