import unittest
import doctest
from os import remove
from os.path import dirname
from zope.component import provideUtility
from zope.testing import cleanup
from plone.keyring.interfaces import IKeyManager

# Use a real Request and Response; there are too many subtleties
from ZPublisher.Request import Request
from ZPublisher.Response import Response

basedir = dirname(__file__)

class DummyRequest(Request):
    def __init__(self):
        env = {'SERVER_NAME': 'nohost',
               'SERVER_PORT': '80',
               'REQUEST_METHOD': 'GET'}
        Request.__init__(self, None, env, Response())

class DummyContext(object):
    def absolute_url(self):
        return 'dummyurl'

class DummyKeyManager(object):
    def secret(self):
        return 'tests-only-stable-value'

def captchaSetUp(test):
    # cheat time. dont try it in real life
    with open(basedir+ '/time.py', 'w') as f:
        f.write("def time():\n  return 1500\n")
    provideUtility(DummyKeyManager(), IKeyManager)

def tearDown(test):
    cleanup.cleanUp()
    for s in ('', 'o', 'c'):
        try:
            remove(basedir+ '/time.py'+ s) # purge generated files
        except OSError:
            pass

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('captcha.txt', globs=globals(),
                             setUp=captchaSetUp, tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
