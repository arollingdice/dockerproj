import unittest
from test.widget import getAttribute


class TestGetAttribute(unittest.TestCase):
    def test_attribute(self, widget_mock):
        # Test when input is a non-string variable
        self.assertRaises(TypeError, get_Attribute, 123)
        
        # Test when input key is not one of the attribute
        self.assertRaises(KeyError, get_Attribute, 'master')
        