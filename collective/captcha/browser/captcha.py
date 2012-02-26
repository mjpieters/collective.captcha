# Zope Captcha generation
import os.path
from random import getrandbits
from time import time
try:
    from hashlib import sha1
except ImportError: # Python < 2.5
    from sha import new as sha1

from skimpyGimpy import skimpyAPI

from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_inner
from App.Common import package_home
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
PERIOD = 300 # captcha will be valid for PERIOD to 2*PERIOD seconds

class Captcha(BrowserView):
    implements(ICaptchaView)

    _session_id = None
    _secret = ''
    __name__ = 'captcha'

    def __init__(self, context, request):
        super(Captcha, self).__init__(context, request)
        self._secret = getUtility(IKeyManager).secret()

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
            id = hex(getrandbits(64))[2:-1]
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

    def _generate(self, nowish=None):
        if nowish is None:
            nowish = int(time() / PERIOD)

        seed = sha1(self._secret + self.request[COOKIE_ID] + str(nowish)).digest()
        word = ''
        for i in xrange(WORDLENGTH):
            index = ord(seed[i]) % len(CHARS)
            word += CHARS[index]

        return word

    def _generate_words(self):
        """Create words for the current session

        We generate one for the current PERIOD seconds, plus one for the
        previous. This way captcha sessions have a livespan of 2 * PERIOD
        seconds at most.

        """
        # To prevent a race condition, generate *one* nowish for both periods
        nowish = int(time() / PERIOD)
        return (self._generate(nowish), self._generate(nowish - 1))

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
        try:
            words = self._generate_words()
            # Delete the session key, we are done with this captcha
            self.request.response.expireCookie(COOKIE_ID, path='/')
        except KeyError:
            # No cookie was present
            return False
        input = input.upper()
        return input == words[0] or input == words[1]

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
        return skimpyAPI.Png(self._generate(), speckle=1.5,
                             fontpath=VERAMONO).data()

    def audio(self):
        """Generate a captcha audio file"""
        self._verify_session()
        self._setheaders('audio/wav')
        return skimpyAPI.Wave(self._generate(), WAVSOUNDS).data()
