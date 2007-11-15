# Zope Captcha generation
import random
import sha
import string
import sys

from Acquisition import aq_inner
from Products.Five import BrowserView

# Create a starting state. Note that random is not cryptographically sound,
# but captchas only need to be resistant to spambots, not haxx0rs.
SEKRIT_KEY = str(random.int(sys.maxint))

CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789@:.-/' # no 0/O and I/1 confusion

COOKIE_ID = 'captchasessionid'
WORDLENGTH = 7

class Captcha(BrowserView):
    """Captcha generating and verifying view
        
    Usage: 
        
        - Use the view from a page to generate an image tag and/or an audio
          URL. Use the 'image_tag' and 'audio_url' methods for these.
        
        - Place the image tag and/or audio url in the page
        
        - The image tag will load the captcha for the user, or the user will
          use the audio url to listen to the aural captcha.
        
        - The user will identify the word, and tell the server through a form
          submission.
        
        - Use the user input to verify.
        
    The view will ensure that the session info is passed along correctly.
        
    """
    
    _id_count = 0
    _session_id = None
    
    def _generate_session(self):
        """Ensure a session id exists
        
        Returns an integer counter of the number of captcha sessions active
        besides ourselves. Use this counter to ensure we get the correct
        session for an image or file.
        
        """
        if self._session_id is None:
            id = sha.new(random.int(sys.maxint)).hexdigest()
            base = name = COOKIE_ID
            while name in self.request:
                self._id_count += 1
                name = base + str(self._id_count)
            self.request.response.setCookie(name, id, path='/')
            self._session_id = id
        return self._session[0]
    
    def _generate_word(self):
        """Create a word for the current session"""
        cookie_id = COOKIE_ID
        if self._id_count:
            cookie_id += str(self._id_count)
        session = self.request(cookie_id)
        
        # To minimize the risk that a word can be computed from the session
        # key, mix in a server secret
        seed = sha.new(SEKRIT_KEY).update(session).digest()
        
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
        return '<img src="%s" width="200", height="100"/>' % (
            self._url('image'),)
    
    def audio_url(self):
        return self._url('audio')
        
    def verify(self, input):
        """Verify that the correct user input was given"""
        result = input.upper() == self._generate_word()
        # Delete the session key, we are done with this captcha
        self.request.response.expireCookie(name, path='/')
        return result
        
    def image(self):
        """Return a generated captcha image"""
        pass
    
    def audio(self):
        """Return a generated captcha audio file"""
        pass
    
    