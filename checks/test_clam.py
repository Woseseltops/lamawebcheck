import unittest

import json
import random
import os.path
import time
import re
from clam.common.client import CLAMClient


def test(self):
    if ' ' in self.args:
        argfile, username, password = self.args.split(' ')
    else:
        argfile = self.args
        username = None
        password = None
    with open(argfile) as f:
        args = json.load(f)
    client = CLAMClient(self.url,username, password)
    project = 'lamawebchecktest' + str("%034x" % random.getrandbits(128))
    client.create(project)
    for file in args['upload']:
        if not 'parameters' in file:
            file['parameters'] = {}
        if not 'file' in file:
            raise Exception("LamaWebCheck Configuration error: no file specified")
        elif not os.path.exists(file['file']):
            raise Exception("LamaWebCheck Configuration error: file " + file['file'] + " does not exist")
        client.upload(project,file['inputtemplate'], file['file'], **file['parameters'])
    if 'timeout' not in args:
        args['timeout'] = 120
    if 'parameters' not in args:
        args['parameters'] = {}
    data = client.start(project, **args['parameters'])
    if data.errors:
        raise Exception("CLAM service returned an error upon start:" + str(data.errors))
    status = 0
    i = 0
    while status < 2: #while not done
        i += 1
        if i > args['timeout']:
            raise Exception("Timeout waiting for CLAM service to finish")
        data = client.get(project)
        status = data.status
        time.sleep(1)
    if 'download' in args:
        for file in args['download']:
            if 'file' not in file:
                raise Exception("LamaWebCheck Configuration error: no file specified")
            client.download(project, file['file'], '/tmp/lamawebcheck_output')
            if 'regex' in file:
                pattern = re.compile(file['regex'])
                with open('/tmp/lamawebcheck_output','r',encoding='utf-8') as f:
                    self.assertTrue(pattern.match(f.read()))
    client.delete(project)


if __name__ == '__main__':
    unittest.main()
