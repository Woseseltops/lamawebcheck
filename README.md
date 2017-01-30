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
        "vars": { "somecustomvariable": "somevalue" },
    }
    
    
2 . The list of websites that need to be checked. Each website is on a new line, with this format: ``id url check_type args``. Example:

    google http://www.google.nl/ online
    mysite http://applejack.science.ru.nl/ regex <html>\s{5}<center><img src=".{1,150}"></center>\s</html>


Using lamawebcheck
------------------

    python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json

It is advisable to make a cron job that runs this command every now and then. Cron job for every five minutes:

    */5 * * * * python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json

Extending lamawebcheck
----------------------

Each of the checks that can be used in lamawebcheck:

* Can be found in the folder ``checks/``.
* Tests are implemented using Python's ``unittest`` module.
* Each check is expected to be in a separate module (file), starting with ``test_``
* The module implements a method ``test(self)`` that runs the test, ``self`` will
  be an instance of ``unittest.TestCase``.
* The URL is available in ``self.url``, argument string in ``self.args``

An example of an extremely basic check:


    import unittest
    from urllib.request import urlopen

    def test(self):
        self.assertEqual(urlopen(self.url).getcode(), 200) #checks for http 200


