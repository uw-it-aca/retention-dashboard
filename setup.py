import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/retention-dashboard>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'retention_dashboard/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/retention-dashboard"
setup(
    name='Retention Analytics Dashboard',
    version=VERSION,
    packages=['retention_dashboard'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django>=2.2,<3.0',
        'UW-Django-SAML2>=1.4,<2.0',
        'django-webpack-loader',
        'django-userservice<4.0,>3.1'
    ],
    license='Apache License, Version 2.0',
    description='A tool for interacting with retention analytics',
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)