import json
import datetime
import unittest
import importlib

from unittest import TestLoader, runner
from sys import argv, path, stderr

from os import mkdir
from os.path import isdir

import smtplib
from email.mime.text import MIMEText

#Importing the setting and the webcheck configuration file
try:
    check_configuration = open(argv[1]).readlines()
    settings = json.load(open(argv[2]))

except IndexError:
    print('python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json')
    quit()

class Test(unittest.TestCase): #base class, tests will be appended dynamically

    def __init__(self, type, testf,name, url, args):
        super(Test,self).__init__()
        self.type = type
        self.testf = testf
        self.name = name
        self.url = url
        self.args = args

    def runTest(self):
        self.testf(self)

    def shortDescription(self):
        return """[%s] %s: %s""" % (self.type, self.name, self.url)

#Parse the check configuration file
checks_per_type = {}

for raw_webcheck in check_configuration:

    items = raw_webcheck.strip().split()

    name = items[0]
    url = items[1]
    check_type = items[2]
    args = ' '.join(items[3:])

    try:
        checks_per_type[check_type].append((name, url,args))
    except KeyError:
        checks_per_type[check_type] = [( name, url,args)]

modules = {} #keep track of dynamically imported modules ourselves
testsuite = unittest.TestSuite()
for check_type, check_data in checks_per_type.items():
    for i, (name, url, args) in enumerate(check_data):
        if check_type not in modules:
            modules[check_type] = importlib.import_module('checks.test_'+check_type)
        testf = modules[check_type].test
        test = Test(check_type, testf,name, url,args)
        testsuite.addTest(test)

#Create the log environment
if not isdir(settings['log_directory']):
    mkdir(settings['log_directory'])

if settings['log_directory'][-1] != '/':
    settings['log_directory']+= '/'

logfile_name = settings['log_directory']+datetime.datetime.now().strftime("%B %d, %Y")
logfile = open(logfile_name,'a')
logfile.write(datetime.datetime.now().strftime("%I:%M%p") + "\n")

#Run the tests
runner.TextTestRunner(logfile, verbosity=2).run(testsuite)
logfile.close()

#Read the log file, and send mail if the last line of the output is not okay
logfile = open(logfile_name,'r')

if logfile.readlines()[-1].strip() != 'OK':

    me = 'wstoop@applejack.science.ru.nl'
    you = settings['email_addresses']

    logfile.seek(0) #Reset pointer
    msg = MIMEText(logfile.read())
    msg['Subject'] = '[Lamawebcheck] Checks have failed'
    msg['From'] = me
    msg['To'] = ';'.join(you)

    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()
