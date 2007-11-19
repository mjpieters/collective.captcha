import os
from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.captcha',
      version=version,
      description="Stateless captcha generation and verification",
      long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
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
      zip_safe=False,
      install_requires=[
          'setuptools',
          # SkimpyGimpy has no pypi entry
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
