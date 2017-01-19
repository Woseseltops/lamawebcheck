import unittest
from urllib.request import urlopen

class TestOnline(unittest.TestCase):

    def test_online(self):

        for url,arg in self.urls:

            with self.subTest(i=url):
                self.assertEqual(urlopen(url).getcode(), 200) #checks for http 200

if __name__ == '__main__':

    unittest.main()