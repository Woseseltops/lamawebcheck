# lamawebcheck
A lightweight tool to test availability and content of websites and webservices

Installing lamawebcheck
-----------------------

Requirements:
* Python 3
* git

Just go 

    git clone git@github.com:Woseseltops/lamawebcheck.git
    cd lamawebcheck

And you're good to go.

Configuring lamawebcheck
------------------------

Every time lamawebcheck is run, it needs to know the location of two configuration files:

1 . The settings file, in json format. Example:

    {
	    "email_addresses": ["example@example.com", "john@smith.com"],
	    "log_directory": "/home/user/webchecklogs"
    }
    
    
2 . The list of websites that need to be checked. Each website is on a new line, with this format: `http://url check_type args`. Example:

    http://www.google.nl/ online
    http://applejack.science.ru.nl/ regex <html>\s{5}<center><img src=".{1,150}"></center>\s</html>

Using lamawebcheck
------------------

    python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json

It is advisable to make a cron job that runs this command every now and then. Cron job for every five minutes:

    */5 * * * * python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json

Extending lamawebcheck
----------------------

Each of the checks that can be used in lamawebcheck:
* Can be found in the folder `checks`.
* Is a testcase from Python's `unittesting` module.
* Is expected to be in a separate file, class and function, starting with `test_`, `Test` and `test_` respectively.
* Is expected to iterate over the content in `self.urls` (all urls that this check should be performed on, in this run), and do an assertion for each of them as part of `with self.subTest(i=url):`

An example of an extremely basic check:


    import unittest
    from urllib.request import urlopen


    class TestOnline(unittest.TestCase):

        def test_online(self):
            for url,arg in self.urls:
                with self.subTest(i=url):
                    self.assertEqual(urlopen(url).getcode(), 200) #checks for http 200


Ideas for improvement
---------------------
* It should not be needed that the iteration over urls should be specified for each individual check. Maybe make a more abstract class that can do this, and then subclass?
