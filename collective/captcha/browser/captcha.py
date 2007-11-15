# Zope Captcha generation
import random
import sha
import string
import sys

from zope.interface import implements
from Acquisition import aq_inner
from Products.Five import BrowserView

from interfaces import ICaptchaView

CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789@:.-/' # no 0/O and I/1 confusion

COOKIE_ID = 'captchasessionid'
WORDLENGTH = 7

class Captcha(BrowserView):
    implements(ICaptchaView)
    
    _id_count = 0
    _session_id = None
    __name__ = 'captcha'
    
    def _generate_session(self):
        """Ensure a session id exists
        
        Returns an integer counter of the number of captcha sessions active
        besides ourselves. Use this counter to ensure we get the correct
        session for an image or file.
        
        """
        if self._session_id is None:
            id = sha.new(str(random.randrange(sys.maxint))).hexdigest()
            base = name = COOKIE_ID
            while name in self.request:
                self._id_count += 1
                name = base + str(self._id_count)
            self.request.response.setCookie(name, id, path='/')
            self._session_id = id
        return self._session_id
    
    def _generate_word(self):
        """Create a word for the current session"""
        cookie_id = COOKIE_ID
        if self._id_count:
            cookie_id += str(self._id_count)
        session = self.request[cookie_id]
        
        seed = sha.new(session).digest()
        
        word = []
        for i in range(WORDLENGTH):
            index = ord(seed[i]) % len(CHARS)
            word.append(CHARS[index])
        return ''.join(word)
        
    def publishTraverse(self, name, request):
        try:
            counter = int(name)
        except ValueError:
            raise KeyError('No such captcha session')
        self._id_count = counter
        return self
    
    def _url(self, type):
        count = self._generate_session()
        url = (aq_inner(self.context).absolute_url(), '@@' + self.__name__,
               type)
        if self._id_count:
            url.insert(2, str(self._id_count))
        return '/'.join(url)
    
    def image_tag(self):
        return '<img src="%s" />' % (self._url('image'),)
    
    def audio_url(self):
        return self._url('audio')
        
    def verify(self, input):
        try:
            result = input.upper() == self._generate_word()
            # Delete the session key, we are done with this captcha
            cookie_id = COOKIE_ID
            if self._id_count:
                cookie_id += str(self._id_count)
            self.request.response.expireCookie(cookie_id, path='/')
        except KeyError:
            result = False # No cookie
        
        return result
        
    def image(self):
        pass
    
    def audio(self):
        pass

