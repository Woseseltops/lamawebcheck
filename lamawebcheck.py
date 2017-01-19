import json
import datetime

from unittest import TestLoader, runner
from sys import argv

from os import mkdir
from os.path import isdir

#Importing the setting and the webcheck configuration file
try:
    check_configuration = open(argv[1]).readlines()
    settings = json.load(open(argv[2]))

except IndexError:
    print('python3 lamawebcheck.py /path/to/check_config_file.conf /path/to/settings.json')
    quit()

#Parse the check configuration file
checks_per_type = {}

for raw_webcheck in check_configuration:

    items = raw_webcheck.strip().split()
    url = items[0]
    check_type = items[1]
    args = ' '.join(items[2:])

    try:
        checks_per_type[check_type].append((url,args))
    except KeyError:
        checks_per_type[check_type] = [( url,args)]

#Insert information about urls to test in the test, using the name of the classes of the checks
suite_groups = TestLoader().discover('')
for suite_group in suite_groups:
    for suite in suite_group:
        for test in suite:
            check_type_name = test.__class__.__name__.lower()[4:]
            
            try:
                test.urls = checks_per_type[check_type_name]
            except KeyError:
                test.urls = []

#Create the log environment
if not isdir(settings['log_directory']):
    mkdir(settings['log_directory'])

if settings['log_directory'][-1] != '/':
    settings['log_directory']+= '/'

logfile = open(settings['log_directory']+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),'w')

#Run the tests
runner.TextTestRunner(logfile).run(suite_groups)
