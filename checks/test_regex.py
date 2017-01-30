import unittest
from urllib.request import urlopen
import re

def test(self):
    regexp = self.args
    site_content = urlopen(self.url).read().decode('utf-8')
    pattern = re.compile(regexp)
    self.assertTrue(pattern.match(site_content))

if __name__ == '__main__':
    unittest.main()
