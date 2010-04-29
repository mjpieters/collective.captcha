from zope.interface import implements
from zope.schema import ASCIILine
from collective.captcha.form.interfaces import ICaptcha


class Captcha(ASCIILine):
    implements(ICaptcha)
