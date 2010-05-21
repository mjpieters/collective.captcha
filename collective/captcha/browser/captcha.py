# Zope Captcha generation
import os.path
import random
import sha
import sys
import time

from skimpyGimpy import skimpyAPI

from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_inner
from Globals import package_home
from Products.Five import BrowserView
from plone.keyring.interfaces import IKeyManager

from interfaces import ICaptchaView

CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
# note: no 0/o/O and i/I/1 confusion

COOKIE_ID = 'captchasessionid'
WORDLENGTH = 7

_package_home = package_home(globals())
WAVSOUNDS = os.path.join(_package_home, 'waveIndex.zip')
VERAMONO = os.path.join(_package_home, 'arevmoit.bdf')

_TEST_TIME = None

class Captcha(BrowserView):
    implements(ICaptchaView)
    
    _session_id = None
    __name__ = 'captcha'
    
    def _setcookie(self, id):
        """Set the session cookie"""
        resp = self.request.response
        if COOKIE_ID in resp.cookies:
            # clear the cookie first, clearing out any expiration cookie
            # that may have been set during verification
            del resp.cookies[COOKIE_ID]
        resp.setCookie(COOKIE_ID, id, path='/')

    def _generate_session(self):
        """Create a new session id"""
        if self._session_id is None:
            id = sha.new(str(random.randrange(sys.maxint))).hexdigest()
            self._session_id = id
            self._setcookie(id)

    def _verify_session(self):
        """Ensure session id and cookie exist"""
        if not self.request.has_key(COOKIE_ID):
            if self._session_id is None:
                # This may happen e.g. when the user clicks the back button
                self._generate_session()
            else:
                # This may happen e.g. when the user does not accept the cookie
                self._setcookie(self._session_id)
            # Put the cookie value into the request for immediate consumption
            self.request.cookies[COOKIE_ID] = self._session_id
    
    def _generate_words(self):
        """Create words for the current session
        
        We generate one for the current 5 minutes, plus one for the previous
        5. This way captcha sessions have a livespan of 10 minutes at most.
        
        """
        session = self.request[COOKIE_ID]
        nowish = int((_TEST_TIME or time.time()) / 300)
        secret = getUtility(IKeyManager).secret()
        seeds = [sha.new(secret + session + str(nowish)).digest(),
                 sha.new(secret + session + str(nowish - 1)).digest()]
        
        words = []
        for seed in seeds:
            word = []
            for i in range(WORDLENGTH):
                index = ord(seed[i]) % len(CHARS)
                word.append(CHARS[index])
            words.append(''.join(word))
        return words
    
    def _url(self, type):
        return '%s/@@%s/%s' % (
            aq_inner(self.context).absolute_url(), self.__name__, type)
    
    def image_tag(self):
        self._generate_session()
        return '<img src="%s" />' % (self._url('image'),)
    
    def audio_url(self):
        self._generate_session()
        return self._url('audio')
        
    def verify(self, input):
        result = False
        try:
            for word in self._generate_words():
                result = result or input.upper() == word.upper()
            # Delete the session key, we are done with this captcha
            self.request.response.expireCookie(COOKIE_ID, path='/')
        except KeyError:
            pass # No cookie
        
        return result
        
    # Binary data subpages
    
    def _setheaders(self, type):
        resp = self.request.response
        resp.setHeader('content-type', type)
        # no caching please
        resp.setHeader('cache-control', 'no-cache, no-store')
        resp.setHeader('pragma', 'no-cache')
        resp.setHeader('expires', 'now')
        
    def image(self):
        """Generate a captcha image"""
        self._verify_session()
        self._setheaders('image/png')
        return skimpyAPI.Png(self._generate_words()[0],
                             fontpath=VERAMONO).data()
    
    def audio(self):
        """Generate a captcha audio file"""
        self._verify_session()
        self._setheaders('audio/wav')
        return skimpyAPI.Wave(self._generate_words()[0], WAVSOUNDS).data()
