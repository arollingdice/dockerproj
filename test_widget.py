import unittest
from Widgets.widget import Widget
from unittest.mock import patch


class TestGetAttribute(unittest.TestCase):
    @patch("Widgets.widget", autospec=True)
    def test_attribute(self, widget_mock):
        test = Widget('123','235', '5678', '6789', '568', '1353', ['45756'])

        # Test when input is a non-string variable
        self.assertRaises(TypeError, test.getAttribute("123"), "123")
        