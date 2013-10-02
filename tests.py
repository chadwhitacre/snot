import unittest


class Tests(unittest.TestCase):

    def test_success(self):
        pass

    def test_failure(self):
        self.assertTrue(False)

    def test_error(self):
        raise heck
