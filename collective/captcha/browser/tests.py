import unittest
from zope.component import provideUtility
from zope.testing import doctest, cleanup
from plone.keyring.interfaces import IKeyManager

# Set the secret and test time to constants to keep the tests workable
import collective.captcha.browser.captcha as captcha
captcha._TEST_TIME = 5

class DummyRequest(object):
    def __init__(self):
        self.cookies = {}
        self.headers = {}
    
    @property
    def response(self):
        return self
    
    def setCookie(self, name, value, path=None):
        cookie = self.cookies.get(name, {})
        cookie.update(dict(value=value, path=path))
        self.cookies[name] = cookie
    
    def expireCookie(self, name, path=None):
        cookie = self.cookies.get(name, {})
        cookie['expired'] = True
        self.cookies[name] = cookie
    
    def setHeader(self, name, value):
        self.headers[name] = value
        
    def __contains__(self, name):
        return name in self.cookies
    
    def __getitem__(self, name):
        return self.cookies[name]['value']
        
class DummyContext(object):
    def absolute_url(self):
        return 'dummyurl'

class DummyKeyManager(object):
    def secret(self):
        return 'tests-only-stable-value'

def captchaSetUp(test):
    provideUtility(DummyKeyManager(), IKeyManager)

def tearDown(test):
    cleanup.cleanUp()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('captcha.txt', globs=globals(),
                             setUp=captchaSetUp, tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
