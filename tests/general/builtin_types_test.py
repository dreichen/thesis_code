import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import wappl.language_builtins as lb
import generation.vanilla_py as generation

class TestTypes(unittest.TestCase):

    def test_date(self):
        with self.assertRaises(lb.InvalidDateException):
            lb.Date("10.05.2023 14:17:31")

        try:
            lb.Date("10.05.2023")
        except lb.InvalidDateException:
            self.fail(
                "Date constructor unexpectedly raised InvalidDateException")

    def test_datetime(self):
        with self.assertRaises(lb.InvalidDateTimeException):
            lb.Datetime("10.05.2023")

        try:
            lb.Datetime("10.05.2023 14:17:31")
        except lb.InvalidDateTimeException:
            self.fail(
                "Datetime constructor unexpectedly raised InvalidDateTimeException")

    def test_text(self):
        self.assertTrue("foo" == lb.Text("foo"))
        self.assertTrue(lb.Text("bar") == lb.Text("bar"))
        self.assertFalse("bar" == lb.Text("foo"))

    def test_mail(self):
        self.assertTrue(lb.Emailaddress("foo@bar.com") == lb.Emailaddress("foo@bar.com"))

        try:
            lb.Emailaddress("foo@bar.com")
        except lb.InvalidMailException:
            self.fail(
                "EMail constructor unexpectedly raised InvalidMailException")

        with self.assertRaises(lb.InvalidMailException):
            lb.Emailaddress(42)

        with self.assertRaises(lb.InvalidMailException):
            lb.Emailaddress("bar.de")

        with self.assertRaises(lb.InvalidMailException):
            lb.Emailaddress("foo@bar")


if __name__ == '__main__':
    unittest.main()
