from setuptools import setup, find_packages

version = '0.1'

setup(name='collective.captcha',
      version=version,
      description="Stateless captcha generation and verification",
      long_description="""\
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
