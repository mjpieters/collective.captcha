import unittest
from zope.testing.doctestunit import DocFileSuite

# Set the secret and test time to constants to keep the tests workable
import collective.captcha.browser.captcha as captcha
captcha.SEKRIT = 'tests-only-stable-value'
captcha._TEST_TIME = 5

class DummyRequest(object):
    def __init__(self):
        self.cookies = {}
        self.expiredcookies = set()
        self.headers = {}
    
    @property
    def response(self):
        return self
    
    def setCookie(self, name, value, path=None):
        self.cookies[name] = value
    
    def expireCookie(self, name, path=None):
        self.expiredcookies.add(name)
        
    def setHeader(self, name, value):
        self.headers[name] = value
        
    def __contains__(self, name):
        return name in self.cookies
    
    def __getitem__(self, name):
        return self.cookies[name]
        
class DummyContext(object):
    def absolute_url(self):
        return 'dummyurl'

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('captcha.txt', globs=globals()),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
