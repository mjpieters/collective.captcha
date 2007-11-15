from setuptools import setup, find_packages

version = '0.1'

setup(name='collective.captcha',
      version=version,
      description="Stateless captcha generation and verification",
      long_description="""\
Captchas without server state
-----------------------------

A view to generate a captcha image and/or wav file, and to verify user input
against it.

A cookie is used to transfer state from one request to the next. The state is
used, together with a server-side secret, to create a random string of
characters, which in turn is displayed as a captcha image, or transformed to
an audio file.

Requirements:
  SkimpyGimpy_
  
_SkimpyGimpy: http://skimpygimpy.sourceforge.net/
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='captcha stateless',
      author='Jarn',
      author_email='info@jarn.com',
      url='http://svn.plone.org/svn/collective/collective.captcha',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
