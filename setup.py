import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='pojson',
    version = '0.1',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    long_description='',
    packages=['pojson'],
    include_package_data = True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'argh',
        'polib',
        'simplejson',
        'argparse',
        'pytest >= 2.0', # XXX test require
    ],
    entry_points= {
        'console_scripts': [
            'pojson = pojson.main:main',
        ]
        },
    
    )
