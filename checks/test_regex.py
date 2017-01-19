import unittest
from urllib.request import urlopen
import re

class TestRegex(unittest.TestCase):

    def test_online(self):

        for url,arg in self.urls:

            with self.subTest(i=url):
                site_content = urlopen(url).read().decode('utf8')
                pattern = re.compile(arg)
                self.assertTrue(pattern.match(site_content))

if __name__ == '__main__':

    unittest.main()