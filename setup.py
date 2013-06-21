from setuptools import setup

setup(
    name = 'uw-gws',
    version = '1.0',
    license = 'Apache',
    url = 'http://github.com/abztrakt/uw-gws',
    description = 'An app for synching Django groups with University of Washington GWS groups.',
    author = 'Craig M. Stimmel, Michael Nguyen',
    packages = ['uw_gws',],
    install_requires = [
        'setuptools',
    ],
)
