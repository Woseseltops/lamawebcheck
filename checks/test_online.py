import unittest
from urllib.request import urlopen


def test(self):
    self.assertEqual(urlopen(self.url).getcode(), 200) #checks for http 200

if __name__ == '__main__':
    unittest.main()
