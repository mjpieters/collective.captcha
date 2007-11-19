# Zope Captcha generation
import os.path
import random
import re
import sha
import string
import sys
import time

from skimpyGimpy import skimpyAPI

from zope.interface import implements
from Acquisition import aq_inner
from App.config import getConfiguration
from Globals import package_home
from Products.Five import BrowserView

from interfaces import ICaptchaView

CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789@:.-/' # no 0/O and I/1 confusion

COOKIE_ID = 'captchasessionid'
WORDLENGTH = 7

WAVSOUNDS = os.path.join(package_home(globals()), 'waveIndex.zip')

# Compute a local secret that is semi-unique to a ZEO cluster or standalone
# Zope. This is not rock-solid, but enough to deter spam-bots. Note that this
# assumes Zope clients in a cluster will all have the same <zodb_db *>
# sections. This keeps Captchas from being predictable
_conf = getConfiguration()
SEKRIT = []
for db in _conf.databases:
    SEKRIT.append(repr(db.config.storage.config.__dict__))
SEKRIT = ''.join(SEKRIT)
SEKRIT = re.sub('at 0x[a-f0-9]+>', 'at MEMORYADDRESS>', SEKRIT)

_TEST_TIME = None

class Captcha(BrowserView):
    implements(ICaptchaView)
    
    _session_id = None
    __name__ = 'captcha'
    
    def _generate_session(self):
        """Ensure a session id exists"""
        if self._session_id is None:
            id = sha.new(str(random.randrange(sys.maxint))).hexdigest()
            self.request.response.setCookie(COOKIE_ID, id, path='/')
            self._session_id = id
    
    def _generate_words(self):
        """Create words for the current session
        
        We generate one for the current 5 minutes, plus one for the previous
        5. This way captcha sessions have a livespan of 10 minutes at most.
        
        """
        session = self.request[COOKIE_ID]
        nowish = _TEST_TIME or int(time.time() / 300)
        seeds = [sha.new(SEKRIT + session + str(nowish)).digest(),
                 sha.new(SEKRIT + session + str(nowish - 5)).digest()]
        
        words = []
        for seed in seeds:
            word = []
            for i in range(WORDLENGTH):
                index = ord(seed[i]) % len(CHARS)
                word.append(CHARS[index])
            words.append(''.join(word))
        return words
    
    def _url(self, type):
        self._generate_session()
        return '%s/@@%s/%s' % (
            aq_inner(self.context).absolute_url(), self.__name__, type)
    
    def image_tag(self):
        return '<img src="%s" />' % (self._url('image'),)
    
    def audio_url(self):
        return self._url('audio')
        
    def verify(self, input):
        result = False
        try:
            for word in self._generate_words():
                result = result or input.upper() == word
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
        self._setheaders('image/png')
        return skimpyAPI.Png(self._generate_words()[0]).data()
    
    def audio(self):
        """Generate a captcha audio file"""
        self._setheaders('audio/wav')
        return skimpyAPI.Wave(self._generate_words()[0], WAVSOUNDS).data()
