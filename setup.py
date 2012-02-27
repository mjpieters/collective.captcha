import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)

version = '1.7'

setup(name='collective.captcha',
      version=version,
      description="Stateless captcha generation and verification",
      long_description=open(os.path.join(here, "README.rst")).read() + '\n' + \
                       open(os.path.join(here, "CHANGELOG.txt")).read(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='captcha stateless',
      author='Jarn',
      author_email='info@jarn.com',
      url='https://github.com/mjpieters/collective.captcha',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'skimpyGimpy',
          'plone.keyring > 1.0',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
