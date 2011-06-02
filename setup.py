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
    version='0.2',
    description="Convert PO files to JSON",
    long_description=long_description,
    keywords='PO i18n internationalisation JSON gettext',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='BSD',
    url='https://bitbucket.org/faassen/pojson',
    packages=['pojson'],
    include_package_data = True,
    zip_safe=False,
    setup_requires=['hgtools'],
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
