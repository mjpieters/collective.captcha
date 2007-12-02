-----------------------------
Captchas without server state
-----------------------------

A view to generate a captcha image and/or wav file, and to verify user input
against it.

A cookie is used to transfer state from one request to the next. The state is
used, together with a server-side secret, to create a random string of
characters, which in turn is displayed as a captcha image, or transformed to
an audio file. Verification happens case-insensitively.

Note that the captcha 'word' is only usable for 5-10 minutes, after which the
view will not accept it any more. Moreover, a different word will be generated
for a given session key every 5 minutes.

This makes these captchas replayable for up to 10 minutes if a determined
user keeps sending the same session id. Because of the server-secret though,
captchas are not transferrable between sites.

Installing
----------

This package requires Plone 2.5 or later and SkimpyGimpy_.

Installing without buildout
~~~~~~~~~~~~~~~~~~~~~~~~~~~

First install SkimpyGimpy. You can install this in either the system python
path or in the lib/python directory of your Zope instance, using the setup.py
script in the SkimpyGimpy source. If you want to install SkimpyGimpy inside
your Zope instance instead of system wide you can its ''--prefix='' option to
install in the ''lib/python'' directory of your Zope instance.

Next you need to install this package. This can also be done by installing it
in either your system path packages or in the lib/python directory of your
Zope instance. You can do this using either easy_install or via the setup.py
script.

After installing the package it needs to be registered in your Zope instance.
This can be done by putting a collective.captcha-configure.zcml file in the
etc/pakage-includes directory with this content::

  <include package="collective.captcha" />

or, alternatively, you can add that line to the configure.zcml in a package or
Product that is already registered.

Installing with buildout
~~~~~~~~~~~~~~~~~~~~~~~~

If you are using `buildout`_ to manage your instance installing
collective.captcha is even simpler. Unfortunately SkimpyGimpy is not yet
easily installed using buildout, you'll still need to install that manually.
You can install collective.captcha by adding it to the eggs line for your
instance::

  [instance]
  eggs = collective.captcha
  zcml = collective.captcha

The last line tells buildout to generate a zcml snippet that tells Zope
to configure collective.captcha.

If another package depends on the collective.captcha egg or includes its zcml
directly you do not need to specify anything in the buildout configuration:
buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'', which
will take care of updating your system.

.. _SkimpyGimpy: http://skimpygimpy.sourceforge.net/
.. _buildout: http://pypi.python.org/pypi/zc.buildout

Using the view
--------------

See the captcha.txt doctest in the collective.captcha.browser package.

Copyright and credits
----------------------

collective.captcha is copyright 2007 by `Jarn`_ (formerly known as Plone
Solutions), and is licensed under the GPL. See LICENSE.txt for details.

It was written by Martijn Pieters.

.. _Jarn: http://www.jarn.com/
