import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='pojson',
    version='0.7',
    description="Convert PO files to JSON",
    long_description=long_description,
    keywords='PO i18n internationalisation JSON gettext obviel',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='BSD',
    url='https://bitbucket.org/obviel/pojson',
    packages=['pojson'],
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'polib',
        'simplejson',
        'argparse',
        'pytest >= 2.0', # XXX test require
    ],
    entry_points= {
        'console_scripts': [
            'pojson = pojson.main:main',
        ],
        'distutils.commands': [
            'po2json = pojson.frontend:po2json',
            'po2json_babel = pojson.frontend:po2json_babel'
        ],
        },
    
    )
